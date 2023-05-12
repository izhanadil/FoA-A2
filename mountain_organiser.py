from __future__ import annotations
from typing import List

from mountain import Mountain


class MountainOrganiser:

    def __init__(self) -> None:
        self.mount_ranks = []

    def cur_position(self, mountain: Mountain) -> int:
        """
        Returns the current position of the given mountain object in the mount_ranks list.
        The time complexity of this method is O(n), where n is the length of the mount_ranks list. This is because
        the method iterates over each element in the list and checks if it matches the given mountain object.
        The space complexity of this method is O(1), as it only creates a single integer variable to hold the result.
        """
        for num, rank in enumerate(self.mount_ranks):
            if rank.name == mountain.name:
                return num
        raise KeyError(mountain.name)

    def add_mountains(self, mountains: List[Mountain]) -> None:
        """
        Adds the given list of mountain objects to the mount_ranks list in descending order of length. If two mountains
        have the same length, they are ordered lexicographically by name.
        The time complexity of this method is O(n^2), where n is the length of the given mountains list. This is because
        for each mountain in the given list, the method iterates over all the elements in the mount_ranks list to find
        the correct position to insert it. In the worst case, when all mountains in the given list have to be inserted
        at the beginning of the mount_ranks list, the time complexity is O(n^2). The space complexity of this method is
        O(1), as it only creates a few integer and object variables to hold intermediate results.
        """
        for mountain in mountains:
            if not self.mount_ranks:
                self.mount_ranks.append(mountain)
            else:
                for num, rank in enumerate(self.mount_ranks):
                    if mountain.length > rank.length:
                        if num == len(self.mount_ranks) - 1:
                            self.mount_ranks.append(mountain)
                            break
                    elif mountain.length < rank.length:
                        self.mount_ranks.insert(num, mountain)
                        break
                    else:
                        if mountain.name > rank.name:
                            if num == len(self.mount_ranks) - 1:
                                self.mount_ranks.append(mountain)
                                break
                        else:
                            self.mount_ranks.insert(num, mountain)
                            break

# from __future__ import annotations
# from typing import List

# from mountain import Mountain

# class MountainOrganiser:

#     def _init_(self) -> None:
#         self.mountains = []
    
#     def cur_position(self, mountain: Mountain) -> int:
#         length = mountain.length
#         name = mountain.name
        
#         count = 0
#         for m in self.mountains:
#             if m.length < length or (m.length == length and m.name < name):
#                 count += 1
        
#         if count == len(self.mountains):
#             raise KeyError("Mountain not found")
        
#         return count + 1
    
#     def add_mountains(self, mountains: List[Mountain]) -> None:
#         self.mountains += mountains
#         self.mountains.sort(key=lambda m: (m.length, m.name))





