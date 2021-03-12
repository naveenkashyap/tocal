from abc import ABC

from tocal.todo import TodoItem

import datetime

class Event(ABC):
    
    def __init__(self, name: str, start: datetime.datetime, end: datetime.datetime, is_allday: bool):
        self.name = name
        self.start = start
        self.end = end
        self.is_allday = is_allday
        self.creation = datetime.datetime.utcnow()
        
    def __str__(self):
        return self.name
    
    def __repr__(self):
        start = self.start.strftime('%I:%M%p')
        end = self.end.strftime('%I:%M%p')
        return f'{self.name}: {start}-{end}'
    
    def __lt__(self, other):
        return self.start < other.start
        
class TodoEvent(Event):
    
    def __init__(self, name: str, start: datetime.datetime, end: datetime.datetime, is_allday: bool, todo_item: TodoItem):
        super().__init__(name, start, end, is_allday)
        self.todo_item = todo_item
    
class GoogleEvent(Event):
    
    def __init__(self, details: dict): 
        
        is_allday = True if details['start'].get("date") else False
        if is_allday:
            start = details['start'].get('date')
            end = details['end'].get('date')
        else:
            start = details['start'].get('dateTime')
            end = details['end'].get('dateTime')

        start = datetime.datetime.fromisoformat(start)
        end = datetime.datetime.fromisoformat(end)
        name = details['summary']
        
        super().__init__(name, start, end, is_allday)
        
        self.details = details
    
    def __lt__(self, other):
        if self.is_allday:
            return True
        if other.is_allday:
            return False
        return self.start < other.start

