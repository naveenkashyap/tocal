import datetime
import heapq
import pickle

from typing import List
from pathlib import Path

class TodoItem:
    
    def __init__(self, name: str, priority: float, duration: int=30):
        self.name = name
        self.priority = priority
        self.duration = datetime.timedelta(minutes=duration)
        
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return f"{self.name}: {self.duration}"
        
    def __lt__(self, other):
        return self.priority < other.priority
        
class TodoList:
    
    def __init__(self):
        self.items: List[TodoItem] = []
    
    def add(self, item: TodoItem):
        heapq.heappush(self.items, item)

    def remove(self, idx: int) -> TodoItem:
        return self.items.pop(idx)
    
    def __getitem__(self, idx: int) -> TodoItem:
        return self.items[idx]

    def __len__(self) -> int:
        return len(self.items)
        
    def __repr__(self) -> str:
        return self.__str__()
    
    def __str__(self) -> str:
        ret = "Todo List:"
        for idx, item in enumerate(self.items, 1):
            ret += f'\n[{idx}] {item}'
        return ret

    def save(self, filepath: Path) -> None:
        with open(filepath, 'wb') as f:
            pickle.dump(self.items, f)

    @classmethod
    def load(cls, filepath) -> 'TodoList':
        try:
            with open(filepath, 'rb') as f:
                items = pickle.load(f)
                return TodoList.from_list(items)
        except FileNotFoundError:
            return cls()

    @classmethod
    def from_list(cls, items: List[TodoItem]) -> 'TodoList':
        c = cls()
        c.items = items
        return c

