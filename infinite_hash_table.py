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

    def hash(self, key: K) -> int:
        if self.level < len(key):
            return ord(key[self.level]) % (self.TABLE_SIZE-1)
        return self.TABLE_SIZE-1

    def __getitem__(self, key: K) -> V:
        """
        Get the value at a certain key

        :raises KeyError: when the key doesn't exist.
        """
        pos = self.get_location(key)
        return self.table[pos[-1]]

    def __setitem__(self, key: K, value: V) -> None:
        """
        Set an (key, value) pair in our hash table.
        """
        pos = self.get_location(key)
        self.table[pos[-1]] = value

    def __delitem__(self, key: K) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :raises KeyError: when the key doesn't exist.
        """
        pos = self.get_location(key)
        self.table[pos[-1]] = None

    def __len__(self):
        return len(self.table)

    def __str__(self) -> str:
        """
        String representation.

        Not required but may be a good testing tool.
        """
        raise NotImplementedError()

    def get_location(self, key):
        """
        Get the sequence of positions required to access this key.

        :raises KeyError: when the key doesn't exist.
        """
        pos = []
        while True:
            h = self.hash(key)
            if self.table[h] is None:
                raise KeyError(key)
            elif self.level == len(key) and isinstance(self.table[h], tuple) and self.table[h][0] == key:
                pos.append(h)
                break
            elif self.level < len(key) and isinstance(self.table[h], InfiniteHashTable):
                pos.append(h)
                self = self.table[h]
                self.level += 1
            else:
                raise KeyError(key)
        return pos

    def __contains__(self, key: K) -> bool:
        """
        Checks to see if the given key is in the Hash Table

        :complexity: See linear probe.
        """
        try:
            _ = self[key]
        except KeyError:
            return False
        else:
            return True
