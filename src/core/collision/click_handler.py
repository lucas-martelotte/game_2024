from enum import Enum, auto
from time import time

import pygame
from pygame.event import Event

from ..utils import Pos, Rect


class ClickState(Enum):

    IDLE = auto()  # Nothing is happening
    HOVER = auto()  # Mouse is hovering
    PRESSED = auto()  # Mouse is currently pressing
    DOUBLE_PRESSED = auto()  # Mouse is currently pressing a double click
    CLICKED = auto()  # Mouse has just released
    DOUBLE_CLICKED = auto()  # Mouse has just released a double click


class ClickHandler(object):

    def __init__(self, rect: Rect, double_click_time: float = 0.5):
        self.rect = rect
        self._click_state: ClickState = ClickState.IDLE
        self._last_click_time: float | None = None
        self._last_press_time: float | None = None
        self._double_click_time = double_click_time

    @property
    def click_state(self) -> ClickState:
        return self._click_state

    def update(self):
        mouse_pos = Pos(*pygame.mouse.get_pos())
        if not self._mouse_collision(mouse_pos):
            self._click_state = ClickState.IDLE
            return
        self.handle_hover()

    def on_event(self, event: Event):
        mouse_pos = Pos(*pygame.mouse.get_pos())
        if not self._mouse_collision(mouse_pos):
            self._click_state = ClickState.IDLE
            return
        match event.type:
            case pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_button_down()
            case pygame.MOUSEBUTTONUP:
                self.handle_mouse_button_up()

    def handle_mouse_button_down(self):
        """This function assumes the mouse has collided"""
        if self._is_under_double_click_time(self._last_press_time):
            self._click_state = ClickState.DOUBLE_PRESSED
        else:
            self._click_state = ClickState.PRESSED
        self._last_press_time = time()

    def handle_mouse_button_up(self):
        """This function assumes the mouse has collided"""
        if self._is_under_double_click_time(self._last_click_time):
            self._click_state = ClickState.DOUBLE_CLICKED
        else:
            self._click_state = ClickState.CLICKED
        self._last_click_time = time()

    def handle_hover(self):
        """This function assumes the mouse has collided"""
        if self._click_state in [ClickState.PRESSED, ClickState.DOUBLE_PRESSED]:
            return
        self._click_state = ClickState.HOVER

    def _mouse_collision(self, mouse_pos: Pos) -> bool:
        return (
            self.rect.x <= mouse_pos.x <= self.rect.x + self.rect.width
            and self.rect.y <= mouse_pos.y <= self.rect.y + self.rect.height
        )

    def _is_under_double_click_time(self, previous_time: float | None) -> bool:
        if previous_time is None:
            return False
        return time() - previous_time < self._double_click_time
