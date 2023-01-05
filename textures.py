from tkinter import PhotoImage


# tell pylint to ignore long lines in this file, since they make more sense
# to not be linewrapped
#
#   ignore a particular guideline "when applying the guideline would make the code less readable"
# https://peps.python.org/pep-0008
#
# pylint: disable=line-too-long
class Textures:
    """Static class containing game textures"""
    STAR = [
            ["#AAAAAA"]
            ]

    ENEMY = [
    [
        [None,      "#00E436", "#008751", "#008751", None,      None,      None,     ],
        ["#00E436", "#00E436", "#00E436", None,      None,      "#008751", None,     ],
        ["#008751", "#00E436", "#00E436", None,      None,      "#00E436", "#008751",],
        [None,      "#008751", "#008751", None,      "#00E436", "#00E436", "#008751",],
        [None,      None,      None,      "#00E436", "#00E436", "#00E436", "#00E436",],
        [None,      None,      "#00E436", "#00E436", "#1D2B53", "#00E436", "#008751",],
        [None,      None,      "#008751", "#00E436", "#1D2B53", "#1D2B53", "#00E436",],
        [None,      None,      "#008751", "#008751", "#00E436", "#FF004D", "#00E436",],
        [None,      "#1D2B53", None,      "#008751", "#008751", "#00E436", "#00E436",],
        [None,      "#008751", "#00E436", None,      "#008751", "#1D2B53", "#1D2B53",],
        ["#008751", "#00E436", "#00E436", "#00E436", None,      "#1D2B53", "#008751",],
        ["#00E436", "#00E436", "#00E436", None,      None,      None,      None,     ],
        ["#008751", "#00E436", "#00E436", "#00E436", "#008751", None,      None,     ],
        ["#1D2B53", "#008751", "#00E436", "#008751", None,      None,      None,     ],
    ],
    [
        [None,      None,      "#C2C3C7", "#1D2B53", None,      None,      None,     ],
        [None,      None,      "#83769C", "#C2C3C7", "#1D2B53", None,      None,     ],
        [None,      None,      None,      "#83769C", "#C2C3C7", "#83769C", "#C2C3C7",],
        ["#83769C", "#1D2B53", None,      None,      "#83769C", "#C2C3C7", "#C2C3C7",],
        ["#83769C", "#83769C", "#83769C", "#1D2B53", "#C2C3C7", "#83769C", "#C2C3C7",],
        ["#1D2B53", "#C2C3C7", "#83769C", "#83769C", "#83769C", "#7E2553", "#1D2B53",],
        ["#C2C3C7", "#C2C3C7", "#1D2B53", None,      "#C2C3C7", "#7E2553", "#7E2553",],
        ["#C2C3C7", "#C2C3C7", None,      None,      "#83769C", "#C2C3C7", "#C2C3C7",],
        ["#C2C3C7", "#C2C3C7", "#C2C3C7", "#83769C", "#1D2B53", None,      None,     ],
        ["#83769C", "#C2C3C7", "#C2C3C7", "#83769C", None,      None,      None,     ],
        ["#1D2B53", "#C2C3C7", "#83769C", "#1D2B53", None,      None,      None,     ],
        [None,      "#C2C3C7", "#83769C", "#83769C", None,      None,      None,     ],
        [None,      "#1D2B53", "#83769C", "#1D2B53", None,      None,      None,     ],
    ],
    [
        [None,      None,      None,      None,      "#7E2553", "#FFA300", "#FFA300",],
        [None,      None,      "#7E2553", "#FFA300", "#FFA300", "#FFA300", "#FFEC27",],
        [None,      "#7E2553", "#FFA300", "#FFA300", "#FFEC27", "#FFEC27", "#FFEC27",],
        [None,      "#FFA300", "#FFA300", "#FFEC27", "#FFA300", "#FFEC27", "#FFEC27",],
        ["#7E2553", "#FFA300", "#FFEC27", "#FFEC27", "#FFEC27", "#FFA300", "#FFA300",],
        ["#FFA300", "#FFA300", "#FFEC27", "#FFEC27", "#FFEC27", "#FFEC27", "#FFEC27",],
        ["#AB5236", "#AB5236", "#000000", "#000000", "#FFA300", "#FFEC27", "#FFEC27",],
        ["#AB5236", "#AB5236", "#1D2B53", "#FF004D", "#000000", "#FFA300", "#FFEC27",],
        ["#AB5236", "#FFA300", "#AB5236", "#1D2B53", "#1D2B53", "#AB5236", "#AB5236",],
        ["#7E2553", "#AB5236", "#FFA300", "#AB5236", "#AB5236", "#FFA300", "#FFA300",],
        ["#7E2553", "#7E2553", "#AB5236", "#AB5236", "#AB5236", "#AB5236", "#AB5236",],
        [None,      "#7E2553", "#7E2553", "#7E2553", None,      None,      None,     ],
    ]
    ]

    ROCK1 = [
        [None,      None,      "#FFA300", "#FFA300", "#FFA300", "#FFA300", "#5F574F", "#1D2B53", None,      None,      None,      None,     ],
        [None,      "#FFA300", "#FFA300", "#5F574F", "#5F574F", "#5F574F", "#5F574F", "#5F574F", "#1D2B53", None,      None,      None,     ],
        ["#FFA300", "#FFA300", "#5F574F", "#5F574F", "#5F574F", "#5F574F", "#5F574F", "#5F574F", "#5F574F", "#1D2B53", None,      None,     ],
        ["#FFA300", "#5F574F", "#1D2B53", "#5F574F", "#5F574F", "#5F574F", "#1D2B53", "#1D2B53", "#5F574F", "#5F574F", "#1D2B53", None,     ],
        ["#5F574F", "#5F574F", "#5F574F", "#FFA300", "#5F574F", "#1D2B53", "#5F574F", "#5F574F", "#FFA300", "#5F574F", "#5F574F", None,     ],
        ["#5F574F", "#5F574F", "#5F574F", "#5F574F", "#5F574F", "#1D2B53", "#5F574F", "#5F574F", "#FFA300", "#5F574F", "#5F574F", "#1D2B53",],
        [None,      "#5F574F", "#5F574F", "#5F574F", "#5F574F", "#5F574F", "#FFA300", "#FFA300", "#5F574F", "#5F574F", "#5F574F", "#1D2B53",],
        [None,      "#1D2B53", "#5F574F", "#5F574F", "#5F574F", "#5F574F", "#5F574F", "#5F574F", "#5F574F", "#5F574F", "#1D2B53", "#1D2B53",],
        [None,      "#1D2B53", "#1D2B53", "#1D2B53", "#5F574F", "#5F574F", "#5F574F", "#5F574F", "#1D2B53", "#1D2B53", "#1D2B53", "#1D2B53",],
        [None,      None,      "#1D2B53", "#1D2B53", "#1D2B53", "#1D2B53", "#1D2B53", "#1D2B53", "#1D2B53", "#1D2B53", "#1D2B53", "#1D2B53",],
        [None,      None,      None,      "#1D2B53", "#1D2B53", "#1D2B53", "#1D2B53", "#1D2B53", "#1D2B53", "#1D2B53", "#1D2B53", None,     ],
        [None,      None,      None,      None,      None,      None,      "#1D2B53", "#1D2B53", "#1D2B53", "#1D2B53", None,      None,     ],
    ]

    ROCK2 = [
    [None,      None,      None,      None,      "#FFA300", "#FFA300", "#5F574F", "#FFA300", "#5F574F", None,      None,      None,     ],
    [None,      None,      None,      "#FFA300", "#FFA300", "#5F574F", "#5F574F", "#1D2B53", "#5F574F", "#1D2B53", "#1D2B53", None,     ],
    [None,      None,      "#FFA300", "#FFA300", "#5F574F", "#5F574F", "#1D2B53", "#5F574F", "#5F574F", "#5F574F", "#1D2B53", "#1D2B53",],
    [None,      "#FFA300", "#FFA300", "#5F574F", "#5F574F", "#5F574F", "#5F574F", "#5F574F", "#FFA300", "#5F574F", "#5F574F", "#1D2B53",],
    [None,      "#FFA300", "#5F574F", "#1D2B53", "#1D2B53", "#5F574F", "#5F574F", "#5F574F", "#5F574F", "#5F574F", "#5F574F", "#1D2B53",],
    [None,      "#5F574F", "#1D2B53", "#5F574F", "#5F574F", "#5F574F", "#5F574F", "#5F574F", "#5F574F", "#5F574F", "#1D2B53", "#1D2B53",],
    [None,      None,      "#1D2B53", "#5F574F", "#5F574F", "#FFA300", "#5F574F", "#5F574F", "#1D2B53", "#1D2B53", "#1D2B53", None,     ],
    [None,      None,      None,      "#1D2B53", "#1D2B53", "#1D2B53", "#1D2B53", "#1D2B53", "#1D2B53", None,      None,      None,     ],
    ]

    ROCK3 = [
        [None,      None,      None,      None,      None,      None,      None,      None,      None,      "#FFA300", "#FFA300", "#5F574F", "#5F574F", "#5F574F", None,      None,     ],
        [None,      None,      None,      None,      "#FFA300", "#FFA300", "#FFA300", "#FFA300", "#FFA300", "#5F574F", "#5F574F", "#5F574F", "#5F574F", "#5F574F", "#1D2B53", None,     ],
        [None,      "#FFA300", "#FFA300", "#FFA300", "#5F574F", "#5F574F", "#5F574F", "#5F574F", "#5F574F", "#5F574F", "#5F574F", "#5F574F", "#1D2B53", "#5F574F", "#1D2B53", "#1D2B53",],
        ["#FFA300", "#FFA300", "#5F574F", "#5F574F", "#5F574F", "#5F574F", "#5F574F", "#5F574F", "#5F574F", "#5F574F", "#5F574F", "#1D2B53", "#5F574F", "#FFA300", "#1D2B53", "#1D2B53",],
        ["#FFA300", "#5F574F", "#5F574F", "#1D2B53", "#1D2B53", "#5F574F", "#5F574F", "#1D2B53", "#1D2B53", "#1D2B53", "#5F574F", "#5F574F", "#1D2B53", "#1D2B53", "#1D2B53", "#1D2B53",],
        ["#5F574F", "#5F574F", "#1D2B53", "#5F574F", "#5F574F", "#FFA300", "#1D2B53", "#1D2B53", "#1D2B53", "#1D2B53", "#1D2B53", "#1D2B53", "#1D2B53", "#1D2B53", "#1D2B53", None,     ],
        ["#1D2B53", "#5F574F", "#5F574F", "#1D2B53", "#1D2B53", "#1D2B53", "#1D2B53", None,      None,      None,      None,      None,      None,      None,      None,      None,     ],
        [None,      "#1D2B53", "#1D2B53", "#1D2B53", "#1D2B53", None,      None,      None,      None,      None,      None,      None,      None,      None,      None,      None,     ],
    ]

    ROCK4 = [
        [None,      None,      "#5F574F", "#FFA300", "#FFA300", "#5F574F", None,     ],
        [None,      "#5F574F", "#FFA300", "#1D2B53", "#5F574F", "#5F574F", "#1D2B53",],
        [None,      "#FFA300", "#1D2B53", "#5F574F", "#5F574F", "#1D2B53", "#1D2B53",],
        ["#FFA300", "#5F574F", "#5F574F", "#5F574F", "#5F574F", "#1D2B53", "#1D2B53",],
        ["#FFA300", "#5F574F", "#5F574F", "#5F574F", "#1D2B53", "#1D2B53", None,     ],
        ["#5F574F", "#5F574F", "#1D2B53", "#1D2B53", "#1D2B53", None,      None,     ],
        [None,      "#1D2B53", "#1D2B53", "#1D2B53", None,      None,      None,     ],
    ]

    ROCK5 = [
        [None,      "#FFA300", "#5F574F", "#5F574F", "#1D2B53", None,     ],
        ["#FFA300", "#1D2B53", "#5F574F", "#5F574F", "#5F574F", "#1D2B53",],
        ["#5F574F", "#5F574F", "#5F574F", "#5F574F", "#5F574F", "#1D2B53",],
        ["#1D2B53", "#5F574F", "#5F574F", "#5F574F", "#1D2B53", None,     ],
        [None,      "#1D2B53", "#1D2B53", "#1D2B53", None,      None,     ],
    ]

    SHIP = [
        [None,      None,      None,      None,      None,      None,      None,      None,     ],
        [None,      None,      None,      "#83769C", "#83769C", None,      None,      None,     ],
        [None,      "#83769C", "#1D2B53", "#FFF1E8", "#29ADFF", "#1D2B53", "#5F574F", None,     ],
        ["#83769C", "#83769C", "#7E2553", "#FFF1E8", "#29ADFF", "#1D2B53", "#5F574F", "#5F574F",],
        ["#83769C", "#C2C3C7", "#83769C", "#29ADFF", "#29ADFF", "#1D2B53", "#83769C", "#5F574F",],
        ["#83769C", "#C2C3C7", "#83769C", "#5F574F", "#1D2B53", "#1D2B53", "#83769C", "#5F574F",],
        ["#1D2B53", "#83769C", "#5F574F", "#83769C", "#83769C", "#5F574F", "#5F574F", "#1D2B53",],
        [None,      "#1D2B53", "#1D2B53", None,      None,      "#1D2B53", "#1D2B53", None,     ],
    ]

    UFO = [
        [None,      None,      None,      None,      None,      "#1D2B53", "#29ADFF", "#FFF1E8",],
        [None,      None,      None,      None,      "#1D2B53", "#29ADFF", "#FFF1E8", "#FFF1E8",],
        [None,      None,      None,      "#1D2B53", "#29ADFF", "#29ADFF", "#29ADFF", "#29ADFF",],
        [None,      "#83769C", "#83769C", "#C2C3C7", "#FFF1E8", "#FFF1E8", "#C2C3C7", "#C2C3C7",],
        ["#83769C", "#83769C", "#C2C3C7", "#FFF1E8", "#FFF1E8", "#C2C3C7", "#C2C3C7", "#C2C3C7",],
        [None,      "#7E2553", "#FF004D", "#7E2553", None,      None,      "#7E2553", "#FF004D",],
    ]

    LAZER = [
        ["#8F8F8F"],
        ["#F8F8F8"],
        ["#F8F8F8"],
        ["#F8F8F8"],
        ["#F8F8F8"],
        ["#8F8F8F"]
    ]

    SMALLENEMY =[
        [
            [None,      "#00E436", "#008751", None,     ],
            ["#00E436", "#008751", None,      None,     ],
            ["#008751", "#008751", "#00E436", "#00E436",],
            [None,      "#00E436", "#1D2B53", "#00E436",],
            [None,      "#00E436", "#FF004D", "#00E436",],
            ["#008751", "#00E436", "#008751", "#008751",],
            ["#00E436", "#1D2B53", None,      None,     ],
            ["#008751", "#00E436", "#00E436", None,     ],
        ],
        [
            [None,      "#7E2553", "#FFA300",],
            ["#7E2553", "#FFA300", "#FFEC27",],
            ["#AB5236", "#FFA300", "#FFA300",],
            ["#AB5236", "#1D2B53", "#AB5236",],
            ["#7E2553", "#AB5236", "#FFA300",],
            [None,      None,      None,     ],
            ["#FFA300", "#AB5236", None,     ],
            ["#AB5236", "#7E2553", None,     ],
        ],
        [
            ["#FF004D", None,      "#7E2553", "#FF004D",],
            ["#7E2553", "#7E2553", "#FF004D", "#FF77A8",],
            [None,      "#FF004D", "#FF004D", "#FF004D",],
            [None,      "#7E2553", None,      "#7E2553",],
            ["#7E2553", "#FF004D", "#1D2B53", "#7E2553",],
            ["#FF004D", "#FF004D", None,      "#FF004D",],
            ["#FF004D", "#7E2553", None,      None,     ],
            ["#7E2553", "#FF004D", "#7E2553", None,     ],
        ],
        [
            [None,      "#1D2B53", "#008751",],
            [None,      "#008751", "#00E436",],
            ["#1D2B53", "#008751", "#00E436",],
            ["#1D2B53", "#7E2553", "#008751",],
            [None,      "#1D2B53", "#008751",],
            ["#008751", "#1D2B53", None,     ],
            ["#008751", None,      None,     ],
            ["#1D2B53", "#008751", None,     ],
        ],
        [
            [None,      None,      "#FFA300", "#FFEC27",],
            [None,      "#FFA300", "#FFEC27", "#FFEC27",],
            ["#AB5236", "#FFA300", "#1D2B53", "#FFA300",],
            ["#FFA300", "#FFEC27", "#FFA300", "#FFEC27",],
            ["#FFEC27", "#FFA300", None,      "#FFEC27",],
            ["#FFA300", None,      None,      None,     ],
            ["#AB5236", "#FFA300", None,      "#AB5236",],
            [None,      "#AB5236", None,      None,     ],
        ],
        [
            [None,      None,      "#7E2553", "#FF77A8",],
            [None,      "#7E2553", "#FF77A8", "#FFCCAA",],
            [None,      "#FF77A8", "#FFCCAA", "#FFCCAA",],
            [None,      "#FFCCAA", "#1D2B53", "#FF77A8",],
            [None,      "#7E2553", "#FF77A8", "#FFCCAA",],
            [None,      "#FF77A8", "#1D2B53", "#FFCCAA",],
            [None,      "#FF77A8", "#1D2B53", "#FF77A8",],
            [None,      "#7E2553", "#FF77A8", "#7E2553",],
        ],
        [
            ["#1D2B53", "#83769C", "#1D2B53", None,     ],
            [None,      "#1D2B53", "#C2C3C7", None,     ],
            ["#83769C", "#1D2B53", "#83769C", "#C2C3C7",],
            ["#C2C3C7", "#83769C", "#C2C3C7", "#C2C3C7",],
            ["#C2C3C7", "#1D2B53", "#7E2553", "#83769C",],
            ["#C2C3C7", "#1D2B53", "#C2C3C7", "#C2C3C7",],
            ["#1D2B53", "#83769C", "#1D2B53", None,     ],
            [None,      "#1D2B53", "#83769C", None,     ],
        ],
        [
            ["#1D2B53", None,      None,     ],
            ["#29ADFF", None,      None,     ],
            ["#29ADFF", "#1D2B53", None,     ],
            ["#1D2B53", "#29ADFF", "#1D2B53",],
            ["#29ADFF", None,      "#29ADFF",],
            ["#29ADFF", "#29ADFF", None,     ],
            ["#29ADFF", "#29ADFF", "#1D2B53",],
            ["#29ADFF", "#1D2B53", None,     ],
        ]
    ]

    EXPLOSION =[
            [
                ["#FFEC27", "#FFEC27"],
                ["#FFF1E8", "#FFEC27"],
                ["#7E2553", "#7E2553"]
            ],
            [
                ["#7E2553", "#FFEC27"],
                ["#FFEC27", "#FFF1E8"],
            ],
            [
                [ None,      "#7E2553", "#FFEC27", "#FFEC27"],
                [ "#7E2553", "#FFEC27", "#FFEC27", "#FFF1E8"],
                [ "#FFEC27", "#FFEC27", "#FFF1E8", "#FFF1E8"],
                [ "#FFEC27", "#FFF1E8", "#FFF1E8", "#FFF1E8"],
                ]
            ]

    @staticmethod
    def hmirror_texture(texture):
        """Horizontally mirror a texture

        :param texture: texture to mirror
        """
        return [(row + row[::-1]) for row in texture]

    @staticmethod
    def vmirror_texture(texture):
        """Vertically mirror a texture

        :param texture: texture to mirror
        """
        return texture + texture[::-1]

    @staticmethod
    def recolor(texture, color):
        """recolor a texture

        :param texture: texture to recolor
        :param color: Color to multiply the texture with
        """
        return [[None if col is None else Textures.multiply_colors(col, color) for col in row] for row in texture]

    @staticmethod
    def multiply_colors(hex1, hex2):
        """Multiply two RGB colours

        :param hex1: first colour
        :param hex2: second colour
        """
        color1 = Textures.hex_to_rgb(hex1)
        color2 = Textures.hex_to_rgb(hex2)
        return Textures.rgb_to_hex([color1[i] * color2[i] for i in range(len(color1))])

    @staticmethod
    def hex_to_rgb(value):
        """Convert a hexadecimal colour value to red green and blue

        :param value: hex value
        """
        value = value.lstrip('#')
        length = len(value)
        return tuple(int(value[i:i + length // 3], 16)/256 for i in range(0, length, length // 3))

    @staticmethod
    def rgb_to_hex(value):
        """Convert red green and blue value to a hexadecimal representation

        :param value: RGB value
        """
        return "#" + "".join(f"{int(v*256):02X}" for v in value)

    @staticmethod
    def white_texture(texture):
        """Replace all coloured pixels with white

        :param texture: Texture to replace on
        """
        return [[None if col is None else "#FFFFFF" for col in row] for row in texture]

    @staticmethod
    def load_textures(texture_factory):
        """Load all textures within this class

        :param texture_factory:
        """
        texture_factory.load_texture(
            "ufo", Textures.hmirror_texture(Textures.UFO))
        texture_factory.load_texture("star", Textures.STAR)

        texture_factory.load_texture("ship", Textures.SHIP)
        texture_factory.load_texture(
            "ship:white", Textures.white_texture(Textures.SHIP))

        texture_factory.load_texture("rock1", Textures.ROCK1)
        texture_factory.load_texture("rock2", Textures.ROCK2)
        texture_factory.load_texture("rock3", Textures.ROCK3)
        texture_factory.load_texture("rock4", Textures.ROCK4)
        texture_factory.load_texture("rock5", Textures.ROCK5)

        texture_factory.load_texture(
            "lazer:white", Textures.recolor(Textures.LAZER, "#ffffff"))
        texture_factory.load_texture(
            "lazer:red", Textures.recolor(Textures.LAZER, "#f2aaaa"))
        texture_factory.load_texture(
            "lazer:yellow", Textures.recolor(Textures.LAZER, "#f2ffaa"))

        for i, enemy in enumerate(Textures.SMALLENEMY):
            name = f"smallenemy{i}"
            texture = Textures.hmirror_texture(enemy)
            texture_factory.load_texture(name, texture)
            texture_factory.load_texture(
                f"{name}:white", Textures.white_texture(texture))
            evil_texture = Textures.recolor(texture, "#FF5555")
            texture_factory.load_texture(f"{name}_evil", evil_texture)
            texture_factory.load_texture(
                f"{name}_evil:white", Textures.white_texture(evil_texture))

        for i, enemy in enumerate(Textures.ENEMY):
            name = f"enemy{i}"
            texture_factory.load_texture(name, Textures.hmirror_texture(enemy))
            texture_factory.load_texture(
                f"{name}:white", Textures.white_texture(Textures.hmirror_texture(enemy)))

        texture_factory.load_texture("explosion3", Textures.EXPLOSION[0])
        texture_factory.load_texture("explosion2", Textures.hmirror_texture(
            Textures.vmirror_texture(Textures.EXPLOSION[1])))
        texture_factory.load_texture("explosion1", Textures.hmirror_texture(
            Textures.vmirror_texture(Textures.EXPLOSION[2])))


class TextureFactory:
    """Object that deals with loading and scaling textures"""

    def __init__(self, scale) -> None:
        """Initialise the texture factory

        :param scale: the amount of pixels to upscale by
        :rtype: None
        """
        self.textures = {}
        self.scale = scale

    def load_texture(self, namespace, texture_matrix):
        """Load and upscale a texture

        :param namespace: namespace to save this texture to
        :param texture_matrix: A matrix of hex colours that represents the texture
        """
        if namespace not in self.textures:
            height = len(texture_matrix) * self.scale
            width = len(texture_matrix[0]) * self.scale
            photo_image = PhotoImage(width=width, height=height)

            for matrix_y, row in enumerate(texture_matrix):
                for matrix_x, color in enumerate(row):
                    if color is not None:
                        pixel_string = (
                            "{" + f"{color} "*self.scale + "} ") * self.scale
                        photo_image.put(
                            pixel_string, (matrix_x*self.scale, matrix_y*self.scale))

            self.textures[namespace] = photo_image
            return photo_image
        return self.get_image(namespace)

    def get_image(self, namespace):
        """Get a loaded image

        :param namespace: to load the image from
        """
        if namespace not in self.textures:
            raise Exception(
                f"Provided namespace \"{namespace}\" has not been loaded!")
        return self.textures[namespace]
