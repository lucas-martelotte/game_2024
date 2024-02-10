import pygame

from src.core import Scene

from .singletons import GameSettings


class Control:
    def __init__(self) -> None:
        settings = GameSettings()
        screen_resolution = (settings.screen_width, settings.screen_height)
        self.screen = pygame.display.set_mode(screen_resolution)
        self.clock = pygame.time.Clock()
        self.active_scene: Scene | None = None

    def main_loop(self):
        if not self.active_scene:
            raise Exception("Error. Active scene is None.")
        while True:
            pygame.display.update()
            self.active_scene.update()
            self.clock.tick(GameSettings().fps)
            self.active_scene.render(self.screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                self.active_scene.on_event(event)

    def set_active_scene(self, scene: Scene):
        self.active_scene = scene
