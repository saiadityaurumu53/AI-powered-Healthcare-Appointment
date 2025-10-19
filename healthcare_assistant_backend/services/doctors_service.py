# services/doctors_service.py

import boto3
from boto3.dynamodb.conditions import Key
import os

# Initialize DynamoDB client
dynamodb = boto3.resource(
    "dynamodb",
    region_name=os.getenv("AWS_REGION", "us-east-1")
)

DOCTORS_TABLE = os.getenv("DOCTORS_TABLE", "Doctors")
table = dynamodb.Table(DOCTORS_TABLE)


def get_all_doctors():
    """Fetch all doctors from DynamoDB."""
    try:
        response = table.scan()
        items = response.get("Items", [])
        items.sort(key=lambda x: x.get("doctor_name", ""))
        return items
    except Exception as e:
        raise Exception(f"Error fetching doctors: {str(e)}")


def get_doctor_by_id(doctor_id: str):
    """Fetch a single doctor by ID."""
    try:
        response = table.get_item(Key={"doctor_id": doctor_id})
        return response.get("Item")
    except Exception as e:
        raise Exception(f"Error fetching doctor {doctor_id}: {str(e)}")
