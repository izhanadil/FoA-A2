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
       __path_top___
      /               \
    -<                 >-path_follow-
      \_path_bottom_/
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

        stack = [(self.store, False)]
        while stack:
            current, has_came_branch = stack.pop()
            if isinstance(current, TrailSeries):
                personality.add_mountain(current.mountain)
                stack.append((current.following.store, False))
            elif isinstance(current, TrailSplit):
                if not has_came_branch:
                    stack.append((current, True))
                    selected_path = current.path_top if personality.select_branch(current.path_top, current.path_bottom) \
                        else current.path_bottom
                    stack.append((selected_path.store, False))
                else:
                    stack.append((current.path_follow.store, False))

    def collect_all_mountains(self) -> list[Mountain]:
        """Returns a list of all mountains on the trail."""
        all_mounts = []

        if self.store is not None:
            if isinstance(self.store, TrailSeries):
                if self.store.mountain is not None:
                    all_mounts.append(self.store.mountain)
                all_mounts += self.store.following.collect_all_mountains()
            elif isinstance(self.store, TrailSplit):
                all_mounts += self.store.path_top.collect_all_mountains()
                all_mounts += self.store.path_bottom.collect_all_mountains()
                all_mounts += self.store.path_follow.collect_all_mountains()
        return all_mounts

    def length_k_paths(self, k) -> list[list[Mountain]]:  # Input to this should not exceed k > 50, at most 5 branches.
        """
        Returns a list of all paths of containing exactly k mountains.
        Paths are represented as lists of mountains.

        Paths are unique if they take a different branch, even if this results in the same set of mountains.
        """
        self.mountain_sets = []
        k_mountains = []
        self.mountain_on_each(self, self.store.path_top, [])
        self.mountain_on_each(self, self.store.path_bottom, [])

        i = 0
        while i < len(self.mountain_sets):
            mountains = self.mountain_sets[i]
            mountains.append(self.store.path_follow.store.mountain)
            if len(mountains) == k:
                k_mountains.append(mountains)
            i += 1

        return k_mountains



    def mountain_on_each(self, current: Trail, next: Trail, until):
        if current.store is not None and isinstance(current.store, TrailSeries) and current.store.mountain is not None:
            until = until + [current.store.mountain]
        current_t = next
        if current_t.store is None:
            self.mountain_sets.append(until)
        else:
            store = current_t.store
            if isinstance(store, TrailSeries):
                self.mountain_on_each(current_t, store.following, until)
            elif isinstance(store, TrailSplit):
                store_bran = [
                    (store.path_top, store.path_follow),
                    (store.path_bottom, store.path_follow)]
                for i, branch in enumerate(store_bran):
                    if i == 0:
                        self.mountain_on_each(branch[0], branch[1], until)
                    else:
                        self.mountain_on_each(branch[0], branch[1], until)

                        
# from _future_ import annotations
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
#        _path_top__
#       /               \
#     -<                 >-path_follow-
#       \path_bottom/
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
