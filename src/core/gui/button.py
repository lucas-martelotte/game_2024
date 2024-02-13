from pygame.surface import Surface

from .. import Entity
from ..collision.colliders import RectCollider
from ..utils import ClickState, MouseButtons, Pos, Rect


class Button(Entity):
    def __init__(
        self,
        collider: RectCollider,
        idle_sfc: Surface,
        pressed_sfc: Surface | None = None,
        hover_sfc: Surface | None = None,
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
        super().__init__(Pos.from_rect(collider.rect), collider)
        self.idle_sfc = idle_sfc
        self.pressed_sfc = pressed_sfc or idle_sfc
        self.hover_sfc = hover_sfc or idle_sfc

    def get_surface(self) -> tuple[Surface, Pos]:
        pos = Pos.from_rect(self.collider.bounding_rect)
        if self.is_left_idle():
            return self.idle_sfc, pos
        elif self.is_left_pressed():
            return self.pressed_sfc, pos
        else:
            return self.hover_sfc, pos
