from pygame.surface import Surface

from ..collision import Collider
from ..entity import Entity
from ..utils import InGameEntityState, Pos


class Sprite(Entity):
    def __init__(
        self,
        position: Pos,
        fps: int,
        frames_per_image: int,
        schema: dict[InGameEntityState, list[tuple[Surface, Pos, frozenset[Collider]]]],
    ):
        super().__init__(position, fps)
        self._frames_per_image = frames_per_image
        self._current_image_frame = 0
        self._waited_frames = 0
        self._schema = schema
        self._state_to_number_of_images = {k: len(v) for k, v in schema.items()}
        self._state = InGameEntityState.IDLE

    def get_surface(self) -> tuple[Surface, Pos]:
        sfc, pos, _ = self._schema[self._state][self._current_image_frame]
        return sfc, pos

    def _get_colliders(self) -> frozenset[Collider]:
        _, _, colliders = self._schema[self._state][self._current_image_frame]
        return colliders

    def update(self):
        super().update()
        self._waited_frames = (self._waited_frames + 1) % self._frames_per_image
        if self._waited_frames == 0:
            n_frames = self._state_to_number_of_images[self._state]
            self._current_image_frame = (self._current_image_frame + 1) % n_frames

    def set_state(self, state: InGameEntityState):
        self._state = state

    @property
    def state(self) -> InGameEntityState:
        return self._state
