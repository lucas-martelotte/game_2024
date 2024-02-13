from ...utils import Pos, Rect
from ..collider import Collider


class RectCollider(Collider):
    def __init__(self, rect: Rect):
        self.rect = rect
        super().__init__()

    def point_collision(self, point: Pos) -> bool:
        return (
            self.rect.x <= point.x <= self.rect.x + self.rect.width
            and self.rect.y <= point.y <= self.rect.y + self.rect.height
        )

    def _calculate_bounding_rect(self) -> Rect:
        return self.rect

    def _move(self, translation_vector: Pos):
        self.rect = Rect.move(self.rect, translation_vector)
