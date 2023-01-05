from config import Config
from game import Game


class BossKey():
    """Object which manages the 'boss key' feature
       When a key is pressed, then the screen switches to a "work"
       related image
    """

    FG = "#ffaa00"
    BG = "#aaaaaa"
    BG2 = "#ffffff"
    FG2 = "#555555"
    TEXT_SIZE = 30

    def __init__(self, game: Game, pause_callback) -> None:
        """Initialises the boss key feature

        :param game: The game which to use
        :type game: Game
        :param pause_callback: The function to call to pause the game
        :rtype: None
        """
        self.game = game
        self.canvas = game.canvas
        self.width, self.height = game.w * Config.SCALE, game.h * Config.SCALE
        self.shapes = []
        self.game.inputs.add_keypress_handler(self.on_key)
        self.hidden = True
        self.pause_callback = pause_callback

    def on_key(self, event):
        """Handle key press events

        :param event: The key press event
        """
        if event.keysym == self.game.inputs.settings.boss \
                and self.hidden:
            self.pause_callback()
            self.create_shapes()
            self.hidden = False
            return True

        if not self.hidden:
            self.delete_shapes()
            self.hidden = True
            return True

        return False

    def create_rectangle(self, x, y, w, h, color):
        """Create a rectangle object

        :param x: x coordinate
        :param y: y coordinate
        :param w: width
        :param h: height
        :param color: The colour of the rectangle
        """
        self.shapes.append(self.canvas.create_rectangle(
            x, y, x+w, y+h, fill=color, state="disabled"))

    def write_text(self, x, y, text):
        """Create a text object

        :param x: x coordiante
        :param y: y coordinate
        :param text: The text used for this label
        """
        self.shapes.append(self.canvas.create_text(
            x, y, text=text, fill=BossKey.BG2,
            font=(f"Helvetica {BossKey.TEXT_SIZE} bold"), state="disabled"))

    def create_shapes(self):
        """Create all the shapes needed for the calculator"""
        width = self.width
        height = self.height
        padding = width // 50

        num_rows = 5
        num_cols = 4

        grid_width = width // num_cols
        grid_height = height // (num_rows+1)

        self.create_rectangle(0, 0, width, height, BossKey.BG)
        self.create_rectangle(padding,
                              padding,
                              width - padding*2,
                              grid_height-padding*2,
                              BossKey.FG2)

        symbols = [
            "(", ")", "%", "AC",
            "7", "8", "9", "/",
            "4", "5", "6", "x",
            "1", "2", "3", "-",
            "0", ".", "=", "+"
        ]
        for row in range(num_rows):
            for col in range(num_cols):
                color = BossKey.FG2
                if row == 0 or col == num_cols - 1:
                    color = BossKey.FG
                x = col*grid_width+padding
                y = row*grid_height+padding+grid_height
                w = grid_width-padding*2
                h = grid_height-padding*2
                self.create_rectangle(x, y, w, h, color)

                offset_x = x + padding + (
                    grid_width
                    - padding*2
                    - BossKey.TEXT_SIZE) // 2

                offset_y = y + padding + (
                    grid_height-padding * 2
                    - BossKey.TEXT_SIZE) // 2

                symbol = symbols[col + row*num_cols]
                self.write_text(offset_x, offset_y, symbol)

    def delete_shapes(self):
        """Remove all the shapes used for the calculator"""
        for shape in self.shapes:
            self.canvas.delete(shape)
