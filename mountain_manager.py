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

    def __init__(self) -> None:
        self.manager = []

    def add_mountain(self, mountain: Mountain):
        self.manager.append(mountain)

    def remove_mountain(self, mountain: Mountain):
        self.manager.remove(mountain)

    def edit_mountain(self, old: Mountain, new: Mountain):
        self.manager.remove(old)
        self.manager.insert(self.manager.index(old), new)
        

    def mountains_with_difficulty(self, diff: int):
        mountains_with_diff = [mountain for mountain in self.manager 
                               if mountain.difficulty_level == diff]
        return mountains_with_diff


    def group_by_difficulty(self):
        """
        Returns a list of mountain groups, where each group contains mountains with the same difficulty level.
        
        The time complexity of this method is O(nlogn) because of the sorting operation on the list of mountains. The method 
        first sorts the list by difficulty level, which takes O(nlogn) time complexity, where n is the length of the manager list. 
        Then, it groups the mountains based on their difficulty level using the groupby function from the itertools module. The groupby 
        function takes O(n) time complexity for an input iterable of length n. Finally, the method appends each group of mountains 
        to a new list, which takes O(1) time complexity.
        """
      
        self.manager.sort(key=lambda x: x.difficulty_level)  # sort the list by difficulty level
        grouped_mountains = []
        for difficulty, group in groupby(self.manager, key=lambda x: x.difficulty_level):
            # group the mountains based on their difficulty level
            grouped_mountains.append(list(group))
        return grouped_mountains

