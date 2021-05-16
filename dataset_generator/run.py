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
# CSharpMajor = Chord("C", "#", "major")
# CFlatMajor = Chord("C", "b", "major")

# 5th flat and sharp
# C5Altered = Chord("C", "", "major", "b")
# C5Altered = Chord("C", "", "major", "#")
# C5Altered = Chord("C", "#", "major", "b")
# C5Altered = Chord("C", "#", "major", "#")
# C5Altered = Chord("C", "b", "major", "b")
# C5Altered = Chord("C", "b", "major", "#")

# Ordinary Number Type (6th, 7th, 9th, 11th, 13th)
# 7 Dominant No Supported Yet (Read chord.py comment about 7 dominant)!
# CDominant7 = Chord("C", "", "", None, "7th")
Cmaj7 = Chord("C", "", "major", None, "7th")
CSharpminor11 = Chord("C", "#", "major", "b", "11th")

if __name__ == '__main__':
    image_creator = ImageCreator(CSharpminor11)
    image_creator.create_image()
