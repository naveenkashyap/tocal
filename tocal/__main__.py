import datetime
import os

from typing import List

from .service import Service
from .calendar import Calendar, Event

PACKAGE_ROOT: str = os.path.dirname(os.path.abspath(__file__))
SECRETS_PATH: str = os.path.join(
    PACKAGE_ROOT, "secrets", "google", "client_secret.json"
)
CREDS_PATH: str = os.path.join(PACKAGE_ROOT, "creds", "google", "creds.pickle")

SCOPES: List[str] = ["https://www.googleapis.com/auth/calendar.events"]


def main():
    service = Service(
        creds_path=CREDS_PATH,
        secrets_path=SECRETS_PATH,
        scopes=SCOPES,
        service_name="calendar",
        service_version="v3",
    ).service

    # Define the start and end times of the current day
    #   start = now
    #   end = midnight
    now = datetime.datetime.now()
    tomorrow = now + datetime.timedelta(days=1)
    tomorrow = tomorrow.replace(hour=0, minute=0, second=0, microsecond=0)
    day_length = tomorrow - now

    now = datetime.datetime.utcnow()
    tomorrow = now + day_length
    now = now.isoformat() + "Z"
    tomorrow = tomorrow.isoformat() + "Z"

    # Call the Calendar API
    print("Getting your events for the rest of the day")

    events_result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=now,
            timeMax=tomorrow,
            maxResults=10,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    owner = events_result.get("summary", "unknown")
    events = events_result.get("items", [])

    cal = Calendar(owner)
    if not events:
        print("No upcoming events found.")
    for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        end = event["end"].get("dateTime", event["end"].get("date"))
        start_datetime = datetime.datetime.fromisoformat(start)
        end_datetime = datetime.datetime.fromisoformat(end)
        duration = end_datetime - start_datetime
        event = Event(duration.total_seconds(), event)
        cal.add_event(event)

