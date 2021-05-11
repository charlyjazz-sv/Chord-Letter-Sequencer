from chord_constructor_random import ChordConstructorRandom
from image_creator import ImageCreator
from chord import Chord

# https://www.pianochord.org/chord-symbols.html

# Qualities
# Cases: Triangle Symbol, M letter, Maj word
# CMajor = Chord("C", "", "major")
# CMinor = Chord("C", "", "minor")
# CHalfDimismished = Chord("C", "", "half disminished")
# CDisminished = Chord("C", "", "disminished")
# CAugmented = Chord("C", "", "augmented")

# Accidental with Quality, Sharp # and Flat b
CSharpMajor = Chord("C", "#", "major")
CFlatMajor = Chord("C", "b", "major")

if __name__ == '__main__':
    image_creator = ImageCreator(CSharpMajor)
    image_creator.create_image()
