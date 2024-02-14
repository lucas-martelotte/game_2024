from ...utils import Pos, Rect
from ..collider import Collider
from ..colliders import PolygonCollider, RectCollider
from .gjk import gjk_algorithm_2d


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
            return CollisionDetector.AABBCollision(obj_1, obj_2)
        elif isinstance(obj_1, PolygonCollider) and isinstance(obj_2, PolygonCollider):
            return (
                Pos(0, 0) if gjk_algorithm_2d(obj_1.as_array, obj_2.as_array) else None
            )
        else:
            raise NotImplementedError()

    @staticmethod
    def AABBCollision(obj_1: RectCollider, obj_2: RectCollider) -> Pos | None:
        def check(rect_1: Rect, rect_2: Rect) -> bool:
            return (
                rect_1.left <= rect_2.right
                and rect_1.right >= rect_2.left
                and rect_1.top <= rect_2.bottom
                and rect_1.bottom >= rect_2.top
            )

        rect_1, rect_2 = obj_1.rect, obj_2.rect
        collide = check(rect_1, rect_2) or check(rect_2, rect_1)
        return Pos(0, 0) if collide else None
