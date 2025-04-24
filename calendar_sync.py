import datetime
import os
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Define the calendar API scope
SCOPES = ['https://www.googleapis.com/auth/calendar']

# Get authorized Google Calendar service
def get_calendar_service():
    creds = None
    token_path = 'token.pickle'
    credentials_path = 'credentials.json'  # Download this from Google Developer Console

    # Load existing token if available
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)

    # If credentials are invalid or missing, re-auth
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)

    return build('calendar', 'v3', credentials=creds)

# Sync event to Google Calendar
def sync_event(start_iso, end_iso, summary="Meeting Follow-up"):
    try:
        service = get_calendar_service()
        event = {
            'summary': summary,
            'start': {'dateTime': start_iso, 'timeZone': 'America/Los_Angeles'},
            'end': {'dateTime': end_iso, 'timeZone': 'America/Los_Angeles'},
        }

        event_result = service.events().insert(calendarId='primary', body=event).execute()
        print(f"🗓️ Event created: {event_result.get('htmlLink')}")
    except Exception as e:
        print(f"❌ Failed to sync event: {e}")
