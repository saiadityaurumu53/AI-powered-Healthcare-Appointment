from flask import Flask, request, jsonify
import boto3
from flask_cors import CORS
from services.bedrock_service import extract_intent
from services.dynamodb_service import book_appointment, cancel_appointment, list_appointments
from services.doctors_service import get_all_doctors, get_doctor_by_id

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
        msg = book_appointment(intent_data["doctor"], intent_data["date"], intent_data["time"], user_id)
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
    else:
        msg = "Sorry, I didn’t understand that. Please rephrase your request."

    return jsonify({"reply": msg, "ai_output": intent_data})

if __name__ == "__main__":
    # Run Flask app on localhost:5000
    app.run(debug=True, host="0.0.0.0", port=5000)
