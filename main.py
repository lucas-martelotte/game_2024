import pygame

from src.game import Control

pygame.init()
pygame.font.init()
pygame.mixer.init()
pygame.display.set_caption("2024 Game")

if __name__ == "__main__":
    from test.collision_test_scene import CollisionTestScene
    from test.test_scene import TestScene

    control = Control(CollisionTestScene())
    control.main_loop()
