from enum import Enum, auto


class ClickState(Enum):

    IDLE = auto()  # Nothing is happening
    HOVER = auto()  # Mouse is hovering
    PRESSED = auto()  # Mouse is currently pressing
    DOUBLE_PRESSED = auto()  # Mouse is currently pressing a double click
    CLICKED = auto()  # Mouse has just released
    DOUBLE_CLICKED = auto()  # Mouse has just released a double click


class SceneTransitionState(Enum):
    IDLE = auto()  # No scene transition required
    CLOSE_AND_MOVE_TO_EXISTING_SCENE = auto()
    CLOSE_AND_MOVE_TO_NEW_SCENE = auto()
    MOVE_TO_EXISTING_SCENE = auto()
    MOVE_TO_NEW_SCENE = auto()