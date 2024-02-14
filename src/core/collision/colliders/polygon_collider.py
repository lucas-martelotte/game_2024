from numpy import array, ndarray

from ...utils import Pos, Rect
from ..collider import Collider


class PolygonCollider(Collider):
    def __init__(self, points: list[Pos]):
        assert len(points) >= 3
        # assert self.__is_convex(points)
        self._points = points
        self._points_array = array(points)
        super().__init__()

    def _move(self, translation_vector: Pos):
        """Translates itself by translation_vector"""
        self._points = [Pos.add(p, translation_vector) for p in self._points]
        self._points_array = array(self._points)

    def _point_collision(self, point: Pos) -> bool:
        """Detects if a point is colliding"""
        return False
        raise NotImplementedError()

    def _calculate_bounding_rect(self) -> Rect:
        left = min(p.x for p in self._points)
        right = max(p.x for p in self._points)
        top = min(p.y for p in self._points)
        bottom = max(p.y for p in self._points)
        return Rect(left, top, right - left, bottom - top)

    @property
    def points(self) -> list[Pos]:
        return self._points

    @property
    def as_array(self) -> ndarray:
        return self._points_array

    def __is_convex(self, points: list[Pos]) -> bool:
        raise NotImplementedError()
