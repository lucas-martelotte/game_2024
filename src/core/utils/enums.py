from enum import Enum, IntEnum, auto


class MouseButtons(IntEnum):
    """Numbers are specific to match with the pygame convention"""

    LEFT = 1
    MIDDLE = 2
    RIGHT = 3
    SCROLL_UP = 4
    SCROLL_DOWN = 5


class ClickState(Enum):

    IDLE = auto()  # Nothing is happening
    HOVER = auto()  # Mouse is hovering
    PRESSED = auto()
    CLICKED = auto()
    DOUBLE_PRESSED = auto()
    DOUBLE_CLICKED = auto()


class SceneTransitionState(Enum):
    IDLE = auto()  # No scene transition required
    CLOSE_AND_MOVE_TO_EXISTING_SCENE = auto()
    CLOSE_AND_MOVE_TO_NEW_SCENE = auto()
    MOVE_TO_EXISTING_SCENE = auto()
    MOVE_TO_NEW_SCENE = auto()
