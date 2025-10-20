import boto3, uuid
from datetime import datetime
from boto3.dynamodb.conditions import Attr

# Initialize DynamoDB resource
dynamo = boto3.resource("dynamodb", region_name="us-east-1")
table = dynamo.Table("Appointments")

def book_appointment(doctor, date, time, user_id="guest"):
    """Book a new appointment."""
    appointment_id = str(uuid.uuid4())
    item = {
        "appointment_id": appointment_id,
        "user_id": user_id,
        "doctor_name": doctor,
        "date": date,
        "time": time,
        "status": "BOOKED",
        "created_at": str(datetime.utcnow())
    }
    table.put_item(Item=item)
    return f"✅ Appointment booked with {doctor} on {date} at {time}."

def cancel_appointment(appointment_id):
    """Cancel an existing appointment."""
    table.update_item(
        Key={"appointment_id": appointment_id},
        UpdateExpression="SET #s = :val",
        ExpressionAttributeNames={"#s": "status"},
        ExpressionAttributeValues={":val": "CANCELLED"}
    )
    return "🗑️ Appointment cancelled successfully."

def list_appointments(user_id):
    """List all appointments for a specific user."""
    response = table.scan(FilterExpression=Attr("user_id").eq(user_id))
    return response["Items"]
