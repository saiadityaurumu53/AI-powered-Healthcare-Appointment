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
# CONVERSATIONAL_MODEL_ID = "amazon.titan-text-lite-v1"
CONVERSATIONAL_MODEL_ID = FALLBACK_MODEL_ID


def extract_intent(user_text: str):
    """
    Extracts structured appointment intent using Amazon Bedrock Claude models.
    Falls back to general conversation handling if no clear intent detected.
    """
    system_prompt = (
        "You are an AI Healthcare Appointment Assistant.\n"
        "Understand user requests about booking, cancelling, or checking doctor appointments.\n"
        "Always respond ONLY with JSON in this exact format:\n"
        '{"intent": "book_appointment", "doctor": "Dr. Lee", "date": "2025-10-13", "time": "10:00 AM"}\n'
        "If information is missing, leave fields blank (e.g., 'date': '')."
    )

    payload = {
        "anthropic_version": "bedrock-2023-05-31",
        "system": system_prompt,
        "max_tokens": 512,
        "temperature": 0.3,
        "messages": [{"role": "user", "content": [{"type": "text", "text": user_text}]}],
    }

    def invoke_model(model_id):
        response = client.invoke_model(
            modelId=model_id,
            body=json.dumps(payload),
            contentType="application/json",
            accept="application/json",
        )
        result = json.loads(response["body"].read())
        return result["content"][0]["text"]

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

    # Try to parse JSON intent
    try:
        parsed = json.loads(output_text)
    except json.JSONDecodeError:
        parsed = {"intent": "unknown", "raw_text": output_text}

    # 🧩 Step 3 — If intent is unknown, use conversational fallback
    if parsed.get("intent") == "unknown" or parsed.get("intent") == "":
        try:
            print(f"💬 Invoking conversational model: {CONVERSATIONAL_MODEL_ID}")
            conv_payload = {
                "inputText": f"You are a friendly healthcare assistant. Respond conversationally to: {user_text}",
                "textGenerationConfig": {"maxTokenCount": 300, "temperature": 0.8}
            }
            conv_response = client.invoke_model(
                modelId=CONVERSATIONAL_MODEL_ID,
                body=json.dumps(conv_payload),
                contentType="application/json",
                accept="application/json",
            )
            conv_output = json.loads(conv_response["body"].read())
            reply_text = conv_output.get("results", [{}])[0].get("outputText", "I'm here to help.")
            parsed = {"intent": "conversation", "reply": reply_text}
        except Exception as e:
            parsed = {"intent": "unknown", "reply": f"Sorry, I couldn’t respond: {str(e)}"}

    return parsed
