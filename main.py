import os

from fastapi import FastAPI, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.responses import RedirectResponse
import boto3
from pydantic import BaseModel
from fastapi import Body, HTTPException
import uvicorn

# Replace placeholders with your actual values
LEX_REGION_NAME = "eu-central-1"
LEX_BOT_ID = "18HYOHEXKA"
LEX_BOT_ALIAS_ID = "TSTALIASID"


app = FastAPI(
    title="Service Desk Chatbot",
    description="Service Desk Chatbot"
)

bearer_scheme = HTTPBearer()
BEARER_TOKEN = "1234" #os.environ.get("BEARER_TOKEN")
assert BEARER_TOKEN is not None


def validate_token(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    if credentials.scheme != "Bearer" or credentials.credentials != BEARER_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid or missing token")
    return credentials


app = FastAPI(dependencies=[Depends(validate_token)])


class Item(BaseModel):
    sessionId: str
    text: str

# auxiliary requests for framework purposes following...
# redirect root requests to the docs
@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")

@app.post("/")
def root(item: Item):
    """Sends user text to Amazon Lexv2 for processing."""

    try:
        
        client = session.client('lexv2-runtime', region_name=LEX_REGION_NAME)

        # Send the text to Lex for processing
        response = client.recognize_text(
            botId=LEX_BOT_ID,
            botAliasId=LEX_BOT_ALIAS_ID,
            localeId="en_US",  # Consider making this dynamic based on user input
            sessionId=item.sessionId,
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

def main():
    # noinspection PyTypeChecker
    port = 8000
    print(f"Starting application, once loaded, access at 3.122.241.50/:{port}")
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()

