import os
import pickle
from dotenv import load_dotenv
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Load environment variables from .env file
load_dotenv()

# Define the scopes required for Google Calendar API
SCOPES = ['https://www.googleapis.com/auth/calendar.events']

def get_google_credentials():
    creds = None

    # Load the existing token if it exists
    if os.path.exists('token.json'):
        with open('token.json', 'rb') as token_file:
            creds = pickle.load(token_file)

    # If no token exists or token is invalid, start the authentication process
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())  # Refresh the token if expired
        else:
            # Create an OAuth flow using the client secret file
            flow = InstalledAppFlow.from_client_secrets_file('config/credentials.json', SCOPES)
            # This will open a browser window to authenticate and get the authorization code
            creds = flow.run_local_server(port=0)  # Using run_local_server for better user experience

        # Save the new token to 'token.json' for future use
        with open('token.json', 'wb') as token_file:
            pickle.dump(creds, token_file)

    return creds

# Test the function to make sure everything works
if __name__ == '__main__':
    credentials = get_google_credentials()
    print("Google credentials are successfully acquired:", credentials)
