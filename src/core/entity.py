from abc import abstractmethod
from time import time

import pygame
from pygame.event import Event
from pygame.surface import Surface

from .utils import ClickState, Pos, Rect


class Entity:

    def __init__(self, rect: Rect):
        self.rect = rect
        self._click_state = ClickState.IDLE
        self._last_click_time: float | None = None
        self._last_press_time: float | None = None
        self._double_click_time = 0.5

    @property
    @abstractmethod
    def surface(self) -> Surface:
        pass

    @property
    def click_state(self) -> ClickState:
        return self._click_state

    def update(self):
        mouse_pos = Pos(*pygame.mouse.get_pos())
        if not self._mouse_collision(mouse_pos):
            self._click_state = ClickState.IDLE
            return
        self._handle_hover()

    def on_event(self, event: Event):
        mouse_pos = Pos(*pygame.mouse.get_pos())
        if not self._mouse_collision(mouse_pos):
            self._click_state = ClickState.IDLE
            return
        match event.type:
            case pygame.MOUSEBUTTONDOWN:
                self._handle_mouse_button_down()
            case pygame.MOUSEBUTTONUP:
                self._handle_mouse_button_up()

    def _handle_mouse_button_down(self):
        """This function assumes the mouse has collided"""
        if self._is_under_double_click_time(self._last_press_time):
            self._click_state = ClickState.DOUBLE_PRESSED
            self._last_press_time = None
        else:
            self._click_state = ClickState.PRESSED
            self._last_press_time = time()

    def _handle_mouse_button_up(self):
        """This function assumes the mouse has collided"""
        if self._is_under_double_click_time(self._last_click_time):
            self._click_state = ClickState.DOUBLE_CLICKED
            self._last_click_time = None
        else:
            self._click_state = ClickState.CLICKED
            self._last_click_time = time()

    def _handle_hover(self):
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

    def is_hovered(self) -> bool:
        return self.click_state == ClickState.HOVER

    def is_pressed(self) -> bool:
        return self.click_state == ClickState.PRESSED

    def is_double_pressed(self) -> bool:
        return self.click_state == ClickState.DOUBLE_PRESSED

    def was_clicked(self) -> bool:
        return self.click_state == ClickState.CLICKED

    def was_double_clicked(self) -> bool:
        return self.click_state == ClickState.DOUBLE_CLICKED
