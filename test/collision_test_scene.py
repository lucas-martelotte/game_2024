from random import randint

import pygame
from pygame.surface import Surface

from src.core import Entity, Scene
from src.core.collision import Collidable, CollisionManager2D
from src.core.collision.colliders import PolygonCollider, RectCollider
from src.core.gui import Button
from src.core.utils import FPSTracker, Pos, Rect
from src.game.singletons import GameSettings


class CollisionTestScene(Scene):
    def __init__(self) -> None:
        super().__init__("TEST")

        self.fps_tracker = FPSTracker()
        self.font = pygame.font.SysFont("Comic Sans MS", 30)

        screen_width = GameSettings().screen_width
        screen_height = GameSettings().screen_height
        self.buttons: set[Button] = set()
        for i in range(350):
            width, height = randint(10, 20), randint(10, 20)
            x, y = randint(0, screen_width - width), randint(0, screen_height - height)
            velocity = Pos(randint(-5, 5), randint(-5, 5))
            idle_sfc = Surface((width, height))
            idle_sfc.fill((0, 0, 0))
            button = Button(
                Pos(x, y),
                GameSettings().fps,
                RectCollider(Rect(0, 0, width, height)),
                idle_sfc,
            )
            button.set_velocity_in_seconds(velocity)
            self.buttons.add(button)
        self.collision_manager = CollisionManager2D()
        self.collision_manager.add_collidables(frozenset(self.buttons))

    def update(self):
        super().update()
        self.fps_tracker.update()
        for button in self.buttons:
            button.update()
            self.handle_button_reflections(button)
        self.collision_manager.update()
        collisions = self.collision_manager.get_collisions()
        for button in self.buttons:
            sfc, _ = button.get_surface()
            sfc.fill((0, 0, 0))
        for collision in collisions:
            obj_1 = collision.obj_1
            obj_2 = collision.obj_2
            assert isinstance(obj_1, Button)
            assert isinstance(obj_2, Button)
            sfc_1, _ = obj_1.get_surface()
            sfc_2, _ = obj_2.get_surface()
            sfc_1.fill((255, 0, 0))
            sfc_2.fill((255, 0, 0))

    def on_event(self, event: pygame.Event):
        super().on_event(event)
        for button in self.buttons:
            button.on_event(event)

    def render(self, screen):
        super().render(screen)
        screen.fill((255, 255, 255))
        for button in self.buttons:
            sfc, pos = button.get_surface()
            screen.blit(sfc, pos)
        pygame.draw.rect(screen, (255, 255, 255), (5, 5, 160, 50))
        text_surface = self.font.render(
            f"FPS: {round(self.fps_tracker.fps, 2)}", False, (0, 0, 0)
        )
        screen.blit(text_surface, (10, 10))

    def handle_button_reflections(self, button: Button):
        rect = button.collider.bounding_rect
        screen_width = GameSettings().screen_width
        screen_height = GameSettings().screen_height
        if rect.right > screen_width:
            button.set_position(Pos(screen_width - rect.width, button.position.y))
            button.set_velocity_in_frames(Pos(-button.velocity.x, button.velocity.y))
        if rect.left < 0:
            button.set_position(Pos(0, button.position.y))
            button.set_velocity_in_frames(Pos(-button.velocity.x, button.velocity.y))
        if rect.bottom > screen_height:
            button.set_position(Pos(button.position.x, screen_height - rect.height))
            button.set_velocity_in_frames(Pos(button.velocity.x, -button.velocity.y))
        if rect.top < 0:
            button.set_position(Pos(button.position.x, 0))
            button.set_velocity_in_frames(Pos(button.velocity.x, -button.velocity.y))
