from flask import Flask, request, jsonify
import boto3
from flask_cors import CORS
from services.bedrock_service import extract_intent
from services.dynamodb_service import book_appointment, cancel_appointment, list_appointments
from services.doctors_service import get_all_doctors, get_doctor_by_id
from services.sns_service import send_email_notification, send_sms_notification
import os 

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
CORS(app) 

@app.route('/')
def home():
    return jsonify({
        "message": "✅ Healthcare AI Assistant backend is running successfully!"
    })


@app.route("/doctors", methods=["GET"])
def list_doctors():
    """Return all doctors."""
    try:
        doctors = get_all_doctors()
        return jsonify({
            "status": "success",
            "count": len(doctors),
            "doctors": doctors
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/doctors/<doctor_id>", methods=["GET"])
def get_doctor(doctor_id):
    """Return details of a specific doctor."""
    try:
        doctor = get_doctor_by_id(doctor_id)
        if not doctor:
            return jsonify({"status": "error", "message": "Doctor not found"}), 404
        return jsonify({"status": "success", "doctor": doctor}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/aws-test')
def aws_test():
    """Test connection with AWS account."""
    try:
        sts = boto3.client("sts")
        identity = sts.get_caller_identity()
        return jsonify({
            "AWS Test": "Connection successful ✅",
            "Account": identity["Account"],
            "UserArn": identity["Arn"]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    


@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data.get("message", "")
    user_id = data.get("user_id", "guest")

    # Step 1 — Understand the message using Bedrock
    intent_data = extract_intent(user_input)
    intent = intent_data.get("intent", "")

    # Step 2 — Execute the correct action
    if intent == "book_appointment":
        msg = book_appointment(
            intent_data["doctor"],
            intent_data["date"],
            intent_data["time"],
            user_id
        )

        # 🔔 Step 3 — Send SNS Notification
        topic_arn = os.getenv("SNS_TOPIC_ARN")
        phone_number = os.getenv("SMS_RECEIVER_NUMBER")
        message = f"Appointment confirmed with {intent_data['doctor']} on {intent_data['date']} at {intent_data['time']}."
        notification_message = (
            f"Appointment confirmed with {intent_data['doctor']} "
            f"on {intent_data['date']} at {intent_data['time']}."
        )
        
        try:
            if topic_arn:
                send_email_notification(
                    topic_arn=topic_arn,
                    subject="Appointment Confirmation",
                    message=message
                )
                print("📩 SNS Email notification sent successfully!")
            else:
                # Optional: send SMS (if number is known)
                # send_sms_notification("+15551234567", message)
                print("⚠️ SNS_TOPIC_ARN not configured. Skipping notification.")
            if phone_number:
                send_sms_notification(phone_number, notification_message)
                print(f"📱 SMS sent successfully to {phone_number}")
        except Exception as e:
            print("⚠️ SNS Notification failed:", e)
    elif intent == "cancel_appointment":
        msg = cancel_appointment(intent_data.get("appointment_id", ""))
    elif intent == "check_appointment":
        records = list_appointments(user_id)
        if not records:
            msg = "You have no upcoming appointments."
        else:
            msg = "📅 Your appointments:\n" + "\n".join(
                [f"{r['doctor_name']} on {r['date']} at {r['time']}" for r in records]
            )
    elif intent_data.get("intent") == "conversation":
        msg = intent_data.get("reply", "I'm here to assist you with appointments.")
    else:
        msg = "Sorry, I didn’t understand that. Please rephrase your request."

    return jsonify({"reply": msg, "ai_output": intent_data})

if __name__ == "__main__":
    # Run Flask app on localhost:5000
    app.run(debug=True, host="0.0.0.0", port=5000)
