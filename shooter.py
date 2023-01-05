from dataclasses import dataclass
from typing import List

from game import DamageableSprite, Game, GameSprite
from sprite import Sprite


class Lazer(GameSprite):
    """Lazer object that is shot by a shooter"""

    def __init__(self, game: Game, velocity=-4, color="white"):
        """Initialise the lazer

        :param game: The game which this belongs to
        :type game: Game
        :param velocity: Velocity to move the lazer at
        :param color: name of the colour of the lazer
        """
        self.velocity = velocity
        self.game = game
        super().__init__(game, game.texture_factory.get_image(
            f"lazer:{color}"))

    def tick(self):
        """Update this object"""
        self.move(0, self.velocity)
        if self.y + self.h > self.game.h or self.y < 0:
            self.destroy()


@dataclass
class ShooterAttributes:
    """Attributes for a shooter object"""

    lazer_color: str = "white"
    cooldown: int = 40
    velocity: int = 1
    hp: int = 3


class Shooter(DamageableSprite):
    """A game object that is able to shoot lazers"""

    def __init__(self, game: Game,
                 image_name: str, attributes: ShooterAttributes):
        """Initialise the shooter

        :param game: The game which this belongs to
        :type game: Game
        :param image_name: The name of the image to use for this sprite
        :type image_name: str
        :param attributes: The attributes to use for this object
        :type attributes: ShooterAttributes
        """
        super().__init__(game, image_name, hp=attributes.hp)
        self.lazers: List[Lazer] = []
        self.attributes = attributes
        self.last_shot = self.game.alpha

    def shoot(self):
        """Soot a lazer if possible"""
        next_shot = self.last_shot + self.attributes.cooldown

        if not self.destroyed \
                and self.game.alpha > next_shot:
            self.last_shot = self.game.alpha

            lazer = Lazer(self.game,
                          velocity=self.attributes.velocity,
                          color=self.attributes.lazer_color)
            lazer.set_pos((self.x + self.w//2 - 1, self.y +
                          self.h//2 - 1))
            lazer.show()
            self.lazers.append(lazer)

    def tick(self):
        """Update this object"""
        super().tick()
        for lazer in self.lazers:
            lazer.tick()

        self.lazers = Sprite.remove_destroyed(self.lazers)

    def destroy(self):
        """Remove all the associated objects"""
        super().destroy()
        for lazer in self.lazers:
            self.game.sprites.append(lazer)
