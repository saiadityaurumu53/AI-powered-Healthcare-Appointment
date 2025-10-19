# Use the Conversation API to send a text message to Amazon Nova.

import boto3
from botocore.exceptions import ClientError


def execute_func():
    # Create a Bedrock Runtime client in the AWS Region you want to use.
    client = boto3.client("bedrock-runtime", region_name="us-east-1")

    # Set the model ID, e.g., Amazon Nova Lite.
    model_id = "anthropic.claude-3-haiku-20240307-v1:0"

    # Start a conversation with the user message.
    user_message = "Describe the purpose of a 'hello world' program in one line."
    conversation = [
        {
            "role": "user",
            "content": [{"text": user_message}],
        }
    ]

    try:
        # Send the message to the model, using a basic inference configuration.
        response = client.converse(
            modelId=model_id,
            messages=conversation,
            inferenceConfig={"maxTokens": 512, "temperature": 0.5, "topP": 0.9},
        )

        # Extract and print the response text.
        response_text = response["output"]["message"]["content"][0]["text"]
        print(response_text)

    except (ClientError, Exception) as e:
        print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
        exit(1)

if __name__ == "__main__":
    execute_func()


