import datetime
import pickle
import os
from googleapiclient.discovery import build  # type: ignore
from google_auth_oauthlib.flow import InstalledAppFlow # type: ignore
from google.auth.transport.requests import Request # type: ignore
from google.oauth2.credentials import Credentials # type: ignore 

from typing import List

PACKAGE_ROOT: str = os.path.dirname(os.path.abspath(__file__))
SECRETS_PATH: str = os.path.join(PACKAGE_ROOT, 'secrets', 'google', 'client_secret.json')
CREDS_PATH: str = os.path.join(PACKAGE_ROOT, 'creds', 'google', 'creds.pickle')

SCOPES: List[str] = ['https://www.googleapis.com/auth/calendar.events']

def get_creds(flow: InstalledAppFlow) -> Credentials:
    creds = None
    if os.path.exists(CREDS_PATH):
        with open(CREDS_PATH, 'rb') as f:
            creds =  pickle.load(f)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            creds = flow.run_local_server()
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

def main():
    flow = InstalledAppFlow.from_client_secrets_file(
        SECRETS_PATH, scopes=SCOPES
    )

    creds = get_creds(flow)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])


