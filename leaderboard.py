from os import path
from random import randint
from typing import List

from config import Config
from font import Font
from game import Game, GameSprite


class LeaderboardFile:
    """Object to manage saving and loading the leaderboard"""

    def __init__(self):
        """Initialise the leaderboard file"""
        self.entries = []

    def load_entries(self):
        """Load leaderboard entries from a file"""
        self.entries = []
        if path.exists(Config.LEADERBOARD_FILE):
            with open(Config.LEADERBOARD_FILE, "rb") as file:
                while (entry := file.read(8 + Config.NICK_LEN)):
                    name = entry[0:Config.NICK_LEN]
                    score = entry[Config.NICK_LEN:11]
                    score_entry = (name.decode("ascii"),
                                   int.from_bytes(score, byteorder="little"))
                    self.entries.append(score_entry)
            self.sort_entries()

    def sort_entries(self):
        """Sort leaderboard entries"""
        self.entries.sort(key=(lambda e: e[1]))
        self.entries.reverse()

    def save_entries(self):
        """Save leaderboard entries"""
        with open(Config.LEADERBOARD_FILE, "wb") as file:
            for name, score in self.entries:
                file.write(bytes(name[0:Config.NICK_LEN], "ascii"))
                file.write(int(score).to_bytes(8, "little"))

    def add_entry(self, name, score):
        """Add a leaderboard entry

        :param name: Initials of the player
        :param score: The sore that was achieved
        """
        self.entries.append((name, score))
        self.sort_entries()


class NameEntryLetter(GameSprite):
    """A single sprite used in a initial entry"""

    def __init__(self, game: Game, image, letter):
        """Initialise the letter

        :param game: The game which this belongs to
        :type game: Game
        :param image: The image to use for this
        :param letter: the letter to use
        """
        self.letter = letter
        super().__init__(game, image)


