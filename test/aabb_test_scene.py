from random import randint

import pygame
from pygame.surface import Surface

from src.core import Entity, Scene
from src.core.collision import Collidable, CollisionManager2D
from src.core.collision.colliders import PolygonCollider, RectCollider
from src.core.gui import Button
from src.core.utils import FPSTracker, Pos, Rect
from src.game.singletons import GameSettings


class AABBTestScene(Scene):
    def __init__(self) -> None:
        super().__init__("TEST")
        screen_width = GameSettings().screen_width
        screen_height = GameSettings().screen_height

        self.collision = False
        self.vector: Pos | None = None
        self.fps_tracker = FPSTracker()
        self.font = pygame.font.SysFont("Comic Sans MS", 30)

        idle_sfc = Surface((200, 200), pygame.SRCALPHA)
        pygame.draw.rect(idle_sfc, (0, 0, 255), (0, 0, 200, 200), width=10)
        self.fixed_button = Button(
            Pos(300, 300),
            GameSettings().fps,
            RectCollider(0, 0, 200, 200),
            idle_sfc,
        )

        idle_sfc = Surface((200, 200), pygame.SRCALPHA)
        pygame.draw.rect(idle_sfc, (255, 0, 0), (0, 0, 200, 200), width=10)
        self.mouse_button = Button(
            Pos(800, 800),
            GameSettings().fps,
            RectCollider(-100, -100, 200, 200),
            idle_sfc,
        )

        self.collision_manager = CollisionManager2D()
        self.collision_manager.add_collidables(
            frozenset({self.fixed_button, self.mouse_button})
        )

    def update(self):
        super().update()
        self.fps_tracker.update()
        self.mouse_button.set_position(Pos(*pygame.mouse.get_pos()))
        self.collision_manager.update()
        collisions = self.collision_manager.get_collisions()
        self.collision = len(collisions) > 0
        if self.collision:
            collision = list(collisions)[0]
            vector = collision.minimal_translation_vector
            self.vector = (
                vector if collision.obj_1 == self.mouse_button else Pos.inv(vector)
            )
        else:
            self.vector = None

    def on_event(self, event: pygame.Event):
        super().on_event(event)
        self.fixed_button.on_event(event)
        self.mouse_button.on_event(event)

    def render(self, screen):
        super().render(screen)
        screen.fill((255, 255, 255))
        # if self.collision:
        #     screen.fill((255, 0, 0))
        # else:
        #     screen.fill((255, 255, 255))
        sfc, pos = self.fixed_button.get_surface()
        screen.blit(sfc, pos)
        sfc, pos = self.mouse_button.get_surface()
        screen.blit(sfc, pos)
        text_surface = self.font.render(
            f"FPS: {round(self.fps_tracker.fps,2)}", False, (0, 0, 0)
        )
        screen.blit(text_surface, (10, 10))
        rect = self.fixed_button.collider.bounding_rect
        if self.vector is not None:
            pygame.draw.line(
                screen, (0, 255, 0), rect.center, Pos.add(rect.center, self.vector), 5
            )
            pygame.draw.circle(
                screen, (0, 255, 0), Pos.add(rect.center, self.vector), 10
            )

    def handle_button_reflections(self, button: Button):
        rect = button.collider.bounding_rect
        screen_width = GameSettings().screen_width
        screen_height = GameSettings().screen_height
        if rect.right >= screen_width or rect.left <= 0:
            button.set_velocity_in_frames(Pos(-button.velocity.x, button.velocity.y))
        if rect.bottom >= screen_height or rect.top <= 0:
            button.set_velocity_in_frames(Pos(button.velocity.x, -button.velocity.y))
