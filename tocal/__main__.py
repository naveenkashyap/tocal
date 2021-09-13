from typing import List
from pathlib import Path

from .clients.event import TodoEvent, GoogleEvent 
from .clients.calendar import Calendar
from .clients.service import GoogleService

from .commands.todo import todo as todo_commands
from .commands.calendar import calendar as calendar_commands

import datetime
import json
import click

@click.group()
def cli():
    pass

cli.add_command(todo_commands)
cli.add_command(calendar_commands)
