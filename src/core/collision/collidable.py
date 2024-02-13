from .collider import Collider


class Collidable:
    def __init__(self, collider: Collider):
        self._collider = collider

    @property
    def collider(self) -> Collider:
        return self._collider
