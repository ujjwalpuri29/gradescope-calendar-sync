import os
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from googleapiclient.discovery import build
from datetime import datetime, timedelta

from google_utils import get_flow, save_credentials, load_credentials, event_exists, TIMEZONE
from gradescope_utils import get_assignments

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1' # Only for localhost (remove in prod)

app = FastAPI()

@app.get("/")
async def home():
    return HTMLResponse(F"""
    <body style="font-family:sans-serif;text-align:center;margin-top:50px;">
        <h1 style="text-align:center;margin:auto">Gradescope sync for Google Calendar</h1>
        <a href="/sync" style="display:inline-block;margin-top:20px;
            padding:10px 20px;background:#4285F4;color:white;
            text-decoration:none;border-radius:5px;">Sync Now
        </a>
    </body>
    """
    )

@app.get("/auth")
async def auth_google():
    flow = get_flow()
    auth_url, _ = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        prompt="consent",
    )
    return RedirectResponse(auth_url)

@app.get("/oauth2callback")
async def oauth2callback(request: Request):
    flow = get_flow()
    flow.fetch_token(authorization_response=str(request.url))
    creds = flow.credentials
    save_credentials(creds)
    return RedirectResponse("/sync")

@app.get("/sync")
async def gradescope_sync():
    creds = load_credentials()
    if not creds:
        return RedirectResponse("/auth")
    
    service = service = build("calendar", "v3", credentials=creds)
    
    assignments = get_assignments()
    created_events = []
    
    for a in assignments:
        if not a["due"]:
            continue
        range_start = datetime.fromisoformat(a["due"])
        range_end = range_start + timedelta(hours=1)
        if event_exists(service, "primary", a["title"], range_start, range_end):
            continue
        
        event = {
            "summary": a["title"],
            "description": "Imported from Gradescope",
            "start": {
                "dateTime": a["due"],
                "timeZone": TIMEZONE,
            },
            "end": {
                "dateTime": a["due"],
                "timeZone": TIMEZONE,
            },
            "reminders": {
                "useDefault": False,
                "overrides": [
                    {"method": "popup", "minutes": 900}, 
                    {"method": "popup", "minutes": 2340},
                ],
            },
        }
        created = service.events().insert(calendarId="primary", body=event).execute()
        created_events.append(
            f"<li><a href='{created.get('htmlLink')}' target='_blank'>{a['title']}</a> (due {a['due'][:10]} {a['due'][11:16]})</li>"
        )
        
    # print(created_events)

    if not created_events:
        return HTMLResponse("""
        <h2 style="font-family:sans-serif;text-align:center;margin-top:50px;">
            No new events created (all assignments already synced)
        </h2>
        """
        )
        
    return HTMLResponse(f"""
    <html>
    <head><title>Sync Complete</title></head>
    <body style="font-family:sans-serif;text-align:center;margin-top:50px;">
        <h1>✅ Gradescope Deadlines Synced</h1>
        <ul style="list-style:none;padding:0;">
            {''.join(created_events)}
        </ul>
        <a href="/" style="display:inline-block;margin-top:20px;
            padding:10px 20px;background:#4285F4;color:white;
            text-decoration:none;border-radius:5px;">Back to Home</a>
    </body>
    </html>
    """
    )
