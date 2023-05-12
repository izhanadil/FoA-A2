from __future__ import annotations

from typing import Generic, TypeVar, Iterator
from data_structures.hash_table import LinearProbeTable, FullError
from data_structures.referential_array import ArrayR

K1 = TypeVar('K1')
K2 = TypeVar('K2')
V = TypeVar('V')


class DoubleKeyTable(Generic[K1, K2, V]):
    """
    Double Hash Table.

    Type Arguments:
        - K1:   1st Key Type. In most cases should be string.
                Otherwise `hash1` should be overwritten.
        - K2:   2nd Key Type. In most cases should be string.
                Otherwise `hash2` should be overwritten.
        - V:    Value Type.

    Unless stated otherwise, all methods have O(1) complexity.
    """

    # No test case should exceed 1 million entries.
    TABLE_SIZES = [5, 13, 29, 53, 97, 193, 389, 769, 1543, 3079, 6151, 12289, 24593, 49157, 98317, 196613, 393241,
                   786433, 1572869]

    HASH_BASE = 31

    def __init__(self, sizes: list | None = None, internal_sizes: list | None = None) -> None:
        if sizes is not None:
            self.TABLE_SIZES = sizes
        self.size_slot = 0
        self.array: ArrayR[tuple[K1, LinearProbeTable]] = ArrayR(self.TABLE_SIZES[self.size_slot])
        self.inter_sizes = internal_sizes
        self.count = 0


    def hash1(self, key: K1) -> int:
        """
        Hash the 1st key for insert/retrieve/update into the hashtable.

        :complexity: O(len(key))
        """

        value = 0
        a = 31415
        for char in key:
            value = (ord(char) + a * value) % self.table_size
            a = a * self.HASH_BASE % (self.table_size - 1)
        return value

    def hash2(self, key: K2, sub_table: LinearProbeTable[K2, V]) -> int:
        """
        Hash the 2nd key for insert/retrieve/update into the hashtable.

        :complexity: O(len(key))
        """

        value = 0
        a = 31415
        for char in key:
            value = (ord(char) + a * value) % sub_table.table_size
            a = a * self.HASH_BASE % (sub_table.table_size - 1)
        return value

    def _linear_probe(self, key1: K1, key2: K2, is_insert: bool) -> tuple[int, int]:
        """
        Find the correct position for this key in the hash table using linear probing.

        :raises KeyError: When the key pair is not in the table, but is_insert is False.
        :raises FullError: When a table is full and cannot be inserted.
        """
        position_1 = self.hash1(key1)
        while True:
            if self.array[position_1] is None:
                if is_insert:
                    n_table = LinearProbeTable(self.inter_sizes)
                    n_table.hash = lambda k: self.hash2(k, n_table)
                    self.array[position_1] = (key1, n_table)
                    self.count += 1
                    break
                else:
                    raise KeyError(key1)

            elif self.array[position_1][0] == key1:
                break
            else:
                position_1 = (position_1 + 1) % self.table_size


        inter_table = self.array[position_1][1]
        position_2 = self.hash2(key2, inter_table)
        for _ in range(inter_table.table_size):
            if self.array[position_1][1].array[position_2] is None:
                if is_insert:
                    return (position_1, position_2)
                else:
                    raise KeyError(key2)
            elif inter_table.array[position_2][0] == key2:
                return (position_1, position_2)
            else:
                position_2 = (position_2 + 1) % inter_table.table_size

        if is_insert:
            raise FullError("Table=full")
        else:
            raise KeyError(key2)

    def iter_keys(self, key: K1 | None = None) -> Iterator[K1 | K2]:
        """
        key = None:
            Returns an iterator of all top-level keys in hash table
        key = k:
            Returns an iterator of all keys in the bottom-hash-table for k.
        """
        if key is not None:

            for ele in self.array:
                if ele is not None:
                    (ar_key, value) = ele
                    if key == ar_key:
                        for ar in value.array:
                            if ar is not None:
                                (inter_key, value) = ar
                                self.curr_key = inter_key
                                break
        else:
            for ele in self.array:
                if ele is not None:
                    (top_key, value) = ele
                    self.curr_key = top_key
                    break

        return iter(self)

    def keys(self, key: K1 | None = None) -> list[K1]:
        """
        key = None: returns all top-level keys in the table.
        key = x: returns all bottom-level keys for top-level key x.
        """
        list_key = []

        if key is not None:

            for ele in self.array:
                if ele is not None:
                    (ar_key, value) = ele
                    if key == ar_key:
                        for ar in value.array:
                            if ar is not None:
                                (inter_key, value) = ar
                                list_key.append(inter_key)

        else:
            for ele in self.array:
                if ele is not None:
                    (top_key, value) = ele
                    list_key.append(top_key)

        return list_key

    def iter_values(self, key: K1 | None = None) -> Iterator[V]:
        """
        key = None:
            Returns an iterator of all values in hash table
        key = k:
            Returns an iterator of all values in the bottom-hash-table for k.
        """
        self.iter_num = 0


        if key is not None:
            for ele in self.array:
                if ele is not None:
                    (ar_key, value) = ele
                    if key == ar_key:
                        for ar in value.array:
                            if ar is not None:
                                (inter_key, value) = ar
                                self.curr_value = value
                                break
        else:
            for ele in self.array:
                if ele is not None:
                    (ar_key, value) = ele
                    for ar in value.array:
                        if ar is not None:
                            (inter_key, value) = ar
                            self.curr_value = value
                            break

        return iter(self)

    def values(self, key: K1 | None = None) -> list[V]:
        """
        key = None: returns all values in the table.
        key = x: returns all values for top-level key x.
        """
        list_val = []


        for ele in self.array:
            if ele is not None:
                (ar_key, value) = ele
                if key is not None and key != ar_key:
                    continue

                for ar in value.array:
                    if ar is not None:
                        (inter_key, value) = ar
                        list_val.append(value)

        return list_val

    def __contains__(self, key: tuple[K1, K2]) -> bool:
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

    def __getitem__(self, key: tuple[K1, K2]) -> V:
        """
        Get the value at a certain key

        :raises KeyError: when the key doesn't exist.
        """
        position = self._linear_probe(key[0], key[1], False)
        return self.array[position[0]][1].__getitem__(key[1])

    def __setitem__(self, key: tuple[K1, K2], data: V) -> None:
        """
        Set an (key, value) pair in our hash table.
        """
        position = self._linear_probe(key[0], key[1], True)
        if not self.array[position[0]]:
            self.count += 1
        self.array[position[0]][1].__setitem__(key[1], data)
        if len(self) > self.table_size / 2:
            self._rehash()

    def __delitem__(self, key: tuple[K1, K2]) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :raises KeyError: when the key doesn't exist.
        """
        position = self._linear_probe(key[0], key[1], False)
        del self.array[position[0]][1][key[1]]
        if self.array[position[0]][1].count == 0:
            self.array[position[0]] = None
            self.count -= 1

    def _rehash(self) -> None:
        """
        Need to resize table and reinsert all values

        :complexity best: O(N*hash(K)) No probing.
        :complexity worst: O(N*hash(K) + N^2*comp(K)) Lots of probing.
        Where N is len(self)
        """
        prev_array = self.array
        self.size_slot += 1
        if self.size_slot == len(self.TABLE_SIZES):
            return
        self.array = ArrayR(self.TABLE_SIZES[self.size_slot])
        self.count = 0

        for ele in prev_array:
            if ele is None:
                continue

            key1, value1 = ele
            for internal_ele in value1.array:
                if internal_ele is None:
                    continue
                key2, value2 = internal_ele
                self[(key1, key2)] = value2

    @property
    def table_size(self) -> int:
        """
        Return the current size of the table (different from the length)
        """
        return len(self.array)

    def __len__(self) -> int:
        """
        Returns number of elements in the hash table
        """
        return self.count

    def __str__(self) -> str:
        """
        String representation.

        Not required but may be a good testing tool.
        """
        result = "\n".join(f"({key}, {value})" for key, value in self.array if key is not None)
        return result

    def __iter__(self):
        return self

    def __next__(self) -> K1 | V:
        if self.iter_num == 0:
            if self.curr_key is not None:
                self.iter_num += 1
                curr_ele = self.curr_key
                self.curr_key = None
                found_curr_key = False
                for ele in self.array:
                    if ele is not None:
                        key, value = ele
                        if found_curr_key:
                            self.curr_key = key
                            break
                        if key == curr_ele:
                            found_curr_key = True
                return curr_ele
            else:
                raise StopIteration

        else:
            if self.curr_value is not None:
                self.iter_num += 1
                curr_ele = self.curr_value
                self.curr_value = None
                found_curr_value = False
                ele_index = 0
                while not found_curr_value and ele_index < len(self.array):
                    if self.array[ele_index] is not None:
                        for value2 in self.array[ele_index][1].values():
                            if found_curr_value:
                                self.curr_value = value2
                                found_curr_value = False
                            if value2 == curr_ele:
                                found_curr_value = True
                    ele_index += 1
                if found_curr_value:
                    return curr_ele
                else:
                    raise StopIteration
            else:
                raise StopIteration


# from __future__ import annotations

# from typing import Generic, TypeVar, Iterator
# from data_structures.hash_table import LinearProbeTable, FullError
# from data_structures.referential_array import ArrayR

# K1 = TypeVar('K1')
# K2 = TypeVar('K2')
# V = TypeVar('V')

# class DoubleKeyTable(Generic[K1, K2, V]):
#     """
#     Double Hash Table.

