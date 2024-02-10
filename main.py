import pygame

from src.game import Control

pygame.init()
pygame.font.init()
pygame.mixer.init()
pygame.display.set_caption("2024 Game")

if __name__ == "__main__":

    from pygame.surface import Surface

    from src.core import Scene
    from src.core.gui import Button
    from src.core.utils import ClickState, Rect

    idle_sfc = Surface((500, 200))
    idle_sfc.fill((255, 0, 0))
    hover_sfc = Surface((500, 200))
    hover_sfc.fill((0, 255, 0))
    pressed_sfc = Surface((500, 200))
    pressed_sfc.fill((0, 0, 255))
    button = Button(
        Rect(100, 100, 500, 200),
        idle_sfc,
        {ClickState.HOVER: hover_sfc, ClickState.PRESSED: pressed_sfc},
    )
    double_click = False

    class TestScene(Scene):
        def __init__(self):
            super().__init__("TEST")
            self.color = (255, 255, 255)

        def update(self):
            super().update()
            button.update()

        def on_event(self, event: pygame.Event):
            super().on_event(event)
            button.on_event(event)
            if button.is_right_double_pressed():
                self.color = (
                    (0, 0, 0) if self.color == (255, 255, 255) else (255, 255, 255)
                )

        def render(self, screen):
            super().render(screen)
            screen.fill(self.color)
            screen.blit(button.surface, button.rect)

    control = Control(TestScene())
    control.main_loop()
