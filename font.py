class Font:
    """Convert a pixel font into photoimages"""

    FONT_SIZE = 5

    # effective width of each character, including letter spacing
    FONT_WIDTH = 6

    CHARS = {
        "\0": [
            "     ",
            "     ",
            "     ",
            "     ",
            "     ",
        ],
        "0": [
            " xxx ",
            "x  xx",
            "x x x",
            "xx  x",
            " xxx ",
        ],
        "1": [
            "  x  ",
            " xx  ",
            "  x  ",
            "  x  ",
            "xxxxx",
        ],
        "2": [
            "xxxx ",
            "    x",
            " xxx ",
            "x    ",
            "xxxxx",
        ],
        "3": [
            "xxxx ",
            "    x",
            "xxxx ",
            "    x",
            "xxxx ",
        ],
        "4": [
            "x   x",
            "x   x",
            "xxxxx",
            "    x",
            "    x",
        ],
        "5": [
            "xxxxx",
            "x    ",
            " xxx ",
            "    x",
            "xxxx ",
        ],
        "6": [
            " xxx ",
            "x    ",
            "xxxx ",
            "x   x",
            " xxx ",
        ],
        "7": [
            "xxxxx",
            "    x",
            "   x ",
            "  x  ",
            " x   ",
        ],
        "8": [
            " xxx ",
            "x   x",
            " xxx ",
            "x   x",
            " xxx ",
        ],
        "9": [
            " xxx ",
            "x   x",
            " xxxx",
            "    x",
            "    x",
        ],

        "a": [
            " xxx ",
            "x   x",
            "xxxxx",
            "x   x",
            "x   x",
        ],
        "b": [
            "xxxx ",
            "x   x",
            "xxxx ",
            "x   x",
            "xxxx ",
        ],
        "c": [
            " xxxx",
            "x    ",
            "x    ",
            "x    ",
            " xxxx",
        ],
        "d": [
            "xxxx ",
            "x   x",
            "x   x",
            "x   x",
            "xxxx ",
        ],
        "e": [
            "xxxxx",
            "x    ",
            "xxxxx",
            "x    ",
            "xxxxx",
        ],
        "f": [
            "xxxxx",
            "x    ",
            "xxxxx",
            "x    ",
            "x    ",
        ],
        "g": [
            " xxxx",
            "x    ",
            "x  xx",
            "x   x",
            " xxxx",
        ],
        "h": [
            "x   x",
            "x   x",
            "xxxxx",
            "x   x",
            "x   x",
        ],
        "i": [
            "xxxxx",
            "  x  ",
            "  x  ",
            "  x  ",
            "xxxxx",
        ],
        "j": [
            "xxxxx",
            "    x",
            "    x",
            "    x",
            "xxxx ",
        ],
        "k": [
            "x   x",
            "x  x ",
            "xxx  ",
            "x  x ",
            "x   x",
        ],
        "l": [
            "x    ",
            "x    ",
            "x    ",
            "x    ",
            "xxxxx",
        ],
        "m": [
            "x   x",
            "xx xx",
            "x x x",
            "x   x",
            "x   x",
        ],
        "n": [
            "x   x",
            "xx  x",
            "x x x",
            "x  xx",
            "x   x",
        ],
        "o": [
            " xxx ",
            "x   x",
            "x   x",
            "x   x",
            " xxx ",
        ],
        "p": [
            "xxxx ",
            "x   x",
            "xxxx ",
            "x    ",
            "x    ",
        ],
        "q": [
            " xxx ",
            "x   x",
            "x   x",
            "x  x ",
            " xx x",
        ],
        "r": [
            "xxxx ",
            "x   x",
            "xxxx ",
            "x   x",
            "x   x",
        ],
        "s": [
            " xxxx",
            "x    ",
            " xxx ",
            "    x",
            "xxxx ",
        ],
        "t": [
            "xxxxx",
            "  x  ",
            "  x  ",
            "  x  ",
            "  x  ",
        ],
        "u": [
            "x   x",
            "x   x",
            "x   x",
            "x   x",
            " xxx ",
        ],
        "v": [
            "x   x",
            "x   x",
            "x   x",
            " x x ",
            "  x  ",
        ],
        "w": [
            "x   x",
            "x   x",
            "x x x",
            "x x x",
            " x x ",
        ],
        "x": [
            "x   x",
            " x x ",
            "  x  ",
            " x x ",
            "x   x",
        ],
        "y": [
            "x   x",
            " x x ",
            "  x  ",
            "  x  ",
            "  x  ",
        ],
        "z": [
            "xxxxx",
            "   x ",
            "  x  ",
            " x   ",
            "xxxxx",
        ],
        " ": [
            "     ",
            "     ",
            "     ",
            "     ",
            "     ",
        ],
        ">": [
            " x   ",
            "  x  ",
            "   x ",
            "  x  ",
            " x   ",
        ],
        "<": [
            "   x ",
            "  x  ",
            " x   ",
            "  x  ",
            "   x ",
        ],
    }

    @staticmethod
    def _create_font_texture(text, color="#fff", letter_space=1):
        """Convert a font array into a game texture

        :param text: the characters used within the font
        :param color: The colour to use
        :param letter_space: The spacing between each letter to use
        """
        string = Font._create_characters(text, letter_space)
        return [
            [
                None if character == " " else color
                for character in row
            ] for row in string
        ]

    @staticmethod
    def _create_characters(text, letter_space):
        """Concatenate font symbols

        :param text: The text of the font
        :param letter_space: The spacing between each letter
        """
        # create a list of all characters in the string
        characters = [
            Font.CHARS[c] if c in Font.CHARS else Font.CHARS["\0"]
            for c in text.lower()
        ]

        # join each row of each character into one "character"
        return [
            (" "*letter_space).join([c[row] for c in characters])
            for row in range(Font.FONT_SIZE)
        ]

    @staticmethod
    def load_text(texture_factory, text, color="#fff", letter_space=1):
        """Create and load text into a photo image

        :param texture_factory: The texture factory used for processing
        :param text: The text to convert
        :param color: Color of the text
        :param letter_space: Spacing between letters
        """
        return texture_factory.load_texture(f"text:{text}",
                                            Font._create_font_texture(
                                                text,
                                                color=color,
                                                letter_space=letter_space)
                                            )
