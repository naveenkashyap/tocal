import datetime
import heapq

from typing import List

class TodoItem:
    
    def __init__(self, name: str, priority: float, *, duration: datetime.timedelta=datetime.timedelta(minutes=30)):
        self.name = name
        self.priority = priority
        self.duration = duration
        
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
    
    def __getitem__(self, idx):
        return self.items[idx]
        
    def __repr__(self):
        return self.__str__()
    
    def __str__(self):
        ret = "Todo List: \n\n"
        ret += '\n'.join(str(item) for item in self.items)
        return ret
    