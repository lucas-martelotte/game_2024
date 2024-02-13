from typing import NamedTuple


class Pos(NamedTuple):
    x: int
    y: int

    @staticmethod
    def add(pos1: "Pos", pos2: "Pos"):
        return Pos(pos1.x + pos2.x, pos1.y + pos2.y)

    @staticmethod
    def sub(pos1: "Pos", pos2: "Pos"):
        return Pos(pos1.x - pos2.x, pos1.y - pos2.y)

    @staticmethod
    def from_rect(rect: "Rect") -> "Pos":
        return Pos(rect.x, rect.y)


class Rect(NamedTuple):
    x: int
    y: int
    width: int
    height: int

    @staticmethod
    def move(rect: "Rect", vector: Pos) -> "Rect":
        return Rect(rect.x + vector.x, rect.y + vector.y, rect.width, rect.height)

    @property
    def left(self) -> int:
        return self.x

    @property
    def right(self) -> int:
        return self.x + self.width

    @property
    def top(self) -> int:
        return self.y

    @property
    def bottom(self) -> int:
        return self.y + self.height
