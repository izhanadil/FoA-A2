# from __future__ import annotations

# from mountain import Mountain

# class MountainOrganiser:

#     def __init__(self) -> None:
#         raise NotImplementedError()

#     def cur_position(self, mountain: Mountain) -> int:
#         raise NotImplementedError()

#     def add_mountains(self, mountains: list[Mountain]) -> None:
#         raise NotImplementedError()
from __future__ import annotations
from typing import List

from mountain import Mountain

class MountainOrganiser:

    def _init_(self) -> None:
        self.mountains = []
    
    def cur_position(self, mountain: Mountain) -> int:
        length = mountain.length
        name = mountain.name
        
        count = 0
        for m in self.mountains:
            if m.length < length or (m.length == length and m.name < name):
                count += 1
        
        if count == len(self.mountains):
            raise KeyError("Mountain not found")
        
        return count + 1
    
    def add_mountains(self, mountains: List[Mountain]) -> None:
        self.mountains += mountains
        self.mountains.sort(key=lambda m: (m.length, m.name))