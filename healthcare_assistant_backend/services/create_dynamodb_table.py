import boto3
import time

# Initialize DynamoDB client
dynamo = boto3.client("dynamodb", region_name="us-east-1")

table_name = "Appointments"

try:
    # Create the table
    response = dynamo.create_table(
        TableName=table_name,
        KeySchema=[
            {"AttributeName": "appointment_id", "KeyType": "HASH"},  # Primary Key
        ],
        AttributeDefinitions=[
            {"AttributeName": "appointment_id", "AttributeType": "S"},
            {"AttributeName": "user_id", "AttributeType": "S"},
        ],
        GlobalSecondaryIndexes=[
            {
                "IndexName": "user_id-index",
                "KeySchema": [{"AttributeName": "user_id", "KeyType": "HASH"}],
                "Projection": {"ProjectionType": "ALL"},
                "ProvisionedThroughput": {"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
            }
        ],
        ProvisionedThroughput={
            "ReadCapacityUnits": 5,
            "WriteCapacityUnits": 5
        }
    )

    print("🚀 Creating table 'Appointments'... please wait ~30s")
    # Wait until table is active
    waiter = dynamo.get_waiter('table_exists')
    waiter.wait(TableName=table_name)
    print("DynamoDB table 'Appointments' created successfully!")

except dynamo.exceptions.ResourceInUseException:
    print("Table 'Appointments' already exists.")
