# from __future__ import annotations
# from typing import Generic, TypeVar

# from data_structures.referential_array import ArrayR

# K = TypeVar("K")
# V = TypeVar("V")

# class InfiniteHashTable(Generic[K, V]):
#     # """
#     # Infinite Hash Table.

#     # Type Arguments:
#     #     - K:    Key Type. In most cases should be string.
#     #             Otherwise `hash` should be overwritten.
#     #     - V:    Value Type.

#     # Unless stated otherwise, all methods have O(1) complexity.
#     # """

#     TABLE_SIZE = 27

#     def __init__(self) -> None:
#         self.level = 0
#         self.table = ArrayR(self.TABLE_SIZE)

#     def hash(self, key: K) -> int:
#         if self.level < len(key):
#             return ord(key[self.level]) % (self.TABLE_SIZE-1)
#         return self.TABLE_SIZE-1

#     def __getitem__(self, key: K) -> V:
#         """
#         Get the value at a certain key

#         :raises KeyError: when the key doesn't exist.
#         """
#         pos = self.get_location(key)
#         return self.table[pos[-1]]

#     def __setitem__(self, key: K, value: V) -> None:
#         """
#         Set an (key, value) pair in our hash table.
#         """
#         pos = self.get_location(key)
#         self.table[pos[-1]] = value

#     def __delitem__(self, key: K) -> None:
#         """
#         Deletes a (key, value) pair in our hash table.

#         :raises KeyError: when the key doesn't exist.
#         """
#         pos = self.get_location(key)
#         self.table[pos[-1]] = None

#     def __len__(self):
#         return len(self.table)

#     def __str__(self) -> str:
#         """
#         String representation.

#         Not required but may be a good testing tool.
#         """
#         raise NotImplementedError()

#     def get_location(self, key):
#         """
#         Get the sequence of positions required to access this key.

#         :raises KeyError: when the key doesn't exist.
#         """
#         pos = []
#         while True:
#             h = self.hash(key)
#             if self.table[h] is None:
#                 raise KeyError(key)
#             elif self.level == len(key) and isinstance(self.table[h], tuple) and self.table[h][0] == key:
#                 pos.append(h)
#                 break
#             elif self.level < len(key) and isinstance(self.table[h], InfiniteHashTable):
#                 pos.append(h)
#                 self = self.table[h]
#                 self.level += 1
#             else:
#                 raise KeyError(key)
#         return pos

#     def __contains__(self, key: K) -> bool:
#         """
#         Checks to see if the given key is in the Hash Table

#         :complexity: See linear probe.
#         """
#         try:
#             _ = self[key]
#         except KeyError:
#             return False
#         else:
#             return True
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
            return self.table[loc[-1]][loc[-2]]
        raise KeyError

    def __setitem__(self, key: K, value: V) -> None:
        loc = self.get_location(key)
        while len(self.table) <= loc[-1]:
            self.table.append(None)
        if loc[-1] < self.TABLE_SIZE - 1:
            if self.table[loc[-1]] is None:
                self.table[loc[-1]] = ArrayR(self.TABLE_SIZE)
            self.table[loc[-1]][loc[-2]] = value
        else:
            new_table = InfiniteHashTable()
            new_table.level = self.level + 1
            new_table.__setitem__(key, value)
            if self.table[-1] is None:
                self.table[-1] = new_table
            else:
                self.table.append(new_table)
        self.size += 1

    def __delitem__(self, key: K) -> None:
        loc = self.get_location(key)
        if loc[-1] == self.TABLE_SIZE - 1:
            raise KeyError

        del self.table[loc[-1]][loc[-2]]
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
            if current_table.table[-1] is None:
                current_table.table[-1] = InfiniteHashTable()
            current_table = current_table.table[-1]
        return location

    def __iter__(self):
        for i in range(self.TABLE_SIZE - 1):
            if i < len(self.table) and self.table[i] is not None:
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
