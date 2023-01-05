import math
from random import choice, randint, random

from boss import CircleBossFormation, SnakeBossFormation
from enemy import EnemyAttributes
from formation import (
    CircleFormation,
    CircleFormationAttributes,
    EnemyFormation,
    FormationAttributes,
    LemniscateFormation,
    RectangleFormation,
    RectangleFormationAttributes,
    TriangleFormation,
    TriangleFormationAttributes,
)


def wobble_pattern(formation):
    """A sinusoidal movement pattern

    :param formation: Formation to move
    """
    x = (1+math.sin(formation.alpha/80)) * formation.game.w/2
    y = formation.y + (1 if formation.alpha % 4 == 0 else 0)
    formation.set_pos((x, y))


def speed_pattern(formation):
    """Quickly move the formation downwards

    :param formation: Formation to move
    """
    x = formation.x
    y = formation.y + 2
    formation.set_pos((x, y))


def slow_pattern(formation):
    """Slowly move the formation downwards

    :param formation: Formation to move
    """
    x = formation.x
    y = formation.y + (1 if formation.alpha % 8 == 0 else 0)
    formation.set_pos((x, y))


def slide_in_pattern(formation):
    """Slowly move into the center of the screen and then remain there

    :param formation: Formation to move
    """
    cy = formation.game.h//3

    if formation.alpha < 400:
        x = formation.x
        y = (formation.alpha/400) * (cy*1.5) - (cy*0.5)
    else:
        x = formation.x
        y = formation.y

    formation.set_pos((int(x), int(y)))


def no_pattern(formation):
    """No movement, stay in the center

    :param formation: Formation to move
    """
    formation.set_pos((
        formation.game.w // 2,
        formation.game.h // 3
    ))


def figure_of_eight_pattern(formation):
    """Move the formation in a figure of eight

    :param formation: Formation to move
    """
    period = 600
    edge = 8
    radius = formation.game.h//3 - edge
    cx, cy = formation.game.w//2, formation.game.h//3

    if formation.alpha < 200:
        x = formation.x
        y = (formation.alpha/200) * (cy*1.5) - (cy*0.5)
    else:
        a = formation.alpha - 200
        t = (a/period)*2*math.pi - math.pi/2

        y = cy + (radius * math.cos(t)) / (1 + math.sin(t)**2)
        x = cx + (radius * math.sin(t) * math.cos(t)) / (1 + math.sin(t)**2)

    formation.set_pos((int(x), int(y)))


