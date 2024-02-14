from typing import override

from ...utils import Pos, Rect
from .polygon_collider import PolygonCollider


class RectCollider(PolygonCollider):
    def __init__(self, rect: Rect):
        self.rect = rect
        super().__init__(
            [rect.top_left, rect.bottom_left, rect.bottom_right, rect.top_right]
        )

    @override
    def _point_collision(self, point: Pos) -> bool:
        # At this point, collision already failed for bounding rect
        return False

    @override
    def _calculate_bounding_rect(self) -> Rect:
        return self.rect

    def _move(self, translation_vector: Pos):
        super()._move(translation_vector)
        self.rect = Rect.move(self.rect, translation_vector)
