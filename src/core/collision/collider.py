from abc import ABC, abstractmethod

from ..utils import Pos, Rect


class Collider:
    def __init__(self):
        super().__init__()
        self._bounding_rect = self._calculate_bounding_rect()

    def move(self, translation_vector: Pos):
        """
        Translates itself and its own bounding
        rect by translation_vector
        """
        self._bounding_rect = Rect.move(self._bounding_rect, translation_vector)
        self._move(translation_vector)

    @abstractmethod
    def _move(self, translation_vector: Pos):
        """Translates itself by translation_vector"""
        pass

    @abstractmethod
    def point_collision(self, point: Pos) -> bool:
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
