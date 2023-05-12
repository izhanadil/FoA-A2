
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
    """
    Hashes a given key to an integer representing the index in the hash table.
    
    :param key: The key to hash.
    :return: An integer representing the index in the hash table.
    
    If self.level < len(key), the hash function will use the character at the
    index of self.level in the key to compute the hash. Otherwise, the hash
    function returns self.TABLE_SIZE-1, indicating that the key should be
    stored in a sub-hash table at index self.TABLE_SIZE-1.
    
    :complexity: O(1)
    """
    if self.level < len(key):
        return ord(key[self.level]) % (self.TABLE_SIZE-1)
    return self.TABLE_SIZE-1


def __getitem__(self, key: K) -> V:
    """
    Returns the value associated with the given key.
    
    :param key: The key associated with the value to retrieve.
    :return: The value associated with the given key.
    :raise KeyError: If the key is not found in the hash table.
    
    This function first calls the get_location method to get the location of the
    key in the hash table. If the location is within the bounds of the current
    table, the value at that location is returned. Otherwise, a KeyError is raised.
    
    :complexity: O(1)
    """
    loc = self.get_location(key)
    if loc[-1] < self.TABLE_SIZE - 1:
        return self.table[loc[-2]][loc[-1]]
    raise KeyError


def __setitem__(self, key: K, value: V) -> None:
    """
    Sets the value associated with the given key in the hash table to the given value.
    
    :param key: The key to associate with the value.
    :param value: The value to associate with the key.
    
    This function first calls the get_location method to get the location of the
    key in the hash table. If the location is within the bounds of the current
    table, the value at that location is set to the given value. Otherwise, a new
    sub-hash table is created and the key and value are added to the new table.
    
    :complexity: O(1) on average, but can be O(n) in the worst case if a large number
    of keys hash to the same location, causing a chain of sub-hash tables to be created.
    """
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
        """Delete an item from the hash table by key.
        
        Args:
        - key: The key of the item to delete.
        
        Raises:
        - KeyError: If the key is not found in the hash table.
        
        Complexity:
        - Time: O(log n), where n is the number of items in the hash table.
            This is because the `get_location` method has time complexity O(log n),
            and deleting an item from a list has time complexity O(n),
            where n is the length of the list.
        - Space: O(log n) because of the call stack used by the `get_location` method.
        """
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
        """Return the number of items in the hash table.
        
        Complexity:
        - Time: O(1), because the `size` attribute is maintained with every insert and delete operation.
        - Space: O(1).
        """
        return self.size

    def __str__(self) -> str:
        """Return a string representation of the hash table.
        
        Complexity:
        - Time: O(n), where n is the number of items in the hash table.
            This is because the `list` constructor has time complexity O(n),
            and the `join` method has time complexity O(n).
        - Space: O(n), where n is the number of items in the hash table.
            This is because the `join` method creates a new string object with length O(n),
            and the `list` constructor creates a new list object with length O(n).
        """
        return str(list(self))

    def get_location(self, key):
        """Return the location of the given key in the hash table.
        
        Args:
        - key: The key to look up.
        
        Returns:
        - A list of integers representing the location of the key in the hash table.
        
        Complexity:
        - Time: O(log n), where n is the number of items in the hash table.
            This is because the `hash` method has time complexity O(1),
            and the loop in this method iterates at most log(n) times.
        - Space: O(log n), because the location list has length at most log(n).
        """
        current_table = self
        location = []
        while True:
            location.append(current_table.hash(key))
            if location[-1] < current_table.TABLE_SIZE - 1:
                break
            current_table = current_table.table[current_table.TABLE_SIZE - 1]
        return location

    def __iter__(self):
        """Iterate over the items in the hash table.
        
        Complexity:
        - Time: O(n), where n is the number of items in the hash table.
            This is because the `yield` statement is executed once for each item in the hash table.
        - Space: O(1).
        """
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
