from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, HTMLResponse
import os
from dotenv import load_dotenv
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1' # remove in prod

load_dotenv()

app = FastAPI()

GOOGLE_CLIENT_SECRETS_FILE = os.getenv("GOOGLE_CLIENT_SECRETS_FILE")
SCOPES = ["https://www.googleapis.com/auth/calendar"]
REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")

def load_credentials():
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            with open("token.json", "w") as token:
                token.write(creds.to_json())

        return creds
    return None

@app.get("/")
def home():
    return HTMLResponse("""
    <h1>Google Calendar OAuth Demo</h1>
    <a href="/auth">Authorize with Google</a>
    """)

@app.get("/auth")
def auth_google():
    flow = Flow.from_client_secrets_file(
        GOOGLE_CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )
    auth_url, _ = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        prompt="consent"
    )
    return RedirectResponse(auth_url)

@app.get("/oauth2callback")
def oauth2callback(request: Request):
    flow = Flow.from_client_secrets_file(
        GOOGLE_CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )

    flow.fetch_token(authorization_response=str(request.url))

    creds = flow.credentials
    with open("token.json", "w") as token:
        token.write(creds.to_json())

    return {"message": "Authorization complete."}

@app.get("/add_event")
def add_event():
    creds = load_credentials()
    if not creds:
        return {"error": "Not authorized."}
    
    service = build("calendar", "v3", credentials=creds)

    event = {
        "summary": "Test Assignment",
        "description": "Created via FastAPI with .env config",
        "start": {
            "dateTime": "2025-09-16T20:00:00-07:00",
            "timeZone": "America/Los_Angeles",
        },
        "end": {
            "dateTime": "2025-09-16T21:00:00-07:00",
            "timeZone": "America/Los_Angeles",
        },
    }

    created_event = service.events().insert(calendarId="primary", body=event).execute()
    return {"event_link": created_event.get("htmlLink")}