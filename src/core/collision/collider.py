from abc import ABC, abstractmethod

from ..utils import Pos, Rect


class Collider:
    def __init__(self):
        super().__init__()
        self._bounding_rect = self._calculate_bounding_rect()
        self._position = Pos(0, 0)

    @property
    def position(self) -> Pos:
        return self._position

    def set_position(self, position: Pos):
        translation_vector = Pos.sub(position, self._position)
        self.move(translation_vector)

    def move(self, translation_vector: Pos):
        """
        Translates itself and its own bounding
        rect by translation_vector
        """
        self._position = Pos.add(self._position, translation_vector)
        self._bounding_rect = Rect.move(self._bounding_rect, translation_vector)
        self._move(translation_vector)

    def point_collision(self, point: Pos) -> bool:
        rect = self.bounding_rect
        collides_with_rect = (
            rect.left <= point.x <= rect.right and rect.top <= point.y <= rect.bottom
        )
        if not collides_with_rect:
            return False
        return self._point_collision(point)

    @abstractmethod
    def _move(self, translation_vector: Pos):
        """Translates itself by translation_vector"""
        pass

    @abstractmethod
    def _point_collision(self, point: Pos) -> bool:
        """Detects if a point is colliding"""
        pass

    @abstractmethod
    def _calculate_bounding_rect(self) -> Rect:
        pass

    @property
    def bounding_rect(self) -> Rect:
        return self._bounding_rect


class ComplexCollider(Collider):
    """A collider represeting a set of individual colliders"""

    def __init__(self, colliders: set[Collider]):
        super().__init__()
        self.colliders = colliders

    def move(self, translation_vector: Pos):
        for collider in self.colliders:
            collider.move(translation_vector)

    def point_collision(self, point: Pos) -> bool:
        return any(collider.point_collision(point) for collider in self.colliders)

    def __calculate_bounding_rect(self):
        raise NotImplementedError()
