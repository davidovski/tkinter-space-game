from dataclasses import dataclass
import math
from typing import List

from enemy import Enemy, EnemyAttributes
from game import Game
from sprite import Sprite


@dataclass
class FormationAttributes(EnemyAttributes):
    """FormationAttributes."""

    count: int = 1


class FormationEnemy(Enemy):
    """An enemy that belongs to a formation"""

    def __init__(self, game: Game, image_name, offset,
                 attributes: EnemyAttributes):
        """Initialise the enemy

        :param game: The game which this belongs to
        :type game: Game
        :param image_name: The name of the image to use for the enemy
        :param offset: The offset from the other enemies
        :param attributes: The attributes given to this enemy
        :type attributes: EnemyAttributes
        """
        self.offset_x, self.offset_y, self.offset_a = offset
        super().__init__(game, image_name, attributes)


class EnemyFormation:
    """Cluster of enemies that move in a particular way"""

    def __init__(self, game: Game, image_name: str,
                 enemy_attributes: FormationAttributes):
        """Initialise the formation

        :param game: The game which this belongs to
        :type game: Game
        :param image_name: The name of the image to use for the enemy
        :type image_name: str
        :param enemy_attributes: The attributes to use for spawned enemies
        :type enemy_attributes: FormationAttributes
        """
        self.game = game
        self.sprites: List[FormationEnemy] = []
        self.image_name = image_name

        self.alpha = 0
        self.attributes = enemy_attributes

        self.x, self.y = 0, 0
        self.destroyed = False

        self.create_enemies()
        self.hidden = True

    def create_enemies(self):
        """Spawn enemies"""
        pass

    def position_enemy(self, enemy: FormationEnemy):
        """Position a single enemy

        :param enemy: The enemy to position
        :type enemy: FormationEnemy
        """
        enemy.set_pos(
            (
                int(self.x + enemy.offset_x),
                int(self.y + enemy.offset_y)
            )
        )

    def spawn_enemy(self, offset):
        """Spawn a single enemy

        :param offset: The offset which to apply to the enemy
        """
        enemy = FormationEnemy(self.game, self.image_name,
                               offset, self.attributes)
        self.sprites.append(enemy)
        return enemy

    def tick(self, player):
        """Update the positions of all enemies

        :param player: The player to check if the enemies collide with
        """
        self.alpha += 1
        for enemy in self.sprites:
            enemy.tick(player)
            self.position_enemy(enemy)
        self.sprites = Sprite.remove_destroyed(self.sprites)
        if len(self.sprites) == 0:
            self.destroy()

    def destroy(self):
        """Delete all enemies in this formation"""
        for enemy in self.sprites:
            enemy.destroy()
        self.sprites = []
        self.destroyed = True

    def set_pos(self, pos):
        """Set the position of this formation

        :param pos: position to move to
        """
        self.x, self.y = pos

    def show(self):
        """Make this formation visible"""
        if self.hidden:
            for enemy in self.sprites:
                enemy.show()
            self.hidden = False

    def hide(self):
        """Make this formation hidden"""
        if not self.hidden:
            for enemy in self.sprites:
                enemy.hide()
            self.hidden = True


@dataclass
class CircleFormationAttributes(FormationAttributes):
    """Attributes for a circle formation"""

    radius: int = 40
    period: int = 300


class CircleFormation(EnemyFormation):
    """A circular formation of enemies, rotating in a ring"""

    def __init__(self, game: Game, image_name,
                 attributes: CircleFormationAttributes):
        """Initialise the formation

        :param game: The game which this belongs to
        :type game: Game
        :param image_name: The name of the image to use for the enemy
        :param attributes: The attributes to use for spawned enemies
        :type attributes: CircleFormationAttributes
        """
        super().__init__(game, image_name, attributes)
        self.attributes: CircleFormationAttributes

    def create_enemies(self):
        """Spawn all the enemies"""
        for i in range(self.attributes.count):
            self.spawn_enemy((0, 0, i))

    def position_enemy(self, enemy: FormationEnemy):
        """Position a single enemy

        :param enemy:
        :type enemy: FormationEnemy
        """
        a = (enemy.offset_a / self.attributes.count) * \
            self.attributes.period + self.game.alpha
        enemy.set_pos(
            (
                int(
                    self.x+math.sin((-a/self.attributes.period)
                                    * 2*math.pi) * self.attributes.radius
                ),
                int(
                    self.y+math.cos((-a/self.attributes.period)
                                    * 2*math.pi) * self.attributes.radius
                )
            )
        )


