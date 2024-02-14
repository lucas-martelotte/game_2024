from time import time

import pygame
from pygame.event import Event
from pygame.surface import Surface

from .collision import Collidable, Collider, CollisionDetector
from .utils import ClickState, MouseButtons, Pos


class Entity(Collidable):

    def __init__(self, position: Pos, fps: int):
        super().__init__()
        self.fps = fps
        self._position = position
        self._velocity = Pos(0, 0)
        self._acceleration = Pos(0, 0)
        self._mouse_button_state_dict: dict[MouseButtons, ClickState] = {
            button: ClickState.IDLE for button in MouseButtons
        }
        self._last_click_time_dict: dict[MouseButtons, float | None] = {
            button: None for button in MouseButtons
        }
        self._last_press_time_dict: dict[MouseButtons, float | None] = {
            button: None for button in MouseButtons
        }
        self._double_click_time = 0.5

    def get_surface(self) -> tuple[Surface, Pos]:
        raise NotImplementedError()

    def _get_colliders(self) -> set[Collider]:
        raise NotImplementedError()

    def get_colliders(self) -> set[Collider]:
        colliders = self._get_colliders()
        for collider in colliders:
            collider.set_position(self.position)
        return colliders

    def update(self):
        mouse_pos = Pos(*pygame.mouse.get_pos())
        if not self.point_collision(mouse_pos):
            self.reset_all_mouse_button_states()
        else:
            self._handle_hover()
        self.move(self.velocity)
        self.accelerate(self.acceleration)

    def on_event(self, event: Event) -> None:
        mouse_pos = Pos(*pygame.mouse.get_pos())
        if not self.point_collision(mouse_pos):
            self.reset_all_mouse_button_states()
            return
        match event.type:
            case pygame.MOUSEBUTTONDOWN:
                event_button = MouseButtons(event.button)
                self._handle_mouse_button_down(event_button)
            case pygame.MOUSEBUTTONUP:
                event_button = MouseButtons(event.button)
                self._handle_mouse_button_up(event_button)

    def point_collision(self, point: Pos) -> bool:
        return any(collider.point_collision(point) for collider in self.get_colliders())

    @property
    def position(self) -> Pos:
        return self._position

    @property
    def velocity(self) -> Pos:
        return self._velocity

    @property
    def acceleration(self) -> Pos:
        return self._acceleration

    def set_position(self, pos: Pos):
        difference = Pos.sub(pos, self._position)
        self.move(difference)

    def set_velocity_in_seconds(self, vel: Pos):
        """The input is assumed to be in pixels per second"""
        self._velocity = Pos(vel.x // self.fps, vel.y // self.fps)

    def set_velocity_in_frames(self, vel: Pos):
        """The input is assumed to be in pixels per frame"""
        self._velocity = vel

    def set_acceleration_in_seconds(self, acc: Pos):
        """The input is assumed to be in pixels per second squared"""
        self._acceleration = Pos(acc.x // self.fps**2, acc.y // self.fps**2)

    def set_acceleration_in_frames(self, acc: Pos):
        """The input is assumed to be in pixels per frame squared"""
        self._acceleration = acc

    def move(self, vector: Pos):
        self._position = Pos.add(self._position, vector)

    def accelerate(self, vector: Pos):
        self._velocity = Pos.add(self._velocity, vector)

    def _handle_mouse_button_down(self, button: MouseButtons):
        """This function assumes the mouse has collided"""
        last_press_time = self._last_press_time_dict[button]
        if self._is_under_double_click_time(last_press_time):
            self.set_mouse_button_state(button, ClickState.DOUBLE_PRESSED)
            self._last_press_time_dict[button] = None
        else:
            self.set_mouse_button_state(button, ClickState.PRESSED)
            self._last_press_time_dict[button] = time()

    def _handle_mouse_button_up(self, button: MouseButtons):
        """This function assumes the mouse has collided"""
        last_click_time = self._last_click_time_dict[button]
        if self._is_under_double_click_time(last_click_time):
            self.set_mouse_button_state(button, ClickState.DOUBLE_CLICKED)
            self._last_click_time_dict[button] = None
        else:
            self.set_mouse_button_state(button, ClickState.CLICKED)
            self._last_click_time_dict[button] = time()

    def _handle_hover(self):
        """This function assumes the mouse has collided"""
        for button in MouseButtons:
            if self.is_mouse_button_pressed(button):
                continue
            self.set_mouse_button_state(button, ClickState.HOVER)

    def _is_under_double_click_time(self, previous_time: float | None) -> bool:
        if previous_time is None:
            return False
        return time() - previous_time < self._double_click_time

    def reset_all_mouse_button_states(self):
        self._mouse_button_state_dict = {
            button: ClickState.IDLE for button in MouseButtons
        }

    def set_mouse_button_state(self, button: MouseButtons, state: ClickState):
        self._mouse_button_state_dict[button] = state

    def is_left_idle(self) -> bool:
        return self.check_button_state(MouseButtons.LEFT, ClickState.IDLE)

    def is_middle_idle(self) -> bool:
        return self.check_button_state(MouseButtons.MIDDLE, ClickState.IDLE)

    def is_right_idle(self) -> bool:
        return self.check_button_state(MouseButtons.RIGHT, ClickState.IDLE)

    def is_left_hover(self) -> bool:
        return self.check_button_state(MouseButtons.LEFT, ClickState.HOVER)

    def is_middle_hover(self) -> bool:
        return self.check_button_state(MouseButtons.MIDDLE, ClickState.HOVER)

    def is_right_hover(self) -> bool:
        return self.check_button_state(MouseButtons.RIGHT, ClickState.HOVER)

    def is_left_pressed(self) -> bool:
        return self.is_mouse_button_pressed(MouseButtons.LEFT)

    def is_middle_pressed(self) -> bool:
        return self.is_mouse_button_pressed(MouseButtons.MIDDLE)

    def is_right_pressed(self) -> bool:
        return self.is_mouse_button_pressed(MouseButtons.RIGHT)

    def is_left_clicked(self) -> bool:
        return self.is_mouse_button_clicked(MouseButtons.LEFT)

    def is_middle_clicked(self) -> bool:
        return self.is_mouse_button_clicked(MouseButtons.MIDDLE)

    def is_right_clicked(self) -> bool:
        return self.is_mouse_button_clicked(MouseButtons.RIGHT)

    def is_left_double_pressed(self) -> bool:
        return self.check_button_state(MouseButtons.LEFT, ClickState.DOUBLE_PRESSED)

    def is_middle_double_pressed(self) -> bool:
        return self.check_button_state(MouseButtons.MIDDLE, ClickState.DOUBLE_PRESSED)

    def is_right_double_pressed(self) -> bool:
        return self.check_button_state(MouseButtons.RIGHT, ClickState.DOUBLE_PRESSED)

    def is_left_double_clicked(self) -> bool:
        return self.check_button_state(MouseButtons.LEFT, ClickState.DOUBLE_CLICKED)

    def is_middle_double_clicked(self) -> bool:
        return self.check_button_state(MouseButtons.MIDDLE, ClickState.DOUBLE_CLICKED)

    def is_right_double_clicked(self) -> bool:
        return self.check_button_state(MouseButtons.RIGHT, ClickState.DOUBLE_CLICKED)

    def is_mouse_button_pressed(self, button: MouseButtons) -> bool:
        pressed = self.check_button_state(button, ClickState.PRESSED)
        double_pressed = self.check_button_state(button, ClickState.DOUBLE_PRESSED)
        return pressed or double_pressed

    def is_mouse_button_clicked(self, button: MouseButtons) -> bool:
        clicked = self.check_button_state(button, ClickState.CLICKED)
        double_clicked = self.check_button_state(button, ClickState.DOUBLE_CLICKED)
        return clicked or double_clicked

    def check_button_state(self, button: MouseButtons, state: ClickState) -> bool:
        return self._mouse_button_state_dict[button] == state
