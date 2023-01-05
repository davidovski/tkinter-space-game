from dataclasses import dataclass
from os import path
from sys import stderr

from config import Config


@dataclass
class InputSettings:
    """Settings for keybinds"""

    down: str = "Down"
    left: str = "Left"
    up: str = "Up"
    right: str = "Right"
    action: str = "space"
    pause: str = "Escape"
    boss: str = "F9"

    def save_inputs(self):
        """Save keybinds to a file"""
        with open(Config.SETTINGS_FILE, "w", encoding="utf-8") as file:
            for key, value in vars(self).items():
                file.write(f"{key}: {value}\n")

    def load_inputs(self):
        """Load keybinds from a file"""
        if path.exists(Config.SETTINGS_FILE):
            with open(Config.SETTINGS_FILE, "r", encoding="utf-8") as file:
                for line in file.readlines():
                    split = line.strip().split(": ")
                    if len(split) == 2:
                        setattr(self, split[0], split[1])
                    else:
                        print(
                            f"Settings file corrupted? Invalid line {line}",
                            file=stderr
                            )


class InputController:
    """Object which listens to key inputs"""

    def __init__(self, game) -> None:
        """Initialise the input controller

        :param game: The game which this belongs to
        :rtype: None
        """
        game.win.bind('<KeyPress>', self.on_key_press)
        game.win.bind('<KeyRelease>', self.on_key_release)

        self.handlers = []

        self.settings = InputSettings()
        self.settings.load_inputs()

        self.k_down = False
        self.k_left = False
        self.k_up = False
        self.k_right = False
        self.k_action = False
        self.k_pause = False
        self.k_boss = False

    def on_key_press(self, e):
        """Handle Key press events

        :param e: The key press event to handle
        """
        if e.keysym == self.settings.left:
            self.k_left = True

        if e.keysym == self.settings.right:
            self.k_right = True

        if e.keysym == self.settings.up:
            self.k_up = True

        if e.keysym == self.settings.down:
            self.k_down = True

        if e.keysym == self.settings.action:
            self.k_action = True

        if e.keysym == self.settings.pause:
            self.k_pause = True

        for t, h in self.handlers:
            if t == "press" and h(e):
                break

    def on_key_release(self, e):
        """Handle Key release events


        :param e: The key press event to handle
        """
        if e.keysym == self.settings.left:
            self.k_left = False

        if e.keysym == self.settings.right:
            self.k_right = False

        if e.keysym == self.settings.up:
            self.k_up = False

        if e.keysym == self.settings.down:
            self.k_down = False

        if e.keysym == self.settings.action:
            self.k_action = False

        if e.keysym == self.settings.pause:
            self.k_pause = False

        for t, h in self.handlers:
            if t == "release" and h(e):
                break

    def add_keypress_handler(self, callback):
        """Register a key press listener

        :param callback:
        """
        self.handlers.insert(0, ("press", callback))

    def add_keyrelease_handler(self, callback):
        """Register a key release listener

        :param callback:
        """
        self.handlers.insert(0, ("release", callback))
