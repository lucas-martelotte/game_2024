import json

from src.core.utils import SingletonMetaclass


class GameSettings(metaclass=SingletonMetaclass):

    GAME_SETTINGS_PATH = "./src/config/game_settings.json"

    def __init__(self):
        with open(self.GAME_SETTINGS_PATH, "r") as f:
            config_dict = json.loads(f.read())
            self.screen_width = int(config_dict["screen_width"])
            self.screen_height = int(config_dict["screen_height"])
            self.fps = int(config_dict["fps"])
