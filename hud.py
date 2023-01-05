from game import Game, GameSprite
from font import Font


class ScoreCounterSprite(GameSprite):
    """Single digit for a score counter"""

    def __init__(self, game: Game):
        """Initialise the score counter

        :param game: The game which this belongs to
        :type game: Game
        """
        self.number_images = []

        self.x = 0

        for i in range(10):
            self.number_images.append(
                Font.load_text(game.texture_factory, str(i)))

        super().__init__(game, self.number_images[0])

    def update_image(self):
        """Update the digit"""
        self.set_image(self.number_images[int(self.x % 10)])

    def set(self, x):
        """Set the image

        :param x: number to set this digit to
        """
        self.x = x
        self.update_image()


class ScoreCounter:
    """Sprite to display a number"""

    def __init__(self, game: Game, num_digits, position=(0, 0)) -> None:
        """__init__.

        :param game:
        :type game: Game
        :param num_digits:
        :param position:
        :rtype: None
        """
        self.digits = []
        x, y = position

        self.number = 0

        for i in range(num_digits):
            sprite = ScoreCounterSprite(game)
            sprite.set_pos((x+(Font.FONT_SIZE + 1)*i, y))
            self.digits.append(sprite)

    def set(self, number):
        """Set the score to be displayed

        :param number:
        """
        if number != self.number:
            self.number = number
            power = 10**len(self.digits)
            for digit in self.digits:
                power /= 10
                digit.set((number // power) % 10)

    def destroy(self):
        """Remove this counter"""
        for n in self.digits:
            n.destroy()

    def send_to_front(self):
        """Move this counter to the foreground"""
        for d in self.digits:
            d.send_to_front()

    def show(self):
        """Make this counter visible"""
        for d in self.digits:
            d.show()

    def hide(self):
        """Make this counter invisible"""
        for d in self.digits:
            d.hide()


class GameHud:
    """Object to manage the items visible in the game's heads up display"""

    SCORE_DIGITS = 8
    HP_DIGITS = 2

    def __init__(self, game) -> None:
        """Initialise the HUD

        :param game: The game which this belongs to
        """

        self.game = game
        self.score_counter = ScoreCounter(game, GameHud.SCORE_DIGITS,
                                          position=(
                                              game.w
                                              - GameHud.SCORE_DIGITS
                                              * (Font.FONT_SIZE+1),
                                              1)
                                          )

        self.hp_symbol = GameSprite(game, game.player.image)
        self.hp_symbol.set_pos((1, 1))

        x_image = Font.load_text(game.texture_factory, "x")
        self.x_symbol = GameSprite(game, x_image)
        self.x_symbol.set_pos((self.hp_symbol.x+self.hp_symbol.w+1, 1))

        self.hp_counter = ScoreCounter(game, GameHud.HP_DIGITS,
                                       position=(self.x_symbol.x+1 +
                                                 self.x_symbol.w, 1)
                                       )

        self.items = (self.score_counter,
                      self.hp_symbol,
                      self.x_symbol,
                      self.hp_counter)

    def tick(self):
        """Update the hud"""
        self.score_counter.set(self.game.score)
        self.hp_counter.set(
            self.game.player.hp if self.game.player.hp > 0 else 0)

        for x in self.items:
            x.send_to_front()

    def destroy(self):
        """Remove all the associated objects"""
        for x in self.items:
            x.destroy()

    def hide(self):
        """Make this object invisible"""
        for x in self.items:
            x.hide()

    def show(self):
        """Make this object visible"""
        for x in self.items:
            x.show()
