from abc import ABC, abstractmethod
from time import time

from pygame.event import Event
from pygame.surface import Surface

from .collision import ClickHandler, ClickState
from .utils import Rect


class Entity(ABC):

    def __init__(self, rect: Rect):
        super().__init__()
        self.rect = rect
        self.click_handler = ClickHandler(rect)

    @property
    @abstractmethod
    def surface(self) -> Surface:
        pass

    @property
    def click_state(self) -> ClickState:
        return self.click_handler.click_state

    def update(self):
        self.click_handler.update()

    def on_event(self, event: Event):
        self.click_handler.on_event(event)
