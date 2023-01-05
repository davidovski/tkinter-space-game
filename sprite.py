from tkinter import Canvas, NW, PhotoImage

from config import Config


class Sprite:
    """Sprite."""

    @staticmethod
    def remove_destroyed(sprite_list):
        """Remove all destroyed sprites from a list

        :param sprite_list:
        :type sprite_list: list[Sprite]
        """
        return list(filter(lambda s: not s.destroyed, sprite_list))

    def __init__(self, canvas: Canvas, image: PhotoImage, position=(0, 0)):
        """Initialise the sprite class

        :param canvas: The canvas to draw the sprites to
        :type canvas: Canvas
        :param image: The image to be used for the sprite
        :type image: PhotoImage
        :param position: The default position to place the sprite
        """
        # set positions
        self.x, self.y = position

        self.canvas = canvas
        self.canvas_image = canvas.create_image(
            self.x * Config.SCALE, self.y * Config.SCALE,
            anchor=NW, image=image, state="hidden")

        # get pixel width and heigh ignoring scale
        self.w = image.width() // Config.SCALE
        self.h = image.height() // Config.SCALE

        self.destroyed = False
        self.hide()

    def update_position(self):
        """Move the image to the sprites position"""
        self.canvas.coords(self.canvas_image, self.x *
                           Config.SCALE, self.y*Config.SCALE)

    def set_pos(self, pos):
        """Set the player position

        :param pos: Position to move to
        """
        self.x, self.y = pos
        self.update_position()

    def get_pos(self):
        """Return the current position of the sprite"""
        return (self.x, self.y)

    def move(self, x, y):
        """Move the sprite by x and y

        :param x: the number of pixels right to move
        :param y: the number of pixels down to move
        """
        self.x += x
        self.y += y
        self.update_position()

    def collides(self, other):
        """Check if the sprite collides with another sprite

        :param other: The other sprite
        """
        return self.x < other.x + other.w \
            and self.x + self.w > other.x \
            and self.y < other.y + other.h \
            and self.h + self.y > other.y

    def collide_all(self, others):
        """Check if the sprite collides with a list of sprites

        :param others: Array of other sprites to check if collides with
        :returns:      index of the sprite that it collided with first
                       or -1 if not colliding
        """
        for i, other in enumerate(others):
            if self.collides(other):
                return i
        return -1

    def tick(self):
        """Update the sprite"""

    def destroy(self):
        """Remove the image from the canvas"""
        self.canvas.delete(self.canvas_image)
        self.destroyed = True

    def send_to_front(self):
        """Move the sprite to the foreground"""
        self.canvas.tag_raise(self.canvas_image)

    def send_to_back(self):
        """Move the sprite to the background"""
        self.canvas.tag_lower(self.canvas_image)

    def set_image(self, image: PhotoImage):
        """Change the image used by the sprite

        :param image: the image to set the sprite to
        :type image: PhotoImage
        """
        self.canvas.itemconfig(self.canvas_image, image=image)

    def show(self):
        """Set the sprite to be shown"""
        self.canvas.itemconfig(self.canvas_image, state="normal")
        return self

    def hide(self):
        """Set the sprite to be hidden"""
        self.canvas.itemconfig(self.canvas_image, state="hidden")
        return self

    def is_hidden(self):
        """Return True if the sprite is hidden"""
        return self.canvas.itemcget(self.canvas_image, "state") == "hidden"
