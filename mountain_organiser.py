# from __future__ import annotations

# from mountain import Mountain

# class MountainOrganiser:

#     def __init__(self) -> None:
#         raise NotImplementedError()

#     def cur_position(self, mountain: Mountain) -> int:
#         raise NotImplementedError()

#     def add_mountains(self, mountains: list[Mountain]) -> None:
#         raise NotImplementedError()


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



# from __future__ import annotations

# from double_key_table import DoubleKeyTable
# from infinite_hash_table import InfiniteHashTable
# from mountain import Mountain

# class MountainOrganiser:
#     def __init__(self) -> None:
#         # Initialize two tables to store the mountains by their length and name.
#         # We use a DoubleKeyTable to allow fast access by both keys.
#         # We use an InfiniteHashTable for O(1) insertion.
#         self.length_table = DoubleKeyTable()
#         self.name_table = DoubleKeyTable()
#         self.mountains = InfiniteHashTable()

#     def add_mountains(self, mountains: list[Mountain]) -> None:
#         # Insert the mountains into the two tables, and keep track of their order.
#         for mountain in mountains:
#             index = len(self.mountains)
#             self.length_table[(mountain.length, index)] = mountain
#             self.name_table[(mountain.name, index)] = mountain
#             self.mountains[index] = mountain

#     def cur_position(self, mountain: Mountain) -> int:
#         # Look up the mountain in the name table to get its index.
#         try:
#             _, index = self.name_table[mountain.name]
#         except KeyError:
#             raise KeyError(f"Mountain '{mountain.name}' has not been added.")
#         # Count the number of mountains that are shorter or have the same length,
#         # and the number of mountains that have the same length but come before
#         # the given mountain lexicographically.
#         count_length = 0
#         count_name = 0
#         for key in self.length_table.keys():
#             if key[0] < mountain.length:
#                 count_length += 1
#             elif key[0] == mountain.length and key[1] < index:
#                 count_length += 1
#         for key in self.name_table.keys():
#             if key[0] < mountain.name:
#                 count_name += 1
#             elif key[0] == mountain.name and key[1] < index:
#                 count_name += 1
#         # The mountain's rank is the number of mountains shorter or with the same
#         # length, plus the number of mountains with the same length that come
#         # before it lexicographically, plus one (to account for the mountain itself).
#         return count_length + count_name + 1


# from _future_ import annotations

# from mountain import Mountain

# class MountainOrganiser:

#     def _init_(self) -> None:
#         raise NotImplementedError()

#     def cur_position(self, mountain: Mountain) -> int:
#         raise NotImplementedError()

#     def add_mountains(self, mountains: list[Mountain]) -> None:
#         raise NotImplementedError()

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


