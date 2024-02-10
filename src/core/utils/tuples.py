from typing import NamedTuple


class Pos(NamedTuple):
    x: int
    y: int


class Rect(NamedTuple):
    x: int
    y: int
    width: int
    height: int
