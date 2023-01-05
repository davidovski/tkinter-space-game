from random import randint, random
from tkinter import Canvas, PhotoImage, Tk
from typing import List

from config import Config
from font import Font
from frame_counter import FrameCounter
from inputs import InputController
from sprite import Sprite
from textures import TextureFactory


class Game:
    """A generic game object"""

    def __init__(self) -> None:
        """Initialise the game
        """
        self.win = Tk()
        game_width, game_height = (
            Config.WIDTH*Config.SCALE, Config.HEIGHT*Config.SCALE
        )
        self.w, self.h = Config.WIDTH, Config.HEIGHT

        self.win.geometry(f"{game_width}x{game_height}")
        self.canvas = Canvas(self.win, width=game_width,
                             height=game_height, bg="#000")
        self.canvas.pack()

        self.texture_factory = TextureFactory(scale=Config.SCALE)
        self.effect_player = EffectPlayer(self)
        self.frame_counter = FrameCounter(self.canvas, Config.FPS)

        self.inputs = InputController(self)
        self.sprites = []

        self.score = 0

        self.alpha = 0

    def start(self):
        """Start the game"""
        self.loop()
        self.win.mainloop()

    def tick(self):
        """Update the game's sprites"""
        for sprite in self.sprites:
            sprite.tick()
        self.effect_player.tick()

    def loop(self):
        """Loop the game at a set framerate"""
        self.alpha += 1
        self.tick()
        self.frame_counter.next_frame(self.loop)

    def clear_all(self):
        """Remove all game sprites"""
        for sprite in self.sprites:
            sprite.destroy()
        self.sprites = []


class GameSprite(Sprite):
    """A sprite which belongs to a game"""

    def __init__(self, game: Game, image: PhotoImage):
        """Initialise the sprite

        :param game: The game which this belongs to
        :type game: Game
        :param image: The image to use for the sprite
        :type image: PhotoImage
        """
        self.game = game
        super().__init__(game.canvas, image, (0, 0))

    def move(self, x, y):
        """Move the sprite by a certain amount

        :param x: Amount of pixels to move right
        :param y: Amount of pixels to move down
        """
        # if the object needs to move less than a pixel
        # only move it every few frames to create this effect
        if abs(x) >= 1:
            self.x += x
        elif x != 0:
            if self.game.alpha % (1/x) == 0:
                self.x += 1

        if abs(y) >= 1:
            self.y += y
        elif y != 0:
            if self.game.alpha % (1/y) == 0:
                self.y += 1

        self.update_position()


class GameEffect(GameSprite):
    """An effect that can be played within game"""

    def __init__(self, game: Game, image: PhotoImage,
                 duration=10, momentum=(0, 0)):
        """Initialise the game effect

        :param game: The game which this belongs to
        :type game: Game
        :param image: The image to use for this
        :type image: PhotoImage
        :param duration: How long this effect should last for
        :param momentum: Which direction to move this effect
        """
        self.start_time = game.alpha
        self.duration = duration
        self.velocity_x, self.velocity_y = momentum
        super().__init__(game, image)

    def tick(self):
        """Move the effect by its momentum and remove it if its over"""
        super().tick()
        self.move(self.velocity_x, self.velocity_y)

        alpha = self.game.alpha - self.start_time
        if self.duration != -1 and alpha > self.duration:
            self.destroy()


