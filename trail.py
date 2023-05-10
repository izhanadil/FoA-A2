from __future__ import annotations
from dataclasses import dataclass

from mountain import Mountain

from typing import TYPE_CHECKING, Union

# Avoid circular imports for typing.
if TYPE_CHECKING:
    from personality import WalkerPersonality

@dataclass
class TrailSplit:
    """
    A split in the trail.
       ___path_top____
      /               \
    -<                 >-path_follow-
      \__path_bottom__/
    """

    path_top: Trail
    path_bottom: Trail
    path_follow: Trail

    def remove_branch(self) -> TrailStore:
        """Removes the branch, should just leave the remaining following trail."""
        return self.path_follow.store

@dataclass
class TrailSeries:
    """
    A mountain, followed by the rest of the trail

    --mountain--following--

    """
    mountain: Mountain
    following: Trail

    def remove_mountain(self) -> TrailStore:
        """Removes the mountain at the beginning of this series."""
        return self.following.store

    def add_mountain_before(self, mountain: Mountain) -> TrailStore:
        """Adds a mountain in series before the current one."""
        return TrailSeries(mountain, Trail(self))

    def add_empty_branch_before(self) -> TrailStore:
        """Adds an empty branch, where the current trailstore is now the following path."""
        return TrailSplit(Trail(None), Trail(None), Trail(self))

    def add_mountain_after(self, mountain: Mountain) -> TrailStore:
        """Adds a mountain after the current mountain, but before the following trail."""
        return TrailSeries(self.mountain, Trail(TrailSeries(mountain, self.following)))

    def add_empty_branch_after(self) -> TrailStore:
        """Adds an empty branch after the current mountain, but before the following trail."""
        return TrailSeries(self.mountain, Trail(TrailSplit(Trail(None), Trail(None), self.following)))

TrailStore = Union[TrailSplit, TrailSeries, None]

@dataclass
class Trail:

    store: TrailStore = None

    def add_mountain_before(self, mountain: Mountain) -> Trail:
        """Adds a mountain before everything currently in the trail."""
        return Trail(TrailSeries(mountain, self))

    def add_empty_branch_before(self) -> Trail:
        """Adds an empty branch before everything currently in the trail."""
        return Trail(TrailSplit(Trail(None), Trail(None), self))

    def follow_path(self, personality: WalkerPersonality) -> None:
        """Follow a path and add mountains according to a personality."""
        raise NotImplementedError()

    def collect_all_mountains(self) -> list[Mountain]:
        """Returns a list of all mountains on the trail."""
        raise NotImplementedError()

    def length_k_paths(self, k) -> list[list[Mountain]]: # Input to this should not exceed k > 50, at most 5 branches.
        """
        Returns a list of all paths of containing exactly k mountains.
        Paths are represented as lists of mountains.

        Paths are unique if they take a different branch, even if this results in the same set of mountains.
        """
        raise NotImplementedError()
# from __future__ import annotations
# from dataclasses import dataclass

# from mountain import Mountain

# from typing import TYPE_CHECKING, Union

# # Avoid circular imports for typing.
# if TYPE_CHECKING:
#     from personality import WalkerPersonality

# @dataclass
# class TrailSplit:
#     """
#     A split in the trail.
#        __path_top___
#       /               \
#     -<                 >-path_follow-
#       \_path_bottom_/
#     """

#     path_top: Trail
#     path_bottom: Trail
#     path_follow: Trail

#     def remove_branch(self) -> TrailStore:
#         """Removes the branch, should just leave the remaining following trail."""
#         return self.path_follow.store

# @dataclass
# class TrailSeries:
#     """
#     A mountain, followed by the rest of the trail

#     --mountain--following--

#     """

#     mountain: Mountain
#     following: Trail

#     def remove_mountain(self) -> TrailStore:
#         """Removes the mountain at the beginning of this series."""
#         return self.following.store

#     def add_mountain_before(self, mountain: Mountain) -> TrailStore:
#         """Adds a mountain in series before the current one."""
#         new_series = TrailSeries(mountain, Trail(self))
#         return new_series

#     def add_empty_branch_before(self) -> TrailStore:
#         """Adds an empty branch, where the current trailstore is now the following path."""
#         new_split = TrailSplit(Trail(None), Trail(None), Trail(self.following))
#         return TrailStore(new_split)

#     def add_mountain_after(self, mountain: Mountain) -> TrailStore:
#         """Adds a mountain after the current mountain, but before the following trail."""
#         new_series = TrailSeries(self.mountain, TrailSeries(mountain, self.following))
#         return new_series

#     def add_empty_branch_after(self) -> TrailStore:
#         """Adds an empty branch after the current mountain, but before the following trail."""
#         new_split = TrailSplit(Trail(None), Trail(None), Trail(self.following))
#         new_series = TrailSeries(self.mountain, Trail(new_split))
#         return new_series

# TrailStore = Union[TrailSplit, TrailSeries, None]

# @dataclass
# class Trail:

#     store: TrailStore = None

#     def add_mountain_before(self, mountain: Mountain) -> Trail:
#         """Adds a mountain before everything currently in the trail."""
#         if self.store is None:
#             return Trail(TrailSeries(mountain, Trail(None)))
#         else:
#             return Trail(self.store.add_mountain_before(mountain))

#     def add_empty_branch_before(self) -> Trail:
#         """Adds an empty branch before everything currently in the trail."""
#         if self.store is None:
#             new_split = TrailSplit(Trail(None), Trail(None), Trail(None))
#             return Trail(new_split)
#         else:
#             return Trail(self.store.add_empty_branch_before())

#     def follow_path(self, personality: WalkerPersonality) -> None:
#         """Follow a path and add mountains according to a personality."""
#         current_trail = self
#         while current_trail.store is not None:
#             if isinstance(current_trail.store, TrailSplit):
#                 if personality.select_branch(current_trail.store.path_top, current_trail.store.path_bottom):
#                     current_trail = current_trail.store.path_top
#                 else:
#                     current_trail = current_trail.store.path_bottom
#             elif isinstance(current_trail.store, TrailSeries):
#                 personality.add_mountain(current_trail.store.mountain)
#                 current_trail = current_trail.store.following

#     def collect_all_mountains(self) -> list[Mountain]:
#         """Returns a list of all mountains on the trail."""
#         raise NotImplementedError()

#     def length_k_paths(self, k) -> list[list[Mountain]]: # Input to this should not exceed k > 50, at most 5 branches.
#         """
#         Returns a list of all paths of containing exactly k mountains.
#         Paths are represented as lists of mountains.

#         Paths are unique if they take a different branch, even if this results in the same set of mountains.
#         """
#         raise NotImplementedError()
