from random import randint

import pygame
from pygame.surface import Surface

from src.core import Entity, Scene
from src.core.collision import Collidable, CollisionManager2D
from src.core.collision.colliders import RectCollider
from src.core.gui import Button
from src.core.utils import Pos, Rect
from src.game.singletons import GameSettings


class CollisionTestScene(Scene):
    def __init__(self) -> None:
        super().__init__("TEST")
        screen_width = GameSettings().screen_width
        screen_height = GameSettings().screen_height
        self.buttons: set[Button] = set()
        for i in range(500):
            width, height = randint(10, 20), randint(10, 20)
            x, y = randint(0, screen_width - width), randint(0, screen_height - height)
            velocity = Pos(randint(-5, 5), randint(-5, 5))
            idle_sfc = Surface((width, height))
            idle_sfc.fill((0, 0, 0))
            button = Button(RectCollider(Rect(x, y, width, height)), idle_sfc)
            button.set_velocity(velocity)
            self.buttons.add(button)
        self.collision_manager = CollisionManager2D()
        self.collision_manager.add_collidables(frozenset(self.buttons))

    def update(self):
        super().update()
        for button in self.buttons:
            button.update()
            self.handle_button_reflections(button)
        self.collision_manager.update()
        collisions = self.collision_manager.get_collisions()
        for button in self.buttons:
            sfc, _ = button.get_surface()
            sfc.fill((0, 0, 0))
        for obj_1, obj_2, vec in collisions:
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

    def handle_button_reflections(self, button: Button):
        rect = button.collider.bounding_rect
        screen_width = GameSettings().screen_width
        screen_height = GameSettings().screen_height
        if rect.right >= screen_width or rect.left <= 0:
            button.set_velocity(Pos(-button.velocity.x, button.velocity.y))
        if rect.bottom >= screen_height or rect.top <= 0:
            button.set_velocity(Pos(button.velocity.x, -button.velocity.y))
