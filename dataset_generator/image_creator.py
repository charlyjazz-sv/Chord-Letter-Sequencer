from PIL import Image, ImageDraw, ImageFont

import cv2
import numpy as np


class ImageCreator():
    def __init__(self, chord_instance: Chord):
        self.chord = chord_instance
        self.fonts_path = [
            
        ]
        # Each key is the label value of the symbol and
        # we going to use severals symbol versions for the
        # same label value
        self.symbols_path = {
            "major": [],
            "sharp": [],
            "bimol": []
        }
        self.font_sizes = [35, 38, 40, 43, 45, 48, 50, 55, 60]

    # This method need measure the real chord length because
    # word like disminished will be replace with a symbol then len(str)
    # is wrong because if the image wil be a symbol with the length
    # of a single character
    def len_chord(self, string):
        return len(string)

    # Create iamge of the chord to save
    def create_image(self):
        chord_string_length = self.len_chord(str(self.chord))
        font_size = np.random.choice(self.font_sizes)
        font_family = np.random.choice(self.fonts_path)
        truetype = ImageFont.truetype(font_family, font_size)
        image = Image.new('RGB', (int((font_size / 1.5) *
                          chord_string_length), 100), color=(255, 255, 255))
        draw = ImageDraw.Draw(image)

        # Array of functions to split concerns and condionality
        pipeline = self.pipeline_of_texts()

        x_offset = 0.0
        for fn in pipeline:
            x_offset = fn(draw, font_size, truetype, x_offset)

        # Show image
        self.open_cv_show_image(image)

    # Useful pipeline of functions to send offset x in each function and
    # Separate concerns and and complex logic in each function
    def pipeline_of_texts(self):
        return [
            self.draw_pitch,
            self.draw_bass_slash_note,
            self.draw_accidentals
        ]

    # Draw Pitch in the image
    def draw_pitch(self, draw, font_size, truetype, x_offset: float):
        new_x_offset = font_size / 1.5
        draw.text((x_offset,  font_size / 2), self.chord.pitch,
                  font=truetype, fill=(0, 0, 0))
        return new_x_offset

    # Add Slash note if exist
    def draw_bass_slash_note(self, draw, font_size, truetype, x_offset: float):
        new_x_offset = x_offset
        if self.chord.bass_slash_note:
            string_to_draw = "/" + self.chord.bass_slash_note
            new_x_offset = x_offset + ((x_offset) * len(string_to_draw))
            draw.text((x_offset,  font_size / 2), string_to_draw,
                      font=truetype, fill=(0, 0, 0))
        return new_x_offset

    # Draw Accidentals with letters or symbols (random choice)
    def draw_accidentals(self,  draw, font_size, truetype, x_offset: float):
        new_x_offset = x_offset
        if self.chord.is_valid_accidental(self.chord.accidentals):
            new_x_offset = x_offset + x_offset
            # TODO: Use symbols
            draw.text((x_offset,  font_size / 2), self.chord.accidentals,
                      font=truetype, fill=(0, 0, 0))
        return new_x_offset

    def open_cv_show_image(self, image):
        cv_img = np.array(image)
        cv_img = cv_img[:, :, ::-1].copy()
        cv2.imshow(str(self.chord), cv_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()