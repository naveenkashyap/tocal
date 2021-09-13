from abc import abstractproperty
from typing import Iterable, Tuple

from .event import Event

import heapq
import datetime
import pytz
class Calendar:
        
    def __init__(self, owner: str, tz: str='UTC'):
        self.owner = owner
        self.tz = pytz.timezone(tz)
        self.events = []
        
    def add(self, event: Event):
        if not event.is_allday:
            heapq.heappush(self.events, event)
            
    def __getitem__(self, idx):
        return self.events[idx]
            
    @property
    def now(self) -> datetime.datetime:
        '''Return current datetime in Calendar timezone'''
        return datetime.datetime.now(tz=self.tz)
    
    @property
    def midnight(self) -> datetime.datetime:
        '''Return midnight in Calendar timezone'''
        tomorrow = self.now + datetime.timedelta(days=1)
        return tomorrow.replace(hour=0, minute=0, second=0, microsecond=0)
        
    @property
    def free_time(self) -> Iterable[Tuple[datetime.datetime, datetime.datetime]]:
        start = self.now
        for event in self.events:
            end = event.start
            if start < end:
                yield start, end
            start = event.end
        end = self.midnight
        yield start, end
        
    def __repr__(self):
        return self.__str__()
    
    def __str__(self):
        ret = f"Calendar:"
        for event in self.events:
            ret += f'\n{event}'
        return ret