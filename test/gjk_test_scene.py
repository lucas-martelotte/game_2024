from random import randint

import pygame
from pygame.surface import Surface

from src.core import Entity, Scene
from src.core.collision import Collidable, CollisionManager2D
from src.core.collision.colliders import PolygonCollider, RectCollider
from src.core.gui import Button
from src.core.utils import FPSTracker, Pos, Rect
from src.game.singletons import GameSettings


class GJKTestScene(Scene):
    def __init__(self) -> None:
        super().__init__("TEST")
        screen_width = GameSettings().screen_width
        screen_height = GameSettings().screen_height

        self.collision = False
        self.fps_tracker = FPSTracker()
        self.font = pygame.font.SysFont("Comic Sans MS", 30)

        polygon = [Pos(300, 300), Pos(300, 400), Pos(400, 600), Pos(400, 300)]
        collider = PolygonCollider(polygon)
        rect = collider.bounding_rect
        idle_sfc = Surface((rect.width, rect.height), pygame.SRCALPHA)
        relative_polygon = PolygonCollider(polygon)
        relative_polygon.move(Pos(-300, -300))
        pygame.draw.polygon(idle_sfc, (0, 0, 0), relative_polygon.points)
        self.fixed_button = Button(collider, GameSettings().fps, idle_sfc)

        polygon = [Pos(500, 500), Pos(550, 600), Pos(600, 600)]
        collider = PolygonCollider(polygon)
        rect = collider.bounding_rect
        idle_sfc = Surface((rect.width, rect.height), pygame.SRCALPHA)
        relative_polygon = PolygonCollider(polygon)
        relative_polygon.move(Pos(-500, -500))
        pygame.draw.polygon(idle_sfc, (0, 0, 0), relative_polygon.points)
        self.mouse_button = Button(collider, GameSettings().fps, idle_sfc)

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

    def on_event(self, event: pygame.Event):
        super().on_event(event)
        self.fixed_button.on_event(event)
        self.mouse_button.on_event(event)

    def render(self, screen):
        super().render(screen)
        if self.collision:
            screen.fill((255, 255, 255))
        else:
            screen.fill((255, 0, 0))
        sfc, pos = self.fixed_button.get_surface()
        screen.blit(sfc, pos)
        sfc, pos = self.mouse_button.get_surface()
        screen.blit(sfc, pos)
        text_surface = self.font.render(f"FPS: {self.fps_tracker}", False, (0, 0, 0))
        screen.blit(text_surface, (10, 10))

    def handle_button_reflections(self, button: Button):
        rect = button.collider.bounding_rect
        screen_width = GameSettings().screen_width
        screen_height = GameSettings().screen_height
        if rect.right >= screen_width or rect.left <= 0:
            button.set_velocity_in_frames(Pos(-button.velocity.x, button.velocity.y))
        if rect.bottom >= screen_height or rect.top <= 0:
            button.set_velocity_in_frames(Pos(button.velocity.x, -button.velocity.y))
