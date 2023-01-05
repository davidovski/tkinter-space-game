from dataclasses import dataclass

from game import Game
from shooter import Shooter, ShooterAttributes


@dataclass
class EnemyAttributes(ShooterAttributes):
    """Attributes of an enemy object"""

    reward: int = 100
    lazer_color: str = "red"
    cooldown: int = 20


class Enemy(Shooter):
    """An enemy in the game"""

    def __init__(self, game: Game, image_name: str,
                 attributes: EnemyAttributes):
        """Initialise the enemy

        :param game: The game which this belongs to
        :type game: Game
        :param image_name: The name of the image to use
        :type image_name: str
        :param attributes: The attributes of this
        :type attributes: EnemyAttributes
        """
        super().__init__(game, image_name, attributes)
        self.attributes = attributes

    def tick(self, player):
        """Check for collisions and shoot

        :param player: The player which to check collisions with
        """
        super().tick()
        if self.attributes.cooldown != -1:
            self.shoot()

        lazer_collisions = self.collide_all(player.lazers)
        if lazer_collisions != -1:
            self.damage()
            player.lazers[lazer_collisions].destroy()

        player_collisions = player.collide_all(self.lazers)
        if player_collisions != -1:
            player.damage()
            self.lazers[player_collisions].destroy()

        if self.collides(player):
            player.damage()
            self.damage()

    def damage(self, amount=1):
        """Reduce the object's health

        :param amount:
        """
        super().damage(amount)
        if self.destroyed:
            self.game.score += self.attributes.reward
