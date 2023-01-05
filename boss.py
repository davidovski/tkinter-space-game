from dataclasses import replace
import math

from enemy import EnemyAttributes
from formation import (
    CircleFormation,
    CircleFormationAttributes,
    EnemyFormation,
    FormationAttributes,
    FormationEnemy,
)
from game import Game


class CircleBossFormation(EnemyFormation):
    """Enemy Formation for the circular game boss"""

    RADIUS = 10
    CYCLE_PEROID = 500
    COUNT = 6

    def __init__(self, game: Game, attributes: EnemyAttributes):
        """Initialise the circle boss

        :param game: The game which this boss belongs to
        :type game: Game
        :param attributes: The attributes on which to base spawned enemies
        :type attributes: EnemyAttributes
        """
        self.image_name = "enemy0"
        self.minion_image_name = "smallenemy0"

        self.alpha = 0

        attributes = CircleFormationAttributes(
            radius=40,
            period=300,
            count=CircleBossFormation.COUNT,
            velocity=attributes.velocity,
            cooldown=attributes.cooldown,
            hp=attributes.hp//2,
            reward=attributes.reward*10
        )
        self.circle_formation = CircleFormation(
            game, self.minion_image_name, attributes)

        super().__init__(game, self.image_name, attributes)

    def create_enemies(self):
        """Spawn the boss"""
        self.spawn_enemy((-4, -4, 0))

    def tick(self, player):
        """Update the boss's position

        :param player: The player which to check collision with
        :type player: Player
        """
        super().tick(player)
        self.circle_formation.x = self.x
        self.circle_formation.y = self.y
        a = (self.alpha/CircleBossFormation.CYCLE_PEROID)*2*math.pi - math.pi

        r = 50*math.sin(a) - 25

        p = math.sin(a*2)*100

        self.circle_formation.attributes.radius = math.floor(
            CircleBossFormation.RADIUS + (r if r > 0 else 0)
        )

        self.circle_formation.attributes.period = math.floor(
            400 + (p if p < 100 else 100)
        )

        self.circle_formation.tick(player)

        # When the boss is dead, the minions will all die
        if len(self.sprites) == 0:
            if len(self.circle_formation.sprites) > 0:
                self.circle_formation.sprites[0].damage()
            else:
                self.destroy()

    def destroy(self):
        """Remove the circle boss"""
        super().destroy()
        self.circle_formation.destroy()

    def hide(self):
        """Hide the circle boss"""
        self.circle_formation.hide()
        return super().hide()

    def show(self):
        """Show the circle boss"""
        self.circle_formation.show()
        return super().show()


class SnakeBossFormation(EnemyFormation):
    """Enemy formation for the snake boss"""

    LENGTH = 32

    def __init__(self, game: Game, attributes: FormationAttributes):
        """Initialise the snake boss

        :param game: The game which the boss belongs to
        :type game: Game
        :param attributes: The attributes of which to base spawned enemies on
        :type attributes: FormationAttributes
        """
        self.minion_name = "smallenemy1"
        self.tail_name = "smallenemy1_evil"
        self.head_name = "enemy2"

        self.phase = 1
        self.phase_timer = 0

        super().__init__(game, self.minion_name, attributes)

    def create_enemies(self):
        """Spawn the snake"""
        head_attributes = replace(self.attributes)
        head_attributes.hp *= 100
        self.head = FormationEnemy(self.game, self.head_name,
                                   (0, 0, 0), head_attributes)

        self.sprites.append(self.head)

        for i in range(SnakeBossFormation.LENGTH):
            self.spawn_enemy((0, 0, i+1))

        tail_attributes = replace(self.attributes)
        head_attributes.hp //= 5
        self.tail = FormationEnemy(self.game, self.tail_name,
                                   (0, 0, SnakeBossFormation.LENGTH+1),
                                   tail_attributes)

        self.sprites.append(self.tail)

    def spawn_enemy(self, offset):
        """Spawn one enemy unit of the snake

        :param offset: The offset of the enemy
        """
        attributes = replace(self.attributes)
        if offset[2] % 6 == 0:
            attributes.cooldown = 40
        else:
            attributes.cooldown = -1

        enemy = FormationEnemy(self.game, self.image_name, offset, attributes)
        self.sprites.append(enemy)
        return enemy

    def position_enemy(self, enemy: FormationEnemy):
        """Position the enemy on the game screen

        :param enemy: The enemy to position
        :type enemy: FormationEnemy
        """
        if self.phase == 2:
            p = 120 / (100 + math.cos(self.phase_timer / 400)*20) * 120
        else:
            p = 120

        m = 4
        t = ((-enemy.offset_a*m) + self.game.alpha) / p + math.pi
        a = self.game.w // 2
        b = self.game.h // 3
        c = 0

        if self.phase == 2:
            n = 10 - (2000 / (self.phase_timer+2000))*5
        else:
            n = 5

        enemy.set_pos((
            int(self.x + a*math.sin(n*t+c)),
            int(self.y + b*math.sin(t))
        ))

    def tick(self, player):
        """Update the position of the enemies

        :param player: The player which to check collision with
        """
        super().tick(player)

        if self.phase == 1:
            self.head.hp = self.attributes.hp*100
            if self.tail.destroyed:
                if len(self.sprites) > 1:
                    self.sprites[-1].damage(amount=(self.attributes.hp//4))
                else:
                    self.head.hp = self.attributes.hp * 3
                    self.phase = 2
        elif self.phase == 2:
            self.phase_timer += 1
            self.head.attributes.cooldown = int(
                20 + math.sin(self.phase_timer / 50)*10)
