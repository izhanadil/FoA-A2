
# from __future__ import annotations
# from typing import Generic, TypeVar

# from data_structures.referential_array import ArrayR

# K = TypeVar("K")
# V = TypeVar("V")


# class InfiniteHashTable(Generic[K, V]):
#     """
#     Infinite Hash Table.

#     Type Arguments:
#         - K:    Key Type. In most cases should be string.
#                 Otherwise `hash` should be overwritten.
#         - V:    Value Type.

#     Unless stated otherwise, all methods have O(1) complexity.
#     """

#     TABLE_SIZE = 27

#     def _init_(self) -> None:
#         self.table = ArrayR(self.TABLE_SIZE)
#         self.level = 0

#     def hash(self, key: K) -> int:
#         if self.level < len(key):
#             return ord(key[self.level]) % (self.TABLE_SIZE-1)
#         return self.TABLE_SIZE-1

#     def _getitem_(self, key: K) -> V:
#         loc = self.get_location(key)
#         return self.table[loc[-1]].get(key)

#     def _setitem_(self, key: K, value: V) -> None:
#         loc = self.get_location(key)
#         table = self.table[loc[-1]]
#         table[key] = value
#         while len(table) > 1 and table.fullness() >= 0.5:
#             table, new_table = table.split()
#             loc.pop()
#             loc.append(len(self.table))
#             self.table.append(new_table)
#             self.level += 1

#     def _delitem_(self, key: K) -> None:
#         loc = self.get_location(key)
#         table = self.table[loc[-1]]
#         del table[key]
#         while len(table) == 1 and len(self.table) > 1:
#             self.table.pop()
#             self.level -= 1
#             loc.pop()
#             table = self.table[loc[-1]]

#     def _len_(self) -> int:
#         count = 0
#         for table in self.table:
#             count += len(table)
#         return count

#     def _str_(self) -> str:
#         result = "{"
#         for table in self.table:
#             result += f"{str(table)}, "
#         result = result.rstrip(", ")
#         result += "}"
#         return result

#     def get_location(self, key: K) -> list[int]:
#         loc = []
#         table = self.table
#         for i in range(self.level+1):
#             loc.append(self.hash(key))
#             if loc[i] < len(table) and table[loc[i]]:
#                 table = table[loc[i]]
#             else:
#                 raise KeyError(f"Key {key} does not exist.")
#         return loc

#     def _contains_(self, key: K) -> bool:
#         try:
#             _ = self[key]
#         except KeyError:
#             return False
#         else:
#             return True



from __future__ import annotations
from typing import Generic, TypeVar

from data_structures.referential_array import ArrayR

K = TypeVar("K")
V = TypeVar("V")

class InfiniteHashTable(Generic[K, V]):
    """
    Infinite Hash Table.

    Type Arguments:
        - K:    Key Type. In most cases should be string.
                Otherwise `hash` should be overwritten.
        - V:    Value Type.

    Unless stated otherwise, all methods have O(1) complexity.
    """

    TABLE_SIZE = 27

    def __init__(self) -> None:
        self.level = 0
        self.table = ArrayR(self.TABLE_SIZE)
        self.size = 0

    def hash(self, key: K) -> int:
        if self.level < len(key):
            return ord(key[self.level]) % (self.TABLE_SIZE-1)
        return self.TABLE_SIZE-1

    def __getitem__(self, key: K) -> V:
        loc = self.get_location(key)
        if loc[-1] < self.TABLE_SIZE - 1:
            return self.table[loc[-2]][loc[-1]]
        raise KeyError

    def __setitem__(self, key: K, value: V) -> None:
        loc = self.get_location(key)
        if loc[-1] < self.TABLE_SIZE - 1:
            self.table[loc[-2]][loc[-1]] = value
        else:
            new_table = InfiniteHashTable()
            new_table.level = self.level + 1
            new_table.__setitem__(key, value)
            self.table[self.TABLE_SIZE-1] = new_table
        self.size += 1

    def __delitem__(self, key: K) -> None:
        loc = self.get_location(key)
        if loc[-1] == self.TABLE_SIZE - 1:
            raise KeyError

        del self.table[loc[-2]][loc[-1]]
        self.size -= 1

        while len(self.table) == 1 and isinstance(self.table[0], InfiniteHashTable):
            new_root = self.table[0]
            self.level = new_root.level
            self.table = new_root.table

    def __len__(self):
        return self.size

    def __str__(self) -> str:
        return str(list(self))

    def get_location(self, key):
        current_table = self
        location = []
        while True:
            location.append(current_table.hash(key))
            if location[-1] < current_table.TABLE_SIZE - 1:
                break
            current_table = current_table.table[current_table.TABLE_SIZE - 1]
        return location

    def __iter__(self):
        for i in range(self.TABLE_SIZE - 1):
            if i < len(self.table):
                if isinstance(self.table[i], V):
                    yield self.table[i]
                elif isinstance(self.table[i], InfiniteHashTable):
                    for value in self.table[i]:
                        yield value

    def __contains__(self, key: K) -> bool:
        """
        Checks to see if the given key is in the Hash Table

        :complexity: O(n) for n keys stored in the table.
        """
        try:
            _ = self[key]
        except KeyError:
            return False
        else:
            return True
