from src.core import Scene
from src.game import Control

if __name__ == "__main__":
    control = Control()
    control.set_active_scene(Scene())
    control.main_loop()
