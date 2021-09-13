import datetime
import click
import json

from .util import CREDS_PATH, SCOPES, SECRETS_PATH, SERVICE_NAME, SERVICE_VERSION, TODOLIST_FILEPATH
from ..clients.todo import TodoList
from ..clients.calendar import Calendar
from ..clients.event import GoogleEvent, TodoEvent
from ..clients.service import GoogleService, Service

cal: Calendar
service: Service

@click.group()
def calendar():
    global cal
    global service

    service = GoogleService(
        creds_path=CREDS_PATH,
        secrets_path=SECRETS_PATH,
        scopes=SCOPES,
        service_name=SERVICE_NAME,
        service_version=SERVICE_VERSION,
    ).service

    now = datetime.datetime.now()
    tomorrow = now + datetime.timedelta(days=1)
    midnight = tomorrow.replace(hour=0, minute=0, second=0, microsecond=0)

    now = now.astimezone(datetime.timezone.utc)
    midnight = midnight.astimezone(datetime.timezone.utc)

    now = now.isoformat()
    midnight = midnight.isoformat()

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
    for event in events:
        event = GoogleEvent(event)
        cal.add(event)

@calendar.command()
def show():
    click.echo(cal)

@calendar.command()
def sync():
    """ Attempts to add todo items to today's calendar """

    # get todo list and add them to local calendar, if there's time
    todo_list = TodoList.load(TODOLIST_FILEPATH)
    for item in todo_list:
        for start, end in cal.free_time:
            free_time = end - start
            if (free_time / item.duration) >= 1:
                event = TodoEvent(item.name, start, start + item.duration, False, item)
                cal.add(event)
                break
        else:
            click.echo(f'Cannot find time for {item}')

    # synchronize local calendar with remote calendar
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