import json
from botocore.exceptions import ClientError
import boto3, os
from dotenv import load_dotenv
load_dotenv()



# Initialize Bedrock Runtime client (ensure your region matches)
client = boto3.client("bedrock-runtime", region_name=os.getenv("AWS_REGION", "us-east-1"))

# ✅ Primary and fallback models (you have on-demand access to both)
PRIMARY_MODEL_ID = "anthropic.claude-3-5-sonnet-20240620-v1:0"
FALLBACK_MODEL_ID = "anthropic.claude-3-haiku-20240307-v1:0"


def extract_intent(user_text: str):
    """
    Extracts structured appointment intent using Amazon Bedrock Claude models.
    The model will understand booking, cancellation, and schedule inquiries,
    and return structured JSON.
    """

    system_prompt = (
        "You are an AI Healthcare Appointment Assistant.\n"
        "Understand user requests about booking, cancelling, or checking doctor appointments.\n"
        "Always respond ONLY with JSON in this exact format:\n"
        '{"intent": "book_appointment", "doctor": "Dr. Lee", "date": "2025-10-13", "time": "10:00 AM"}\n'
        "If information is missing, leave fields blank (e.g., 'date': '')."
    )

    # ✅ Construct Anthropic-compliant payload
    payload = {
        "anthropic_version": "bedrock-2023-05-31",
        "system": system_prompt,
        "max_tokens": 512,
        "temperature": 0.3,
        "messages": [
            {
                "role": "user",
                "content": [{"type": "text", "text": user_text}],
            }
        ],
    }

    # 🧠 Internal function to call Bedrock safely
    def invoke_model(model_id):
        response = client.invoke_model(
            modelId=model_id,
            body=json.dumps(payload),
            contentType="application/json",
            accept="application/json",
        )
        result = json.loads(response["body"].read())
        return result["content"][0]["text"]

    # ✅ Try Claude 3.5 Sonnet first, fallback to Haiku if needed
    try:
        print(f"🟢 Invoking primary model: {PRIMARY_MODEL_ID}")
        output_text = invoke_model(PRIMARY_MODEL_ID)
    except ClientError as e:
        error_message = str(e)
        print(f"⚠️ Primary model failed: {error_message}")
        if "AccessDenied" in error_message or "Throttling" in error_message:
            print(f"🟡 Falling back to {FALLBACK_MODEL_ID} ...")
            output_text = invoke_model(FALLBACK_MODEL_ID)
        else:
            raise

    # ✅ Try to parse model’s response as JSON
    try:
        parsed = json.loads(output_text)
    except json.JSONDecodeError:
        parsed = {"intent": "unknown", "raw_text": output_text}

    return parsed
