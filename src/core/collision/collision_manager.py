from abc import abstractmethod
from typing import Literal

from ..utils import Pos, insertion_sort
from .collidable import Collidable
from .collider import Collider
from .collision import Collision, PreCollision
from .collision_detection.collision_detector import CollisionDetector


class _Vertice2D:

    def __init__(self, collidable: Collidable, collider: Collider, is_initial: bool):
        super().__init__()
        self.is_initial = is_initial
        self.collidable = collidable
        self.collider = collider

    @property
    @abstractmethod
    def value(self) -> int:
        pass


class _YInitialVertice2D(_Vertice2D):
    def __init__(self, collidable: Collidable, collider: Collider):
        super().__init__(collidable, collider, True)

    @property
    def value(self) -> int:
        rect = self.collider.bounding_rect
        return rect.y


class _YFinalVertice2D(_Vertice2D):
    def __init__(self, collidable: Collidable, collider: Collider):
        super().__init__(collidable, collider, False)

    @property
    def value(self) -> int:
        rect = self.collider.bounding_rect
        return rect.y + rect.height


class _XInitialVertice2D(_Vertice2D):
    def __init__(self, collidable: Collidable, collider: Collider):
        super().__init__(collidable, collider, True)

    @property
    def value(self) -> int:
        rect = self.collider.bounding_rect
        return rect.x


class _XFinalVertice2D(_Vertice2D):
    def __init__(self, collidable: Collidable, collider: Collider):
        super().__init__(collidable, collider, False)

    @property
    def value(self) -> int:
        rect = self.collider.bounding_rect
        return rect.x + rect.width


class CollisionManager2D:
    def __init__(self) -> None:
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
        for collider in obj.get_colliders():
            self.x_sorted.append(_XInitialVertice2D(obj, collider))
            self.x_sorted.append(_XFinalVertice2D(obj, collider))
            self.y_sorted.append(_YInitialVertice2D(obj, collider))
            self.y_sorted.append(_YFinalVertice2D(obj, collider))
        self.active_objs.add(obj)
        self.update()

    def remove_collidable(self, obj: Collidable):
        self.objs_to_remove.add(obj)
        self.active_objs.remove(obj)

    def get_collisions(self) -> set[Collision]:
        return self.narrow_phase(self.broad_phase())

    def broad_phase(self) -> set[PreCollision]:
        colliding_in_x = self.broad_phase_in_axis("x")
        colliding_in_y = self.broad_phase_in_axis("y")
        self.objs_to_remove = set()
        return colliding_in_x.intersection(colliding_in_y)

    def broad_phase_in_axis(self, axis: Literal["x", "y"]) -> set[PreCollision]:
        """Implements the sweep-and-prune algorithm for one axis"""
        vertices = self.x_sorted if axis == "x" else self.y_sorted
        pre_collisions: set[PreCollision] = set()
        touching_objs: set[tuple[Collidable, Collider]] = set()
        vertices_to_remove: set[_Vertice2D] = set()
        for vertice in vertices:
            obj_1 = vertice.collidable
            collider_1 = vertice.collider
            if obj_1 in self.objs_to_remove:
                vertices_to_remove.add(vertice)
                continue
            if not vertice.is_initial:
                touching_objs.remove((obj_1, collider_1))
                continue
            for obj_2, collider_2 in touching_objs:
                if obj_1 == obj_2:
                    continue
                pre_collisions.add(
                    PreCollision(
                        obj_1=obj_1,
                        collider_1=collider_1,
                        obj_2=obj_2,
                        collider_2=collider_2,
                    )
                )
            touching_objs.add((obj_1, collider_1))
        for vertice in vertices_to_remove:
            vertices.remove(vertice)
        return pre_collisions

    def narrow_phase(self, pre_collisions: set[PreCollision]) -> set[Collision]:
        collisions: set[Collision] = set()
        for pre_collision in pre_collisions:
            collider_1 = pre_collision.collider_1
            collider_2 = pre_collision.collider_2
            if vector := CollisionDetector.collide(collider_1, collider_2):
                collisions.add(Collision.from_pre_collision(pre_collision, vector))
        return collisions

    def sort_on_x(self):
        insertion_sort(self.x_sorted, size=(lambda v: v.value))

    def sort_on_y(self):
        insertion_sort(self.y_sorted, size=(lambda v: v.value))
