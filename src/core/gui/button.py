from pygame.surface import Surface

from ..collision import ClickState
from ..entity import Entity
from ..utils import Rect


class Button(Entity):
    def __init__(
        self,
        click_rect: Rect,
        idle_sfc: Surface,
        hover_sfc: Surface | None = None,
        pressed_sfc: Surface | None = None,
    ):
        """
        Creates a new button.

        click_rect (Rect): the region which will detect clicks.
        idle_sfc (Surface): the default surface of the button
            hover_sfc (Surface | None, optional): the surface which will appear
            if the user is hovering over the button. If None, sets to idle_sfc.
        pressed_sfc (Surface | None, optional): the surface which will appear
            if the user is pressing the button. If None, sets to idle_sfc.
        """
        super().__init__(click_rect)
        self.idle_sfc = idle_sfc
        self.hover_sfc = hover_sfc or idle_sfc
        self.pressed_sfc = pressed_sfc or idle_sfc

    @property
    def surface(self) -> Surface:
        state = self.click_state
        if state in [ClickState.IDLE, ClickState.CLICKED, ClickState.DOUBLE_CLICKED]:
            return self.idle_sfc
        elif state in [ClickState.PRESSED, ClickState.DOUBLE_PRESSED]:
            return self.pressed_sfc
        elif state == ClickState.HOVER:
            return self.hover_sfc
        raise Exception(f"Invalid value for click state: {state.name}")