from pygame.surface import Surface

from .. import Entity
from ..utils import ClickState, MouseButtons, Rect


class Button(Entity):
    def __init__(
        self,
        click_rect: Rect,
        idle_sfc: Surface,
        state_2_sfc: dict[ClickState, Surface],
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
        self.state_2_sfc = state_2_sfc

    @property
    def surface(self) -> Surface:
        state = self._mouse_button_state_dict[MouseButtons.LEFT]
        sfc = self.state_2_sfc.get(state, self.idle_sfc)
        return sfc
