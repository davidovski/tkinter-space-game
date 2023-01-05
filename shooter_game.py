from enum import Enum, auto
from os import path, remove
from random import random

from boss_key import BossKey
from cheat_engine import Cheat, CheatEngine, DevModeCheat, InvincibilityCheat
from config import Config
from formation_spawner import FormationSpawner
from game import Game
from hud import GameHud
from leaderboard import Leaderboard
from menu import KeybindsMenu, Menu
from shooter import Shooter, ShooterAttributes
from textures import Textures


class GameState(Enum):
    """Enum of possible game states"""

    MAIN_MENU = auto()
    GAME = auto()
    PAUSED = auto()
    END_LEADERBOARD = auto()
    LEADERBOARD = auto()
    SETTINGS = auto()


class GameSave:
    """Static class for saving and loading game"""

    @staticmethod
    def save_game(game):
        """Save game state to a file

        :param game: Game to save
        """

        phase = int.to_bytes(game.formation_spawner.phase, 2, "big")
        hp = int.to_bytes(game.player.hp, 1, "big")
        score = int.to_bytes(game.score, 8, "big")

        with open(Config.SAVE_FILE, "wb") as file:
            file.write(phase)
            file.write(hp)
            file.write(score)

        if not game.menu.has_item("Continue"):
            game.menu.add_item("Continue", game.restore_game, index=0)

    @staticmethod
    def load_game(game):
        """load game state from file

        :param game: Game to load
        """
        with open(Config.SAVE_FILE, "rb") as file:
            game.formation_spawner.phase = int.from_bytes(file.read(2), "big")
            game.player.hp = int.from_bytes(file.read(1), "big")
            game.score = int.from_bytes(file.read(8), "big")

    @staticmethod
    def remove_save(game):
        """Remove the game save file

        :param game:
        """
        if path.exists(Config.SAVE_FILE):
            remove(Config.SAVE_FILE)
            if game.menu.has_item("Continue"):
                game.menu.del_item("Continue")


