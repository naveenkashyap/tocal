import heapq

from typing import NamedTuple


class Event(NamedTuple):
    duration: float
    details: dict
    age: int = 1
    priority: float = 3.0


class Calendar:
    def __init__(self, owner: str):
        self.owner = owner
        self.events = []

    def add_event(self, event: Event):
        heapq.heappush(self.events, ((event.priority, event)))

    def __str__(self):
        res = ""
        for priority, event in self.events:
            res += f"{event.details['summary']}"
        return res
