from dataclasses import dataclass


@dataclass
class Config:
    """Various constants and configuration for the game"""

    WIDTH = 100
    HEIGHT = 200
    # Number of window pixels used for each game "pixel"
    SCALE = 6

    FPS = 30

    NICK_LEN = 3
    DEVMODE = False

    LEADERBOARD_FILE = "leaderboard"
    SAVE_FILE = "save"
    SETTINGS_FILE = "settings"