class Player(Shooter):
    """Controllable player object"""

    def __init__(self, game: Game):
        """Initialise the player

        :param game: The game which this belongs to
        :type game: Game
        """
        attributes = ShooterAttributes(
            cooldown=12,
            velocity=-2,
            hp=10
        )

        super().__init__(game, "ship", attributes)
        self.set_pos(
            ((self.game.w - self.w) // 2, (self.game.h - self.h)))

    def tick(self):
        """Update this object"""
        super().tick()
        if self.game.inputs.k_left:
            self.move(-1, 0)
        if self.game.inputs.k_right:
            self.move(1, 0)
        if self.game.inputs.k_up:
            self.move(0, -1)
        if self.game.inputs.k_down:
            self.move(0, 1)

        # clamp the player to the screen
        if self.x < 0:
            self.set_pos((0, self.y))
        if self.y < 0:
            self.set_pos((self.x, 0))
        if self.x + self.w > self.game.w:
            self.set_pos((self.game.w - self.w, self.y))
        if self.y + self.h > self.game.h:
            self.set_pos((self.x, self.game.h - self.h))

        if self.game.inputs.k_action:
            self.shoot()


class ShooterGame(Game):
    """Game with menus and enemies to be shot at """

    def __init__(self):
        """Initialise the game"""
        super().__init__()

        self.state = GameState.MAIN_MENU
        self.death_time = -1
        self.paused_frame = 0

        # load textures
        Textures.load_textures(self.texture_factory)
        self.effect_player.load_textures()
        self.effect_player.create_stars()

        self.state = GameState.MAIN_MENU

        self.formation_spawner = FormationSpawner(self)

        self.player = Player(self)

        # make the game hud last to make sure its ontop
        self.game_hud = GameHud(self)

        # create the leaderboard sprites
        self.leaderboard = Leaderboard(self)
        self.leaderboard.callback = self.show_menu

        # make the settings menu
        self.settings_menu = KeybindsMenu(self, "Keybinds")
        for name, value in vars(self.inputs.settings).items():
            label = self.settings_menu.get_label(name, value)
            self.settings_menu.add_item(
                label,
                self.settings_menu.get_set_keybind(name)
            )
        self.settings_menu.add_item("Return", self.show_menu)

        # make the main menu
        self.menu = Menu(self, "Main Menu")
        if path.exists(Config.SAVE_FILE):
            self.menu.add_item("Continue", self.restore_game)
        self.menu.add_item("New Game", self.start_game)
        self.menu.add_item("Leaderboard", self.show_leaderboard)
        self.menu.add_item("Settings", self.show_settings)
        self.menu.show()

        # make the pause menu
        self.pause_menu = Menu(self, "Game Paused")
        self.pause_menu.add_item("Resume", self.resume_game)

        self.pause_menu.add_item("Save", lambda: (
            self.save_game(),
            self.effect_player.splash_text("Game saved"),
            self.resume_game())
        )

        self.pause_menu.add_item("Exit", self.show_menu)

        # initialise cheats
        self.cheat_engine = CheatEngine(self)
        self.cheat_engine.add_cheat(
            Cheat(self, list("test"),
                  (lambda: self.effect_player.splash_text("test ok"))
                  ))

        self.cheat_engine.add_cheat(
            Cheat(self, [
                "Up",
                "Up",
                "Down",
                "Down",
                "Left",
                "Right",
                "Left",
                "Right",
                "b",
                "a",
            ],
                (lambda: [self.formation_spawner.spawn_rectangle()
                 for _ in range(20)])
            ))

        self.cheat_engine.add_cheat(DevModeCheat(self, [
            "Left",
            "Right",
            "Left",
            "Right",
            "Escape",
            "d",
            "Up",
            "t",
            "b",
            "b",
            "a",
            "b",
            "s"
        ]))

        self.cheat_engine.add_cheat(InvincibilityCheat(self, list("xyzzy")))

        self.boss_key = BossKey(self, self.pause_game)

    def tick(self):
        """Update the game state"""
        if self.state != GameState.PAUSED:
            super().tick()

            if random() > 0.9:
                self.effect_player.create_star()

        if self.state == GameState.MAIN_MENU:
            self.menu.tick()
        elif self.state == GameState.SETTINGS:
            self.settings_menu.tick()
        elif self.state == GameState.GAME:
            self.tick_game()
        elif self.state == GameState.PAUSED:
            self.alpha = self.paused_frame
            self.pause_menu.tick()
        elif self.state == GameState.END_LEADERBOARD:
            self.leaderboard.tick()
        elif self.state == GameState.LEADERBOARD:
            self.leaderboard.tick()

    def tick_game(self):
        """Update the game during game play"""
        self.game_hud.tick()
        self.formation_spawner.tick()
        self.player.tick()

        if self.player.destroyed:
            if self.death_time == -1:
                self.death_time = self.alpha
                self.effect_player.splash_text("GAME OVER", 100)
            elif self.alpha - self.death_time > 100:
                self.show_score()

        if self.inputs.k_pause:
            self.pause_game()

    def pause_game(self):
        """Set the game to paused state"""
        if self.state == GameState.GAME:
            self.state = GameState.PAUSED

            self.paused_frame = self.alpha
            self.pause_menu.show()

    def resume_game(self):
        """Resume the game from paused state"""
        self.state = GameState.GAME

        self.pause_menu.hide()

    def start_game(self):
        """Start a new game"""
        self.state = GameState.GAME

        GameSave.remove_save(self)

        self.menu.hide()
        self.pause_menu.hide()
        self.formation_spawner.phase = -1
        self.clear_all()

        self.score = 0
        self.player = Player(self)

        self.formation_spawner.next_phase()

        self.player.show()
        self.game_hud.show()

        self.death_time = -1

    def show_leaderboard(self):
        """Show the game's leaderboard"""
        self.state = GameState.LEADERBOARD

        self.menu.hide()
        self.pause_menu.hide()
        self.leaderboard.editing = False
        self.leaderboard.populate_entries()
        self.leaderboard.start_animation()

        self.leaderboard.show()

    def show_score(self):
        """Allow the user to enter their name into the leaderboard"""
        self.state = GameState.END_LEADERBOARD

        self.clear_all()
        self.game_hud.hide()
        self.leaderboard.editing = True
        self.leaderboard.populate_entries()
        self.leaderboard.start_animation()
        self.leaderboard.show()
        GameSave.remove_save(self)

    def show_menu(self):
        """Show the main menu"""
        self.state = GameState.MAIN_MENU

        self.clear_all()
        self.leaderboard.hide()
        self.game_hud.hide()
        self.player.hide()
        self.pause_menu.hide()
        self.settings_menu.hide()

        self.menu.show()

    def clear_all(self):
        """Remove all the associated game objects"""
        self.formation_spawner.clear_all()
        self.player.destroy()

    def restore_game(self):
        """Restore the game's state from file"""
        self.state = GameState.GAME

        self.menu.hide()
        self.pause_menu.hide()
        self.clear_all()

        self.player = Player(self)
        self.death_time = -1

        GameSave.load_game(self)

        self.formation_spawner.start_phase()
        self.game_hud.show()
        self.player.show()

    def save_game(self):
        """Save the game's state to a file"""
        GameSave.save_game(self)

    def show_settings(self):
        """Show the keybind setting menu"""
        self.state = GameState.SETTINGS

        self.menu.hide()
        self.settings_menu.show()