class NameEntry():
    """An initial entry element, allowing the user to enter their initials"""

    def __init__(self, game: Game, callback, num_letters=3, position=(0, 0)):
        """Initialise the name entry

        :param game: The game which this belongs to
        :type game: Game
        :param callback: callback to call when the entry is complete
        :param num_letters: Number of letters to use for the initials
        :param position: Position of this element
        """
        self.game = game
        self.callback = callback

        self.alphabet = [
            Font.load_text(game.texture_factory, c)
            for c in list(map(chr, range(97, 123)))
        ]

        self.letters: List[NameEntryLetter] = []
        self.selection = 0

        self.hidden = True

        self.populate_letters(num_letters)
        self.game.inputs.add_keypress_handler(self.on_key)
        self.set_pos(position)

    def populate_letters(self, num_letters):
        """Create sprites for each of the letters

        :param num_letters: Number of letters to use for initials
        """
        for _ in range(num_letters):
            sprite = NameEntryLetter(
                self.game,  self.alphabet[0], 0
            )
            self.letters.append(sprite)

        enter_image = Font.load_text(self.game.texture_factory, "enter")
        self.button = GameSprite(self.game, enter_image)
        self.w = self.button.w + (self.letters[0].w+1)*len(self.letters)
        self.h = Font.FONT_SIZE

    def on_key(self, _):
        """Handle Key press events


        :param _: The key press event to handle
        """
        inp = self.game.inputs
        if not self.hidden:
            if inp.k_action and self.selection == len(self.letters):
                self.callback(self.get_string())
                return True

            if inp.k_left:
                self.selection -= 1
                self.get_selected_letter().show()

            if inp.k_right or inp.k_action:
                self.get_selected_letter().show()
                self.selection += 1
                self.get_selected_letter().hide()

            self.selection %= len(self.letters) + 1

            if inp.k_up:
                self.modify_letter(-1)

            if inp.k_down:
                self.modify_letter(1)

            return True

        return False

    def get_string(self):
        """Get the initials entered"""
        return "".join(map(lambda l: chr(97 + l.letter), self.letters))

    def modify_letter(self, amount):
        """Increase or decrease a single character

        :param amount: number of letters to increment by
        """
        letter = self.get_selected_letter()
        if letter in self.letters:
            letter.letter += amount
            letter.letter %= len(self.alphabet)
            self.update_letter(letter)
            letter.show()

    def update_letter(self, letter):
        """Upare the image of a single letter

        :param letter: letter to update
        """
        letter.set_image(self.alphabet[letter.letter])

    def get_selected_letter(self):
        """Get the letter that has been selected"""
        if self.selection < len(self.letters):
            return self.letters[self.selection]

        return self.button

    def set_pos(self, pos):
        """set the element's position

        :param pos: position to move to
        """
        pos_x, pos_y = pos
        offset_x = 0
        for letter in self.letters:
            letter.set_pos((pos_x + offset_x, pos_y))
            offset_x += letter.w + 1
        offset_x += Font.FONT_SIZE

        self.button.set_pos((pos_x + offset_x, pos_y))

    def update_position(self):
        """Update the position of all the letters"""
        for letter in self.letters:
            letter.update_position()

    def show(self):
        """Make this object visible"""
        if self.hidden:
            for letter in self.letters:
                letter.show()
                letter.send_to_front()
            self.button.show()
            self.button.send_to_front()
            self.hidden = False

    def hide(self):
        """Make this object invisible"""
        if not self.hidden:
            for letter in self.letters:
                letter.hide()
            self.button.hide()
            self.hidden = True

    def tick(self):
        """Update the state of this object"""
        if not self.hidden:
            selected = self.get_selected_letter()
            for letter in self.letters + [self.button]:
                if self.game.alpha//15 == self.game.alpha / 15:
                    if letter == selected:
                        if (self.game.alpha//15) % 2 == 0:
                            self.get_selected_letter().show()
                        else:
                            self.get_selected_letter().hide()
                    else:
                        letter.show()
        else:
            self.hide()


class Leaderboard:
    """Leaderboard object to display previous scores"""

    ANIMATION_TIME = 5
    ANIMATION_DELAY = 5

    def __init__(self, game: Game):
        """Initialise the leaderboard

        :param game: The game which this belongs to
        :type game: Game
        """
        self.game = game
        self.file = LeaderboardFile()
        self.entries = []
        self.editing = True
        self.padding = 5

        self.callback = (lambda: None)

        self.hidden = True

        self.game.inputs.add_keypress_handler(self.on_key)
        self.name_entry = NameEntry(self.game, self.submit_name)

        self.blinking_sprite = None
        self.animation_start = -1

    def populate_entries(self, blink_entry=("", 0)):
        """Populate entries.

        :param blink_entry:
        """
        self.clear_entries()
        self.file.load_entries()

        editing_area = 0
        if self.editing:
            editing_area = Font.FONT_SIZE + self.padding*2
        remaining_area = self.game.h - self.padding*2 - editing_area

        to_fit = remaining_area // (Font.FONT_SIZE+self.padding) - 1

        to_draw = self.file.entries[0:to_fit]

        # create a row variable that is incremented for each entry
        y = self.padding

        # create the title sprite and increment the row
        image = Font.load_text(self.game.texture_factory, "leaderboard")
        sprite = GameSprite(self.game, image)
        sprite.set_pos((0, y))
        self.entries.append(sprite)
        x = (self.game.w - sprite.w) // 2
        sprite.set_pos((x, y))

        y += sprite.h + self.padding

        # calculate the number of zeros to pad the score by
        zfill = ((self.game.w-self.padding*2) //
                 (Font.FONT_SIZE+1)) - Config.NICK_LEN - 5
        for name, score in to_draw:
            text = f"{name}     {str(score).zfill(zfill)}"
            x = self.padding
            image = Font.load_text(self.game.texture_factory, text)
            sprite = GameSprite(self.game, image)
            sprite.set_pos((x, y))

            if (name, score) == blink_entry:
                self.blinking_sprite = sprite
            self.entries.append(sprite)

            y += sprite.h + self.padding

        if self.editing:
            self.name_entry.set_pos((self.padding, y+self.padding))
            self.name_entry.show()
        else:
            self.name_entry.hide()

    def start_animation(self):
        """Start the animation."""
        for e in self.entries:
            e.set_pos((-self.game.w, e.y))
        self.name_entry.hide()
        self.animation_start = self.game.alpha

    def on_key(self, _):
        """Handle Key press events

        :param _: The key press event to handle
        """
        inp = self.game.inputs
        if not self.hidden and inp.k_action and not self.editing:
            self.callback()
            return True

        return False

    def submit_name(self, name):
        """Submit a name to the leaderboard

        :param name:
        """
        score = self.game.score
        self.file.add_entry(name, score)
        self.file.save_entries()

        self.editing = False
        self.name_entry.hide()

        self.populate_entries(blink_entry=(name, score))
        self.start_animation()
        for e in self.entries:
            e.show()

    def animate_sprite(self, sprite, i):
        """Animate a single sprite.

        :param sprite:
        :param i:
        """
        alpha = self.game.alpha \
            - self.animation_start \
            - i*Leaderboard.ANIMATION_DELAY

        if alpha <= Leaderboard.ANIMATION_TIME:
            if i == 0:
                # only title should be h aligned
                cx = (self.game.w - sprite.w) // 2
            else:
                cx = self.padding

            x = (alpha/Leaderboard.ANIMATION_TIME) * \
                (cx+self.game.w//2) - self.game.w//2
            sprite.set_pos((x, sprite.y))

            return False
        return True

    def tick(self):
        """Update the leaderboard"""
        animation_complete = True
        for i, sprite in enumerate(self.entries):
            sprite.send_to_front()
            if not self.animate_sprite(sprite, i):
                animation_complete = False

        if self.editing:
            animation_time = self.game.alpha \
                - self.animation_start \
                - len(self.entries)*Leaderboard.ANIMATION_DELAY

            if animation_complete \
                    and animation_time > Leaderboard.ANIMATION_TIME:
                self.name_entry.show()
                self.name_entry.tick()
        else:
            if self.blinking_sprite is not None:
                if (self.game.alpha//15) % 2 == 0:
                    self.blinking_sprite.show()
                else:
                    self.blinking_sprite.hide()

    def show(self):
        """Make this object visible"""
        if self.hidden:
            for m in self.entries:
                m.show()
                m.send_to_front()

            self.hidden = False

    def hide(self):
        """Make this object invisible"""
        if not self.hidden:
            for m in self.entries:
                m.hide()
            self.name_entry.hide()
            self.hidden = True

    def start_editing(self):
        """Allow the user to input a name"""
        self.editing = True
        self.blinking_sprite = None

    def clear_entries(self):
        """Remove all the associated objects"""
        for entry in self.entries:
            entry.destroy()
        self.entries = []


# test to add entries to game leaderboard
if __name__ == "__main__":
    lb = LeaderboardFile()
    lb.load_entries()

    for input_name, input_score in lb.entries:
        print(f"{input_name} {input_score}")

    while True:
        input_name = input("Enter name or leave blank to exit: ")
        if input_name:
            input_score = input("enter score blank for random: ")
            if not input_score:
                input_score = randint(1, 999999)
            lb.add_entry(input_name, int(input_score))
        else:
            break

    for input_name, input_score in lb.entries:
        print(f"{input_name} {input_score}")

    lb.save_entries()
