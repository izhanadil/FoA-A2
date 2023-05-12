# from mountain import Mountain

# class MountainManager:

#     def __init__(self) -> None:
#         pass

#     def add_mountain(self, mountain: Mountain):
#         raise NotImplementedError()

#     def remove_mountain(self, mountain: Mountain):
#         raise NotImplementedError()

#     def edit_mountain(self, old: Mountain, new: Mountain):
#         raise NotImplementedError()

#     def mountains_with_difficulty(self, diff: int):
#         raise NotImplementedError()

#     def group_by_difficulty(self):
#         raise NotImplementedError()


# from mountain import Mountain
# from typing import List

# class MountainManager:

#     def __init__(self) -> None:
#         self._mountains = []
#         self._mountain_difficulties = {}

#     def add_mountain(self, mountain: Mountain) -> None:
#         self._mountains.append(mountain)
#         if mountain.difficulty_level in self._mountain_difficulties:
#             self._mountain_difficulties[mountain.difficulty_level].append(mountain)
#         else:
#             self._mountain_difficulties[mountain.difficulty_level] = [mountain]

#     def remove_mountain(self, mountain: Mountain) -> None:
#         self._mountains.remove(mountain)
#         self._mountain_difficulties[mountain.difficulty].remove(mountain)

#     def edit_mountain(self, old_mountain: Mountain, new_mountain: Mountain) -> None:
#         self.remove_mountain(old_mountain)
#         self.add_mountain(new_mountain)

#     def mountains_with_difficulty(self, diff: int) -> List[Mountain]:
#         return self._mountain_difficulties.get(diff, [])

#     def group_by_difficulty(self) -> List[List[Mountain]]:
#         groups = []
#         for diff in sorted(self._mountain_difficulties.keys()):
#             groups.append(self._mountain_difficulties[diff])
#         return groups


from mountain import Mountain
from itertools import groupby


class MountainManager:

    def _init_(self) -> None:
        self.manager = []

    def add_mountain(self, mountain: Mountain):
        self.manager.append(mountain)

    def remove_mountain(self, mountain: Mountain):
        self.manager.remove(mountain)

    def edit_mountain(self, old: Mountain, new: Mountain):
        self.manager.remove(old)
        self.manager.insert(self.manager.index(old), new)
        

    def mountains_with_difficulty(self, diff: int):
        mountains_with_diff = [mountain for mountain in self.manager if mountain.difficulty_level == diff]
        return mountains_with_diff


    def group_by_difficulty(self):
        """
        The time complexity of the group_by_difficulty method depends on the size of our manager list, which contains all the mountain 
        objects. Sorting of manager  takes O(nlogn) time complexity, where n is the length of the manager list. 
        Then, the method since we used the groupby function from the itertools  module to group the mountains based on their difficulty_level. 
        groupby function takes O(n) time complexity for an input iterable of length n. Finally, the method appends each group of mountains 
        to a new list grouped_mountains, which takes O(1) time complexity.
        Therefore, the overall time complexity of the group_by_difficulty method is O(nlogn) because of the sorting operation.
        """
      
        self.manager.sort(key=lambda x: x.difficulty_level)  # sort the list by difficulty level
        grouped_mountains = []
        for difficulty, group in groupby(self.manager, key=lambda x: x.difficulty_level):
            # group the mountains based on their difficulty level
            grouped_mountains.append(list(group))
        return grouped_mountains