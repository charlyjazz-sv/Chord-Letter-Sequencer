from PIL import Image, ImageDraw, ImageFont
from chord import Chord

import cv2
import os

from numpy.random import choice
from numpy import array

# Major	C Cmaj CM	C, E, G
# Minor	Cm Cmin C-	C, Eb, G
# Diminished	Cdim Co	C, Eb, Gb
# Augmented	Caug C+ C+5	C, E, G#

PATH = os.path.dirname(os.path.abspath(__file__))


def get_font_path(name):
    return os.path.join(PATH, 'fonts', name + '.ttf')


def get_symbol_path(name):
    return os.path.join(PATH, 'symbols', name + '.png')


class ImageCreator():
    def __init__(self, chord_instance: Chord):
        self.chord = chord_instance
        self.fonts_path = [
            get_font_path('arial'),
            get_font_path('Cooljazz')
        ]
        # Each key is the label value of the symbol and
        # we going to use severals symbol versions for the
        # same label value
        self.symbols = {
            # Qualities
            "major": [
                "",
                "ma",
                "M",
                "Maj",
                get_symbol_path('major_triangle1'),
                get_symbol_path('major_triangle2')
            ],
            "minor": ["-", "m", "min", "mi"],
            "half disminished": [
                get_symbol_path('half_disminished1'),
                get_symbol_path('half_disminished2'),
                get_symbol_path('half_disminished3'),
                get_symbol_path('half_disminished4'),
                get_symbol_path('half_disminished5'),
                get_symbol_path('half_disminished6'),
                get_symbol_path('half_disminished7'),
                "0"
            ],
            "disminished": ["o", "O", "0", get_symbol_path('disminished'), ],
            "augmented": ["AUG", "aug", "+"],
            # Accidental
            "#": [
                "#",
                get_symbol_path('sharp1'),
                get_symbol_path('sharp2'),
                get_symbol_path('sharp3'),
                get_symbol_path('sharp4'),
            ],
            "b": [
                "b",
                get_symbol_path('flat1'),
                get_symbol_path('flat2'),
                get_symbol_path('flat3'),
                get_symbol_path('flat4'),
                get_symbol_path('flat5'),
                get_symbol_path('flat6')
            ],
        }
        self.font_sizes = [35]

        # Creating Image State

        self.chord_string_length = None
        self.font_size = None
        self.font_family = None
        self.truetype = None
        self.image = None
        self.draw = None
        self.x_offset = 0.0

    # This method need measure the real chord length because
    # word like disminished will be replace with a symbol then len(str)
    # is wrong because if the image wil be a symbol with the length
    # of a single character
    def len_chord(self, string):
        return len(string)

    # Create image of the chord to save
    def create_image(self):
        self.chord_string_length = self.len_chord(str(self.chord))
        self.font_size = choice(self.font_sizes)
        self.font_family = choice(self.fonts_path)
        self.truetype = ImageFont.truetype(self.font_family, self.font_size)
        self.image = Image.new('RGB', (int(
            (self.font_size / 1.5) * self.chord_string_length), 100), color=(255, 255, 255))
        self.draw = ImageDraw.Draw(self.image)

        # Array of functions to split concerns and condionality
        pipeline = self.pipeline_of_texts()

        for fn in pipeline:
            fn()

        # Show image
        self.open_cv_show_image()

    # Useful pipeline of functions to send offset x in each function and
    # Separate concerns and and complex logic in each function
    def pipeline_of_texts(self):
        return [
            self.draw_pitch,
            self.draw_accidentals,
            self.draw_quality
        ]

    # Draw Pitch in the image
    def draw_pitch(self):
        new_x_offset = self.font_size / 1.5
        self.draw.text((self.x_offset,  self.font_size / 2),
                       self.chord.pitch, font=self.truetype, fill=(0, 0, 0))
        self.x_offset = new_x_offset

    # Draw Accidentals with letters or symbols (random choice)
    # Accidentals are flat `b` and sharp `#`
    def draw_accidentals(self):
        new_x_offset = self.x_offset
        if self.chord.is_valid_accidental(self.chord.accidentals):
            synonymous = choice(self.symbols[self.chord.accidentals])
            fontsizes = [15, 18, 20, 22, 25, 27]
            fontsize = int(choice(fontsizes))
            if ".png" in synonymous:
                image_symbol = Image.open(synonymous)
                image_symbol.thumbnail((fontsize, fontsize))
                image_symbol = image_symbol.convert("RGB").copy()
                self.image.paste(
                    image_symbol, (int(self.x_offset),  int(self.font_size / 2)))
                self.x_offset = self.x_offset + fontsize
            elif len(synonymous):
                font = ImageFont.truetype(self.font_family, fontsize)
                y = fontsize
                self.draw.text((self.x_offset,  y), synonymous,
                               font=font, fill=(0, 0, 0))
                self.x_offset = self.x_offset + (fontsize * len(synonymous))
        return new_x_offset

    # Draw Quality with letters or symbols (random choice)
    # Quality word are minor, major, augmented, disminished and half disminished
    def draw_quality(self):
        # Chose a symbol or word to replace the quality word
        synonymous = choice(self.symbols[self.chord.quality])
        fontsizes = [15, 18, 20, 22, 25, 27]
        fontsize = int(choice(fontsizes))
        if ".png" in synonymous:
            image_symbol = Image.open(synonymous)
            image_symbol.thumbnail((fontsize, fontsize))
            image_symbol = image_symbol.convert("RGB").copy()
            self.image.paste(
                image_symbol, (int(self.x_offset),  int(self.font_size / 2)))
            self.x_offset = self.x_offset + fontsize
        elif len(synonymous):
            font = ImageFont.truetype(self.font_family, fontsize)
            y = fontsize
            self.draw.text((self.x_offset,  y), synonymous,
                           font=font, fill=(0, 0, 0))
            self.x_offset = self.x_offset + (fontsize * len(synonymous))
        else:
            pass

    def open_cv_show_image(self):
        cv_img = array(self.image)
        cv_img = cv_img[:, :, ::-1].copy()
        cv2.imshow(str(self.chord), cv_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
