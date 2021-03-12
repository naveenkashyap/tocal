from typing import List

from tocal.event import TodoEvent, GoogleEvent 
from tocal.calendar import Calendar
from tocal.service import GoogleService
from tocal.todo import TodoItem, TodoList

import datetime
import os
import json

package_root: str = os.path.join('/', 'Users', 'naveen', 'dev', 'tocal', 'tocal')
SECRETS_PATH: str = os.path.join(package_root, 'secrets', 'google', 'client_secret.json')
CREDS_PATH: str = os.path.join(package_root, 'creds', 'google', 'creds.pickle')
SCOPES: List[str] = ['https://www.googleapis.com/auth/calendar.events', 'https://www.googleapis.com/auth/calendar']
service_name = 'calendar'
service_version = 'v3'

def main():
    now = datetime.datetime.now()
    tomorrow = now + datetime.timedelta(days=1)
    midnight = tomorrow.replace(hour=0, minute=0, second=0, microsecond=0)

    now = now.astimezone(datetime.timezone.utc)
    midnight = midnight.astimezone(datetime.timezone.utc)

    now = now.isoformat()
    midnight = midnight.isoformat()
    service = GoogleService(
        creds_path=CREDS_PATH,
        secrets_path=SECRETS_PATH,
        scopes=SCOPES,
        service_name=service_name,
        service_version=service_version,
    ).service

    freebusy_result = service.freebusy().query(
        body={
            "items": [ 
                {
                "id": "primary", 
                },
            ],
            "timeMin": now,
            "timeMax": midnight,
        }
    ).execute()

    events_result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=now,
            timeMax=midnight,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )

    timezone = events_result.get('timeZone')
    owner = events_result.get("summary", "unknown")
    events = events_result.get("items", [])
    cal = Calendar(owner, tz=timezone)

    if not events:
        print("No upcoming events found.")
    for event in events:
        event = GoogleEvent(event)
        cal.add(event)

    todo_list = TodoList()
    todo_list.add(TodoItem(name='PRs', priority=4))
    todo_list.add(TodoItem(name='Column Detection', priority=2))
    todo_list.add(TodoItem(name='BofA - localize classifier', priority=1))
    todo_list.add(TodoItem(name='BofA - investigate HLFM classifier changes', priority=2))

    for item in todo_list:
        for start, end in cal.free_time:
            free_time = end - start
            if (free_time / item.duration) >= 1:
                event = TodoEvent(item.name, start, start + item.duration, False, item)
                cal.add(event)
                break
        else:
            print(f'Cannot find time for {item}')

    for event in cal:
        if not isinstance(event, TodoEvent):
            continue
        body = {
            'description': json.dumps({
                'creation': event.creation.isoformat(),
                'priority': event.todo_item.priority
            }),
            'end': {
                'dateTime': event.end.isoformat(),
                'timeZone': str(cal.tz),
            },
            'start': {
                'dateTime': event.start.isoformat(),
                'timeZone': str(cal.tz),
            },
            'source': {
                'title': 'ToCal',
                'url': 'http://www.instabase.com',
            },
            'summary': event.name,
            'visibility': 'private'
        }
        service.events().insert(
            calendarId='primary',
            body=body,
        ).execute()
        print(f'uploaded {event}')
        