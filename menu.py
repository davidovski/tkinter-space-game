import re

from font import Font
from game import Game, GameSprite
from sprite import Sprite


class MenuItem(GameSprite):
    """A selectable item in a menu"""

    def __init__(self, game: Game, text, callback):
        """Initialise the item

        :param game: The game which this belongs to
        :type game: Game
        :param text: Text to display for this item
        :param callback: function to call when this item is selected
        """
        image = Font.load_text(game.texture_factory, text)
        self.text = text
        self.callback = callback
        super().__init__(game, image)

    def set_text(self, text):
        """Update the text of an entry

        :param text:
        """
        self.text = text
        image = Font.load_text(self.game.texture_factory, text)
        self.set_image(image)


class Menu():
    """Menu object with selectable entries"""

    def __init__(self, game: Game, title) -> None:
        """Initialise the menu object

        :param game: The game which this belongs to
        :type game: Game
        :param title: The title of this menu
        """
        self.game = game
        self.title = title
        self.padding = 5

        self.game.inputs.add_keypress_handler(self.on_key)

        self.menu_items = []

        self.selection = 0

        carret_image = Font.load_text(game.texture_factory, ">")
        self.carret = GameSprite(self.game, carret_image)

        title_image = Font.load_text(game.texture_factory, title)

        position = ((self.game.w - len(title)*Font.FONT_WIDTH)//2, 5*2)
        self.title = GameSprite(self.game, title_image)
        self.title.set_pos(position)

        self.hidden = True

        self.alpha = 0

    def on_key(self, _):
        """Handle Key press events


        :param event: The key press event to handle
        """
        if not self.hidden:
            inp = self.game.inputs

            if inp.k_down or inp.k_right:
                self.selection += 1

            if inp.k_up or inp.k_left:
                self.selection -= 1

            self.selection %= len(self.menu_items)
            self.update_carret()

            if inp.k_action:
                self.menu_items[self.selection].callback()

            return True

        return False

    def update_carret(self):
        """Move the carret to the correct location"""
        selected = self.menu_items[self.selection]
        x = selected.x - Font.FONT_SIZE
        y = selected.y
        self.carret.set_pos((x, y))

    def arrange_items(self):
        """Move the menu items to their correct positions"""
        cy = self.game.h // 2

        max_height = sum(item.h for item in self.menu_items
                         ) + self.padding*(len(self.menu_items)-1)
        top = cy - max_height//2

        y = top

        for item in self.menu_items:
            item_x = (self.game.w - item.w) // 2
            item_y = y
            y += item.h + self.padding
            item.set_pos((item_x, item_y))
        self.update_carret()

    def add_item(self, text: str, callback, index=-1):
        """Add a menu item

        :param text: Label of this item
        :type text: str
        :param callback: Function to call when it is selected
        :param index: Where to insert this item
        """
        if index == -1:
            index = len(self.menu_items)
        self.menu_items.insert(index, MenuItem(self.game, text, callback))
        self.arrange_items()

    def show(self):
        """Make this object visible"""
        if self.hidden:
            for m in self.menu_items:
                m.show()
                m.send_to_front()
            self.carret.show()
            self.carret.send_to_front()

            self.title.show()
            self.title.send_to_front()

            self.hidden = False

    def hide(self):
        """Make this object invisible"""
        if not self.hidden:
            for m in self.menu_items:
                m.hide()
            self.carret.hide()

            self.title.hide()

            self.hidden = True

    def tick(self):
        """Update this object"""
        self.alpha += 1
        if not self.hidden:
            if (self.alpha//15) % 2 == 0:
                self.carret.show()
            else:
                self.carret.hide()
        else:
            self.carret.hide()

    def has_item(self, text):
        """Return true if matching item is found

        :param text: Label text to match
        """
        for entry in self.menu_items:
            if entry.text == text:
                return True

        return False

    def get_item(self, regex) -> MenuItem:
        """Return an item that is matched

        :param regex: regular expression to match item text to
        :rtype: MenuItem
        """
        for entry in self.menu_items:
            if re.match(regex, entry.text):
                return entry

        return self.menu_items[0]

    def edit_item(self, regex, new_text):
        """Edit the text of a menu item

        :param regex: Regular expression to use to match the item's text to
        :param new_text: Text to replace to
        """
        for entry in self.menu_items:
            if re.match(regex, entry.text):
                entry.set_text(new_text)

        self.arrange_items()

    def del_item(self, text):
        """Remove an item

        :param text: Label text to match
        """
        for entry in self.menu_items:
            if entry.text == text:
                entry.destroy()
        self.menu_items = Sprite.remove_destroyed(self.menu_items)
        self.arrange_items()

        return False


class KeybindsMenu(Menu):
    """A menu for selecting keybinds on"""

    def __init__(self, game: Game, title):
        """Initialise the menu

        :param game: The game which this belongs to
        :type game: Game
        :param title: The title of this menu
        """
        super().__init__(game, title)
        self.key_selecting = ""

        image = Font.load_text(game.texture_factory, "press any key")
        self.press_key_sprite = GameSprite(self.game, image)
        self.press_key_sprite.set_pos(
            ((self.game.w - self.press_key_sprite.w) // 2, self.game.h // 2))

    def on_key(self, event):
        """Handle Key press events


        :param event: The key press event to handle
        """
        if self.key_selecting:
            key = event.keysym
            self.set_keybind(self.key_selecting, key)
            self.press_key_sprite.hide()
            self.show()
            return True
        return super().on_key(event)

    def set_keybind(self, name, key):
        """set_keybind.

        :param name:
        :param key:
        """
        setattr(self.game.inputs.settings, self.key_selecting, key)
        self.game.inputs.settings.save_inputs()
        self.key_selecting = ""
        self.edit_item(f"{name}\\s*<.*>", self.get_label(name, key))

    def select_keybind(self, keyname):
        """Allow the user to press a key to decide their keybind

        :param keyname:
        """
        self.hide()
        self.press_key_sprite.show()
        self.key_selecting = keyname

    def get_set_keybind(self, keyname):
        """Return a function that sets the keybind of a particular keyname

        :param keyname:
        """
        return lambda: self.select_keybind(keyname)

    def get_label(self, name, value):
        """Get a label for a keybind item

        :param name:
        :param value:
        """
        available_width = (self.game.w - Font.FONT_SIZE*2) // Font.FONT_WIDTH
        num_spaces = available_width - (len(name) + len(value) + 2) - 1
        spaces = " " * num_spaces
        return f"{name} {spaces}<{value}>"
