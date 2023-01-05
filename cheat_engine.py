from typing import Callable, List

from config import Config
from menu import Menu


class Cheat:
    """A single cheat, to be assigned to a cheat engine"""

    def __init__(self, game, code: List[str], callback: Callable):
        """Initialise the cheat

        :param game: The game which the cheat belongs to
        :param code: A string of key codes to be pressed to activate the cheat
        :type code: List[str]
        :param callback: The function to be called when this cheat is activated
        :type callback: Callable
        """
        self.game = game
        self.code = code
        self.callback = callback
        self.position = 0

    def on_key(self, event):
        """Handle a key press event

        :param event: The event that is being handled
        """
        if self.position < len(self.code):
            next_key = self.code[self.position]
            if event.keysym == next_key:
                self.position += 1
                if self.position == len(self.code):
                    self.callback()
                    self.position = 0
            else:
                self.position = 0
        return False


class InvincibilityCheat(Cheat):
    """Cheat that makes the player invincible"""

    def __init__(self, game, code: List[str]):
        """Initialise the cheat

        :param game: The game which this belongs to
        :param code: The combination of characters for which to
                     activate this cheat
        :type code: List[str]
        """
        super().__init__(game, code, self.toggle)
        self.enabled = False
        self.damage_function = None

    def toggle(self):
        """Enable or disable this cheat"""
        self.enabled = not self.enabled
        if self.enabled:
            self.game.effect_player.splash_text("Godmode on")
            self.game.player.set_image(self.game.player.white_image)
            self.damage_function = self.game.player.damage
            self.game.player.damage = (lambda: None)
        else:
            self.game.effect_player.splash_text("Godmode off")
            self.game.player.set_image(
                self.game.texture_factory.get_image("ship"))
            self.game.player.damage = self.damage_function


class DevModeCheat(Cheat):
    """Cheat that enables 'dev mode' which:
       - enables spawning menu
       - key to remove all enemies
       - key to stop spawning outright
    """

    def __init__(self, game, code: List[str]):
        """Initialise the cheat

        :param game: The game which this belongs to
        :param code: The combination of characters which activate this cheat
        :type code: List[str]
        """
        super().__init__(game, code, self.toggle)
        self.enabled = Config.DEVMODE

        self.spawning_disabled = False
        self.spawn_menu = Menu(self.game, "Spawn Menu")
        for i in ("circle_boss",
                  "snake_boss",
                  "loop",
                  "orbital",
                  "rectangle",
                  "fleet"):
            self.spawn_menu.add_item(i, self.spawn_item(i))

    def toggle(self):
        """Toggle if this mode is enabled"""
        self.enabled = not self.enabled
        if self.enabled:
            self.game.effect_player.splash_text("devmode on")
        else:
            self.game.effect_player.splash_text("devmode off")

    def spawn_item(self, name):
        """Spawn a named item from the menu

        :param name: The name of the formation to spawn
        """
        return lambda: (
            self.spawn_menu.hide(),
            getattr(self.game.formation_spawner, f"spawn_{name}")()
        )

    def on_key(self, event):
        """Handle Key press events

        :param event: The key press event to handle
        """
        if self.enabled:
            if event.keysym == "n":
                self.game.formation_spawner.clear_all()
                self.game.formation_spawner.next_phase()

            if event.keysym == "c":
                self.game.formation_spawner.clear_all()

            if event.keysym == "k":
                if self.spawning_disabled:
                    self.game.effect_player.splash_text("spawning on")
                    self.spawning_disabled = False
                    self.game.formation_spawner.next_formation = 0
                else:
                    self.game.effect_player.splash_text("spawning off")
                    self.game.formation_spawner.clear_all()
                    self.game.formation_spawner.next_formation = -1

            if event.keysym == "m":
                self.spawn_menu.show()

        return super().on_key(event)


class CheatEngine:
    """Object which manages cheats"""

    def __init__(self, game):
        """Initialise the cheat engine

        :param game: The game which this belongs to
        """
        self.game = game
        self.cheats = []

    def add_cheat(self, cheat):
        """Register a cheat to the engine

        :param cheat: The cheat to be registered
        """
        self.game.inputs.add_keypress_handler(cheat.on_key)
        self.cheats.append(cheat)