class LemniscateFormation(EnemyFormation):
    """An 'infinity' shape enemy formation"""

    def __init__(self, game: Game, image_name,
                 attributes: CircleFormationAttributes):
        """Initialise the formation

        :param game: The game which this belongs to
        :type game: Game
        :param image_name: The name of the image to use for the enemy
        :param attributes: The attributes to use for spawned enemies
        :type attributes: CircleFormationAttributes
        """
        super().__init__(game, image_name, attributes)
        self.attributes: CircleFormationAttributes

    def create_enemies(self):
        """Spawn all enemies"""
        for i in range(self.attributes.count):
            self.spawn_enemy((0, 0, (i / self.attributes.count)
                             * self.attributes.period * 0.25))

    def position_enemy(self, enemy: FormationEnemy):
        """Position an enemy

        :param enemy:
        :type enemy: FormationEnemy
        """
        a = enemy.offset_a + self.game.alpha

        t = (-a/self.attributes.period)*2*math.pi
        x = self.x+(self.attributes.radius * math.cos(t)) / \
            (1 + math.sin(t)**2)
        y = self.y+(self.attributes.radius * math.sin(t) * math.cos(t)) / \
            (1 + math.sin(t)**2)

        enemy.set_pos(
            (
                int(x),
                int(y)
            )
        )


@dataclass
class TriangleFormationAttributes(FormationAttributes):
    """Attributes for a triangular formation"""

    spacing: int = 16


class TriangleFormation(EnemyFormation):
    """A v-shaped formation of enemies"""

    def __init__(self, game: Game, image_name: str,
                 attributes: TriangleFormationAttributes):
        """Initialise the formation

        :param game: The game which this belongs to
        :type game: Game
        :param image_name: The name of the image to use for the enemy
        :type image_name: str
        :param attributes: The attributes to use for spawned enemies
        :type attributes: TriangleFormationAttributes
        """
        super().__init__(game, image_name, attributes)
        self.attributes: TriangleFormationAttributes

    def create_enemies(self):
        """Spawn all enemies in this formation"""
        for i in range(self.attributes.count):
            y = -((i+1) // 2)*self.attributes.spacing//2

            # first part is multiply by 1 or -1 to determine the side
            # then just have an offset for how far
            x = 2*((i % 2)-0.5) * ((i+1)//2)*self.attributes.spacing

            self.spawn_enemy((x, y, 1))


@dataclass
class RectangleFormationAttributes(TriangleFormationAttributes):
    """Attributes for a rectangle formation"""

    width: int = 5
    height: int = 2


class RectangleFormation(EnemyFormation):
    """A grid-like formation of enemies"""

    def __init__(self, game: Game, image_name,
                 attributes: RectangleFormationAttributes):
        """Initialise the formation

        :param game: The game which this belongs to
        :type game: Game
        :param image_name: The name of the image to use for the enemy
        :param attributes: The attributes to use for spawned enemies
        :type attributes: RectangleFormationAttributes
        """
        super().__init__(game, image_name, attributes)
        self.attributes: RectangleFormationAttributes

    def create_enemies(self):
        """Spawn all enemies"""
        full_width = self.attributes.width * self.attributes.spacing
        full_height = self.attributes.height * self.attributes.spacing

        for y in range(self.attributes.height):
            offset_y = ((y+0.5)*self.attributes.spacing)-(full_height/2)

            for x in range(self.attributes.width):
                offset_x = ((x+0.5)*self.attributes.spacing)-(full_width/2)
                self.spawn_enemy((offset_x, offset_y, 1))