#     Type Arguments:
#         - K1:   1st Key Type. In most cases should be string.
#                 Otherwise `hash1` should be overwritten.
#         - K2:   2nd Key Type. In most cases should be string.
#                 Otherwise `hash2` should be overwritten.
#         - V:    Value Type.

#     Unless stated otherwise, all methods have O(1) complexity.
#     """

#     # No test case should exceed 1 million entries.
#     TABLE_SIZES = [5, 13, 29, 53, 97, 193, 389, 769, 1543, 3079, 6151, 12289, 24593, 49157, 98317, 196613, 393241, 786433, 1572869]

#     HASH_BASE = 31

#     def __init__(self, sizes:list|None=None, internal_sizes:list|None=None) -> None:
#         raise NotImplementedError()

#     def hash1(self, key: K1) -> int:
#         """
#         Hash the 1st key for insert/retrieve/update into the hashtable.

#         :complexity: O(len(key))
#         """

#         value = 0
#         a = 31415
#         for char in key:
#             value = (ord(char) + a * value) % self.table_size
#             a = a * self.HASH_BASE % (self.table_size - 1)
#         return value

#     def hash2(self, key: K2, sub_table: LinearProbeTable[K2, V]) -> int:
#         """
#         Hash the 2nd key for insert/retrieve/update into the hashtable.

