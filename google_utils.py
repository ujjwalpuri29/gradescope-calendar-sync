import os
from dotenv import load_dotenv
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/calendar"]
GOOGLE_CLIENT_SECRETS_FILE = os.getenv("GOOGLE_CLIENT_SECRETS_FILE")
REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")
TIMEZONE = os.getenv("TIMEZONE", "UTC")

def save_credentials(creds: Credentials):
    with open("token.json", "w") as token:
        token.write(creds.to_json())
    
def load_credentials():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            save_credentials(creds)
    
    return creds

def get_flow():
    return Flow.from_client_secrets_file(
        GOOGLE_CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )
    
def event_exists(service, calendar_id, summary, start_time, end_time):
    events_result = service.events().list(
        calendarId=calendar_id,
        timeMin=start_time.isoformat(),
        timeMax=end_time.isoformat(),
        singleEvents=True,
        orderBy="startTime"
    ).execute()

    events = events_result.get("items", [])
    for event in events:
        if event.get("summary") == summary:
            return True
    return False