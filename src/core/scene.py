from pygame.event import Event
from pygame.surface import Surface

from .utils import SceneTransitionState


class Scene:
    def __init__(self, name: str):
        self.name = name
        self._transition_state = SceneTransitionState.IDLE
        self.next_scene: Scene | str | None = None  # Next scene to be executed

    @property
    def transition_state(self) -> SceneTransitionState:
        return self._transition_state

    def update(self):
        pass

    def on_event(self, event: Event):
        pass

    def render(self, screen: Surface):
        pass
