import boto3
import csv
from decimal import Decimal
import json

# Initialize DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

def load_csv_to_dynamo(table_name, file_path, key_columns):
    """
    Uploads CSV data to DynamoDB.
    Args:
        table_name: str -> DynamoDB table name
        file_path: str -> Path to the CSV file
        key_columns: list -> Column names to ensure uniqueness
    """
    table = dynamodb.Table(table_name)

    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        count = 0
        for row in reader:
            # Convert empty strings to None
            item = {k: (v if v != '' else None) for k, v in row.items()}

            # Convert numeric strings to Decimal if needed
            for k, v in item.items():
                try:
                    if v and v.replace('.', '', 1).isdigit():
                        item[k] = Decimal(v)
                except Exception:
                    pass

            # Put item into DynamoDB
            table.put_item(Item=item)
            count += 1
            if count % 10 == 0:
                print(f"Uploaded {count} records to {table_name}")

        print(f"✅ Upload complete: {count} records added to {table_name}")

# Run for all your files
load_csv_to_dynamo("Doctors", "Doctors.csv", ["doctor_id"])
load_csv_to_dynamo("DoctorAvailability", "DoctorAvailability_2Months.csv", ["doctor_id", "date"])
load_csv_to_dynamo("PatientAppointments", "PatientAppointments.csv", ["appointment_id"])
