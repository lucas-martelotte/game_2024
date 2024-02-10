import pygame

from src.core import Scene
from src.core.utils import SceneTransitionState

from .singletons import GameSettings


class Control:
    def __init__(self, initial_scene: Scene) -> None:
        settings = GameSettings()
        screen_resolution = (settings.screen_width, settings.screen_height)
        self.screen = pygame.display.set_mode(screen_resolution)
        self.clock = pygame.time.Clock()
        self.active_scene = initial_scene
        self.scene_dict = {initial_scene.name: initial_scene}

    def main_loop(self):
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
            self.handle_scene_transition()

    def set_active_scene(self, scene: Scene):
        self.active_scene = scene

    def handle_scene_transition(self):
        scene = self.active_scene
        match scene.transition_state:
            case SceneTransitionState.CLOSE_AND_MOVE_TO_EXISTING_SCENE:
                assert isinstance(scene.next_scene, str)
                del self.scene_dict[scene.name]
                self.active_scene = self.scene_dict[scene.next_scene]
            case SceneTransitionState.CLOSE_AND_MOVE_TO_NEW_SCENE:
                assert isinstance(scene.next_scene, Scene)
                del self.scene_dict[scene.name]
                self.active_scene = scene.next_scene
                self.scene_dict[self.active_scene.name] = self.active_scene
            case SceneTransitionState.MOVE_TO_EXISTING_SCENE:
                assert isinstance(scene.next_scene, str)
                self.active_scene = self.scene_dict[scene.next_scene]
            case SceneTransitionState.MOVE_TO_NEW_SCENE:
                assert isinstance(scene.next_scene, Scene)
                self.active_scene = scene.next_scene
                self.scene_dict[self.active_scene.name] = self.active_scene
