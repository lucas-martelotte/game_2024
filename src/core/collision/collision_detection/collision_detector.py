from ...utils import Pos, Rect
from ..collider import Collider
from ..colliders import PolygonCollider, RectCollider
from .aabb import aabb_algorithm
from .gjk import gjk_algorithm


class CollisionDetector:
    def __init__(self):
        pass

    @staticmethod
    def collide(obj_1: Collider, obj_2: Collider) -> Pos | None:
        """
        If obj_1 does not collide with obj_2, returns None.
        Otherwise, returns the minimal translation vector V
        that separates the two (obj_1 + V does no intersect
        with obj_2).
        """
        if isinstance(obj_1, RectCollider) and isinstance(obj_2, RectCollider):
            return aabb_algorithm(obj_1.rect, obj_2.rect)
        elif isinstance(obj_1, PolygonCollider) and isinstance(obj_2, PolygonCollider):
            return Pos(0, 0) if gjk_algorithm(obj_1.as_array, obj_2.as_array) else None
        else:
            raise NotImplementedError()
