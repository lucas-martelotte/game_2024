from dataclasses import dataclass

from src.core.utils import Pos

from .collidable import Collidable
from .collider import Collider


@dataclass(unsafe_hash=False, kw_only=True, frozen=True)
class PreCollision:
    obj_1: Collidable
    collider_1: Collider
    obj_2: Collidable
    collider_2: Collider

    def __eq__(self, other: object) -> bool:
        """
        Two pre collisions are equal if they have the same
        two pairs (obj, collider), independent of order.
        For example, the following data is considered equal:
            (obj_1, collider_1, obj_2, collider_2)
            is equal to
            (obj_2, collider_2, obj_1, collider_1)
        """
        if not isinstance(other, PreCollision):
            return False
        if self.obj_1 == other.obj_1:
            return (
                self.collider_1 == other.collider_1
                and self.obj_2 == other.obj_2
                and self.collider_2 == other.collider_2
            )
        elif self.obj_1 == other.obj_2:
            return (
                self.collider_1 == other.collider_2
                and self.obj_2 == other.obj_1
                and self.collider_2 == other.collider_1
            )
        return False

    def __hash__(self) -> int:
        return hash((self.obj_1, self.collider_1)) + hash((self.obj_2, self.collider_2))


@dataclass(unsafe_hash=False, kw_only=True, frozen=True)
class Collision(PreCollision):
    minimal_translation_vector: Pos

    @classmethod
    def from_pre_collision(
        cls, pre_collision: PreCollision, minimal_translation_vector: Pos
    ):
        return cls(
            obj_1=pre_collision.obj_1,
            collider_1=pre_collision.collider_1,
            obj_2=pre_collision.obj_2,
            collider_2=pre_collision.collider_2,
            minimal_translation_vector=minimal_translation_vector,
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Collision):
            return False
        if not super().__eq__(other):
            return False
        return self.minimal_translation_vector == other.minimal_translation_vector

    def __hash__(self) -> int:
        return hash((hash(super()), self.minimal_translation_vector))
