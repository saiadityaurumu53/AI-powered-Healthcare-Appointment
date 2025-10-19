# services/sns_service.py
import boto3
import os
topic_arn = os.getenv("SNS_TOPIC_ARN")
sns_client = boto3.client("sns", region_name=os.getenv("AWS_REGION", "us-east-1"))

def send_sms_notification(phone_number: str, message: str):
    """Send an SMS message using AWS SNS."""
    try:
        response = sns_client.publish(
            PhoneNumber=phone_number,
            Message=message
        )
        return {"status": "success", "message_id": response["MessageId"]}
    except Exception as e:
        raise Exception(f"Failed to send SMS: {str(e)}")


def send_email_notification(topic_arn: str, subject: str, message: str):
    """Send an email via an SNS topic."""
    try:
        response = sns_client.publish(
            TopicArn=topic_arn,
            Subject=subject,
            Message=message
        )
        return {"status": "success", "message_id": response["MessageId"]}
    except Exception as e:
        raise Exception(f"Failed to send email: {str(e)}")
