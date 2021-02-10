import datetime
import pickle
import os
import logging

from typing import List

from googleapiclient.discovery import build  # type: ignore
from google_auth_oauthlib.flow import InstalledAppFlow # type: ignore
from google.auth.transport.requests import Request # type: ignore
from google.oauth2.credentials import Credentials # type: ignore 


PACKAGE_ROOT: str = os.path.dirname(os.path.abspath(__file__))
SECRETS_PATH: str = os.path.join(PACKAGE_ROOT, 'secrets', 'google', 'client_secret.json')
CREDS_PATH: str = os.path.join(PACKAGE_ROOT, 'creds', 'google', 'creds.pickle')

SCOPES: List[str] = ['https://www.googleapis.com/auth/calendar.events']

def get_creds() -> Credentials:
    creds = None
    if os.path.exists(CREDS_PATH):
        with open(CREDS_PATH, 'rb') as f:
            creds =  pickle.load(f)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(SECRETS_PATH, scopes=SCOPES)
            creds = flow.run_local_server()
        with open(CREDS_PATH, 'wb') as f:
            pickle.dump(creds, f)
    
    return creds

def main():
    creds = get_creds()
    service = build('calendar', 'v3', credentials=creds)

    # Define the start and end times of the current day
    #   start = now
    #   end = midnight
    now = datetime.datetime.now()
    tomorrow = now + datetime.timedelta(days=1)
    tomorrow = tomorrow.replace(hour=0, minute=0, second=0, microsecond=0)
    day_length = tomorrow - now

    now = datetime.datetime.utcnow()
    tomorrow = now + day_length
    now = now.isoformat() + 'Z'
    tomorrow = tomorrow.isoformat() + 'Z'

    # Call the Calendar API
    print('Getting your events for the rest of the day')

    events_result = service.events().list(calendarId='primary', timeMin=now, timeMax=tomorrow,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])


