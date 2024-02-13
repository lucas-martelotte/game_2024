from abc import abstractmethod
from typing import Literal

from ..utils import Pos, insertion_sort
from .collidable import Collidable
from .collision_detector import CollisionDetector


class _Vertice2D:

    def __init__(self, collidable: Collidable, is_initial: bool):
        super().__init__()
        self.is_initial = is_initial
        self.collidable = collidable

    @property
    @abstractmethod
    def value(self) -> int:
        pass


class _YInitialVertice2D(_Vertice2D):
    def __init__(self, collidable: Collidable):
        super().__init__(collidable, True)

    @property
    def value(self) -> int:
        rect = self.collidable.collider.bounding_rect
        return rect.y


class _YFinalVertice2D(_Vertice2D):
    def __init__(self, collidable: Collidable):
        super().__init__(collidable, False)

    @property
    def value(self) -> int:
        rect = self.collidable.collider.bounding_rect
        return rect.y + rect.height


class _XInitialVertice2D(_Vertice2D):
    def __init__(self, collidable: Collidable):
        super().__init__(collidable, True)

    @property
    def value(self) -> int:
        rect = self.collidable.collider.bounding_rect
        return rect.x


class _XFinalVertice2D(_Vertice2D):
    def __init__(self, collidable: Collidable):
        super().__init__(collidable, False)

    @property
    def value(self) -> int:
        rect = self.collidable.collider.bounding_rect
        return rect.x + rect.width


class CollisionManager2D:
    def __init__(self) -> None:
        # To decide how to order a pair of colliding objects
        self.obj_sort_criteria = lambda x: x.collider.bounding_rect.x
        self.objs_to_remove: set[Collidable] = set()
        self.active_objs: set[Collidable] = set()
        self.x_sorted: list[_Vertice2D] = []
        self.y_sorted: list[_Vertice2D] = []

    def update(self):
        self.sort_on_x()
        self.sort_on_y()

    def add_collidables(self, objs: frozenset[Collidable]):
        for obj in objs:
            self.add_collidable(obj)

    def remove_collidables(self, objs: frozenset[Collidable]):
        for obj in objs:
            self.remove_collidable(obj)

    def add_collidable(self, obj: Collidable):
        self.x_sorted.append(_XInitialVertice2D(obj))
        self.x_sorted.append(_XFinalVertice2D(obj))
        self.y_sorted.append(_YInitialVertice2D(obj))
        self.y_sorted.append(_YFinalVertice2D(obj))
        self.active_objs.add(obj)
        self.update()

    def remove_collidable(self, obj: Collidable):
        self.objs_to_remove.add(obj)
        self.active_objs.remove(obj)

    def get_collisions(self) -> set[tuple[Collidable, Collidable, Pos]]:
        return self.narrow_phase(self.broad_phase())

    def broad_phase(self) -> set[tuple[Collidable, Collidable]]:
        colliding_in_x = self.broad_phase_in_axis("x")
        colliding_in_y = self.broad_phase_in_axis("y")
        self.objs_to_remove = set()
        return colliding_in_x.intersection(colliding_in_y)

    def broad_phase_in_axis(
        self, axis: Literal["x", "y"]
    ) -> set[tuple[Collidable, Collidable]]:
        """Implements the sweep-and-prune algorithm for one axis"""
        vertices = self.x_sorted if axis == "x" else self.y_sorted
        colliding_pairs: set[tuple[Collidable, Collidable]] = set()
        touching_objs: set[Collidable] = set()
        vertices_to_remove: set[_Vertice2D] = set()
        for vertice in vertices:
            obj1 = vertice.collidable
            if obj1 in self.objs_to_remove:
                vertices_to_remove.add(vertice)
            if vertice.is_initial:
                for obj2 in touching_objs:
                    pair = sorted([obj1, obj2], key=self.obj_sort_criteria)
                    colliding_pairs.add((pair[0], pair[1]))
                touching_objs.add(obj1)
            else:
                touching_objs.remove(obj1)
        for vertice in vertices_to_remove:
            vertices.remove(vertice)
        return colliding_pairs

    def narrow_phase(
        self, possible_collisions: set[tuple[Collidable, Collidable]]
    ) -> set[tuple[Collidable, Collidable, Pos]]:
        collisions: set[tuple[Collidable, Collidable, Pos]] = set()
        for obj_1, obj_2 in possible_collisions:
            if vector := CollisionDetector.collide(obj_1.collider, obj_2.collider):
                collisions.add((obj_1, obj_2, vector))
        return collisions

    def sort_on_x(self):
        insertion_sort(self.x_sorted, size=(lambda v: v.value))

    def sort_on_y(self):
        insertion_sort(self.y_sorted, size=(lambda v: v.value))
