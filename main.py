from fastapi import FastAPI
import boto3
from pydantic import BaseModel

app = FastAPI()
# Replace placeholders with your actual values
LEX_PROFILE_NAME = "prod@account-admin"
LEX_REGION_NAME = "eu-central-1"
LEX_BOT_ID = "18HYOHEXKA"
LEX_BOT_ALIAS_ID = "TSTALIASID"
LEX_SESSION_ID = "100"


class Item(BaseModel):
    sessionId: str
    text: str

@app.get("/")
def root():
    """Returns a welcome message."""

    return {"message": "Welcome to the Amazon Lexv2 API!"}

@app.post("/")
def root(item: Item):
    """Sends user text to Amazon Lexv2 for processing."""

    try:
        # Create a boto3 session with the specified profile

        # Create Lexv2 client
        client = boto3.client('lexv2-runtime', region_name=LEX_REGION_NAME)

        # Send the text to Lexv2 for processing
        response = client.recognize_text(
            botId=LEX_BOT_ID,
            botAliasId=LEX_BOT_ALIAS_ID,
            localeId="en_US",  # Consider making this dynamic based on user input
            sessionId=LEX_SESSION_ID,
            text=item.text
        )


        # Handle potential errors gracefully
        if "errorMessage" in response:
            return {"error": response["errorMessage"]}

        return response

    except Exception as e:
        # Log the error for deeper troubleshooting
        print(f"An error occurred: {e}")
        return {"error": "Internal server error"}