class FormationSpawner():
    """Object to manage spawning of enemies and phases"""

    def __init__(self, game):
        """Initialise the formation spawner

        :param game: The game which this belongs to
        """
        self.game = game
        self.formations = []
        self.difficulty_multiplier = 0.5

        self.next_formation = 0

        self.phase = -1
        self.phases = [
            Phase("Phase:1", [
                  self.spawn_fleet,
                  self.spawn_loop,
                  self.spawn_orbital], 10),
            Phase("Boss:1", [self.spawn_circle_boss], 1),
            Phase("Phase:2", [
                  self.spawn_fleet,
                  self.spawn_loop,
                  self.spawn_orbital], 10, max_wave=3),
            Phase("Boss:2", [self.spawn_snake_boss], 1),
        ]

        self.to_spawn = 0
        self.current_reward = 1

    def tick(self):
        """Update all formations"""
        for formation, update in self.formations:
            formation.tick(self.game.player)
            update(formation)
            if formation.y > self.game.h:
                formation.destroy()
        self.formations = list(
            filter(lambda s: not s[0].destroyed, self.formations))

        self.spawn_next()

    def spawn_random(self):
        """Spawn a random formation"""
        options = [
            self.spawn_fleet,
            self.spawn_loop,
            self.spawn_orbital,
            self.spawn_rectangle
        ]
        choice(options)()

    def spawn_formation(self, formation: EnemyFormation, update):
        """Add a formation to the list of formations

        :param formation: Formation to add
        :type formation: EnemyFormation
        :param update: movement function to use for this formation
        """
        update(formation)
        formation.show()
        self.formations.append((formation, update))

    def spawn_circle_boss(self):
        """Spawn the circle boss"""
        attributes = EnemyAttributes(
            hp=int(15*self.difficulty_multiplier),
            reward=self.current_reward,
            cooldown=50
        )
        formation = CircleBossFormation(self.game, attributes)
        formation.set_pos((self.game.w//2, 0))
        update = figure_of_eight_pattern
        self.spawn_formation(formation, update)

    def spawn_snake_boss(self):
        """Spawn the snake boss"""
        attributes = FormationAttributes(
            hp=int(10*self.difficulty_multiplier),
            reward=self.current_reward,
            cooldown=160
        )

        formation = SnakeBossFormation(self.game, attributes)
        formation.set_pos((self.game.w//2, 0))
        update = slide_in_pattern
        self.spawn_formation(formation, update)

    def spawn_fleet(self):
        """Spawn the fleet formation"""
        sprite = randint(6, 7)

        position = (random()*self.game.w, -32)
        attributes = TriangleFormationAttributes(
            hp=int(self.difficulty_multiplier),
            cooldown=-1,
            reward=self.current_reward,
            count=randint(1, 3)*2 + 1,
            spacing=8
        )
        formation = TriangleFormation(
            self.game, f"smallenemy{sprite}", attributes)
        formation.set_pos(position)

        update = speed_pattern
        self.spawn_formation(formation, update)

    def spawn_orbital(self):
        """Spawn the orbital formation"""
        position = (random()*self.game.w, -32)
        sprite = choice((1, 3))

        attributes = CircleFormationAttributes(
            hp=int(self.difficulty_multiplier * 2),
            count=randint(3, 4)*2,
            radius=randint(10, 20),
            period=randint(100//int(self.difficulty_multiplier), 400),
            cooldown=80,
            reward=self.current_reward

        )

        formation = CircleFormation(
            self.game, f"smallenemy{sprite}", attributes)
        formation.set_pos(position)

        update = wobble_pattern
        formation.alpha = randint(1, 1000)
        self.spawn_formation(formation, update)

    def spawn_rectangle(self):
        """Spawn the rectangle formation"""
        sprite = choice((0, 2))
        position = (random() * self.game.w, -32)

        attributes = RectangleFormationAttributes(
            hp=int(self.difficulty_multiplier * 2),
            width=randint(4, 6),
            height=randint(2, 3),
            cooldown=80,
            reward=self.current_reward,
        )

        formation = RectangleFormation(
            self.game, f"smallenemy{sprite}", attributes
        )
        formation.set_pos(position)

        update = wobble_pattern
        formation.alpha = randint(1, 1000)
        self.spawn_formation(formation, update)

    def spawn_loop(self):
        """Spawn the loop formation"""
        sprite = choice((4, 5))
        position = (random()*self.game.w, -32)
        attributes = CircleFormationAttributes(
            count=randint(4, 8),
            radius=randint(self.game.w//2, self.game.w),
            period=randint(200, 300),
            hp=int(self.difficulty_multiplier),
            reward=self.current_reward,
            cooldown=160,
        )

        formation = LemniscateFormation(
            self.game, f"smallenemy{sprite}", attributes)
        formation.set_pos(position)

        update = slow_pattern
        self.spawn_formation(formation, update)

    def spawn_next(self):
        """Spawn the next formation to be spawned"""
        if self.to_spawn > 0:
            if len(self.formations) < self.current_phase().max_wave:
                if self.game.alpha > self.next_formation \
                        and self.next_formation != -1:
                    self.next_formation = self.game.alpha \
                            + 100 / self.difficulty_multiplier

                    self.current_phase().get_spawn_function()()
                    self.to_spawn -= 1
        else:
            if len(self.formations) == 0:
                self.next_phase()

    def next_phase(self):
        """Increment the phase by 1 and start the next phase"""
        self.phase += 1
        self.game.save_game()
        self.start_phase()

    def start_phase(self):
        """Start the next phase"""
        self.to_spawn = self.current_phase().duration

        self.difficulty_multiplier = (self.phase+2) * 0.5
        self.current_reward = int(2**self.difficulty_multiplier)

        self.next_formation = self.game.alpha + 100
        if self.current_phase().name:
            self.game.effect_player.splash_text(self.current_phase().name)

    def current_phase(self):
        """Return the current phase"""
        if self.phase < len(self.phases):
            return self.phases[self.phase]

        return Phase(f"Phase:{self.phase-1}", [
            self.spawn_random
        ], 10 * self.difficulty_multiplier,
            max_wave=int(self.difficulty_multiplier)
                     )

    def clear_all(self):
        """Remove all formation objects"""
        for f, _ in self.formations:
            f.destroy()


class Phase:
    """Rules for which formation will be spawned"""

    def __init__(self, name, spawn_functions, duration, max_wave=2):
        """__init__.

        :param name: The name of the phase
        :param spawn_functions:  A list of functions to use to spawn enemies
        :param duration: The number of formations to spawn
                         before the phase is over
        :param max_wave: The maximum number of formations to spawn at a time
        """
        self.spawn_functions = spawn_functions
        self.duration = duration
        self.name = name
        self.max_wave = max_wave

    def get_spawn_function(self):
        """Return a random spawn function"""
        return choice(self.spawn_functions)