#         :complexity: O(len(key))
#         """

#         value = 0
#         a = 31415
#         for char in key:
#             value = (ord(char) + a * value) % sub_table.table_size
#             a = a * self.HASH_BASE % (sub_table.table_size - 1)
#         return value

#     def _linear_probe(self, key1: K1, key2: K2, is_insert: bool) -> tuple[int, int]:
#         """
#         Find the correct position for this key in the hash table using linear probing.

#         :raises KeyError: When the key pair is not in the table, but is_insert is False.
#         :raises FullError: When a table is full and cannot be inserted.
#         """
#         raise NotImplementedError()

#     def iter_keys(self, key:K1|None=None) -> Iterator[K1|K2]:
#         """
#         key = None:
#             Returns an iterator of all top-level keys in hash table
#         key = k:
#             Returns an iterator of all keys in the bottom-hash-table for k.
#         """
#         raise NotImplementedError()

#     def keys(self, key:K1|None=None) -> list[K1]:
#         """
#         key = None: returns all top-level keys in the table.
#         key = x: returns all bottom-level keys for top-level key x.
#         """
#         raise NotImplementedError()

#     def iter_values(self, key:K1|None=None) -> Iterator[V]:
#         """
#         key = None:
#             Returns an iterator of all values in hash table
#         key = k:
#             Returns an iterator of all values in the bottom-hash-table for k.
#         """
#         raise NotImplementedError()

#     def values(self, key:K1|None=None) -> list[V]:
#         """
#         key = None: returns all values in the table.
#         key = x: returns all values for top-level key x.
#         """
#         raise NotImplementedError()

#     def __contains__(self, key: tuple[K1, K2]) -> bool:
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

#     def __getitem__(self, key: tuple[K1, K2]) -> V:
#         """
#         Get the value at a certain key

#         :raises KeyError: when the key doesn't exist.
#         """
#         raise NotImplementedError()

#     def __setitem__(self, key: tuple[K1, K2], data: V) -> None:
#         """
#         Set an (key, value) pair in our hash table.
#         """

#         raise NotImplementedError()

#     def __delitem__(self, key: tuple[K1, K2]) -> None:
#         """
#         Deletes a (key, value) pair in our hash table.

#         :raises KeyError: when the key doesn't exist.
#         """
#         raise NotImplementedError()

#     def _rehash(self) -> None:
#         """
#         Need to resize table and reinsert all values

#         :complexity best: O(N*hash(K)) No probing.
#         :complexity worst: O(N*hash(K) + N^2*comp(K)) Lots of probing.
#         Where N is len(self)
#         """
#         raise NotImplementedError()

#     def table_size(self) -> int:
#         """
#         Return the current size of the table (different from the length)
#         """
#         raise NotImplementedError()

#     def __len__(self) -> int:
#         """
#         Returns number of elements in the hash table
#         """
#         raise NotImplementedError()

#     def __str__(self) -> str:
#         """
#         String representation.

#         Not required but may be a good testing tool.
#         """
#         raise NotImplementedError()








