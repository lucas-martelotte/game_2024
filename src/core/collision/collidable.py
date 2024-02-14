from abc import ABC, abstractmethod

from .collider import Collider


class Collidable(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def get_colliders(self) -> set[Collider]:
        pass
