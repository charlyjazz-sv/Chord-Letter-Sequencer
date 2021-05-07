from chord_constructor_random import ChordConstructorRandom
from image_creator import ImageCreator


if __name__ == '__main__':
    chord_constructor = ChordConstructorRandom()
    random_chord_created = chord_constructor.chord_creation_flow()
    print(random_chord_created)
    image_creator = ImageCreator(random_chord_created)
    image_creator.create_image()