class AnimatedEffect(GameEffect):
    """An effect which involves animating an image"""

    def __init__(self, game: Game, images: List[PhotoImage],
                 frame_time=1, momentum=(0, 0)):
        """Initialise the effect

        :param game: The game which this belongs to
        :type game: Game
        :param images: The images to use for this animation
        :type images: List[PhotoImage]
        :param frame_time: Length of each frame of the animation
        :param momentum: Direction to move this effect
        """
        self.start_time = game.alpha
        self.frame_time = frame_time
        self.images = images
        self.frame_start = game.alpha
        super().__init__(game, images[0], duration=len(
            images)*frame_time, momentum=momentum)

    def tick(self):
        """Animate the effect"""
        super().tick()

        alpha = self.game.alpha - self.start_time

        i = int(alpha // self.frame_time)
        if i < len(self.images):
            self.set_image(self.images[i])
        else:
            self.destroy()


class EffectPlayer:
    """An object which concerns itself with managing the effects"""

    def __init__(self, game: Game) -> None:
        """Initialise the

        :param game: The game which this belongs to
        :type game: Game
        """
        self.sprites = []
        self.game = game
        self.explosion_frames = []
        self.star_image: PhotoImage

    def load_textures(self):
        """Load effect textures"""

        self.explosion_frames = [
            self.game.texture_factory.get_image(f"explosion{i+1}")
            for i in range(3)
        ]
        self.star_image = self.game.texture_factory.get_image("star")

    def tick(self):
        """Update all effects"""
        for sprite in self.sprites:
            sprite.tick()

        self.sprites = Sprite.remove_destroyed(self.sprites)

    def create_stars(self):
        """Initialise the stars in the background"""
        for _ in range(100):
            self.create_star(True)

    def create_star(self, new=False):
        """Add a star to the background

        :param new: Whether this star should be added at
                    the top of the screen or anywhere
        """
        x = randint(0, self.game.w)
        if new:
            y = randint(0, self.game.h)
        else:
            y = -1

        speed = randint(1, 4) * 0.1
        duration = 2*self.game.h / speed

        star = GameEffect(
            self.game,
            self.star_image,
            duration=int(duration),
            momentum=(0, speed)
        )
        star.set_pos((x, y))

        star.send_to_back()
        star.show()

        self.sprites.append(star)

    def create_explosion(self, position=(0, 0)):
        """Create an explosion effect

        :param position: location of the explosion
        """
        for _ in range(randint(1, 3)):
            m = ((random()*2)-1, (random()*2)-1)
            explosion_sprite = AnimatedEffect(
                self.game, self.explosion_frames, frame_time=5, momentum=m)
            explosion_sprite.set_pos(position)
            explosion_sprite.show()

            self.sprites.append(explosion_sprite)

    def splash_text(self, text, duration=50):
        """splash_text.

        :param text:
        :param duration:
        """
        text_img = Font.load_text(self.game.texture_factory, text)
        position = (
            (self.game.w-Font.FONT_WIDTH*len(text)) // 2,
            (self.game.h-Font.FONT_SIZE) // 3
        )

        text_sprite = GameEffect(
            self.game, text_img, duration=duration)
        text_sprite.set_pos(position)
        text_sprite.show()
        self.sprites.append(text_sprite)


class DamageableSprite(GameSprite):
    """Sprite with health points """

    def __init__(self, game: Game, image_name: str, hp=3):
        """Initialise the sprite

        :param game: The game which this belongs to
        :type game: Game
        :param image_name: The name of the image to use for this sprite
        :type image_name: str
        :param hp: The number of hit points this sprite spawns with
        """
        self.image = game.texture_factory.get_image(image_name)
        self.white_image = game.texture_factory.get_image(
            f"{image_name}:white")

        self.hp = hp
        self.animation_frame = 0

        super().__init__(game, self.image)

    def damage(self, amount=1):
        """Decrease number of hit points by an amount

        :param amount:
        """
        if not self.destroyed:
            self.hp -= amount
            self.animation_frame = 5
            if self.hp <= 0:
                self.hp = 0
                self.destroy()
                self.game.effect_player.create_explosion(self.get_pos())

    def tick(self):
        """Update the sprite"""
        super().tick()
        if self.animation_frame > 0:
            self.animation_frame -= 1
            if self.animation_frame % 2 == 0:
                self.set_image(self.image)
            else:
                self.set_image(self.white_image)


if __name__ == "__main__":
    print("!!!")
    print("This is not the main file!")
    print("Pleae run\n\tpython main.py\ninstead!")
    print("!!!")
