import random
import argparse
import numpy as np
from main import non_or_str
from PIL import Image, ImageDraw, ImageFont

notes = np.array(["C", "D", "E", "F", "G", "A", "B"])
alterations_dictionary = {
    "Δ":"major",
    "M": "major",
    "-" : "minor",
    "m": "minor",
    "+": "augmented",
    "o": "diminished",
    "ø": "half diminished",
    "#": "sharp",
    "b": "bimol",
    "min": "minor",
    "Maj":"major",
    "maj":"major",
    "dim":"diminished",
    "None": None,
    # "<"   : "mychord",
    # "9\\6" : "6add9"
    # "♯": "sharp"
}
symbols = np.array(list(alterations_dictionary.keys()))
extra_notes = np.array([
    "4",
    "6",
    "9",
    "11",
    "13",
    "b4",
    "b6",
    "b9",
    "b11",
    "b13",
    None
])
suspended_chords = [
    "sus4",
    "sus2"
]
dict_alterations = {
    "+": 'augmented',
    "-": "diminished",
    "": "add"
}
keys_dict_alterations = np.array(list(dict_alterations.keys()))
chords_list = []

def gen_data(path, count):
    maxlen = 0
    for i in range(count):
        root = np.random.choice(notes)
        symbol = np.random.choice(symbols)
        extra = np.random.choice(extra_notes, size=np.random.randint(1, 3))
        extra_value_to_img = ""
        extra_label = "" 
        symbol_label = "major"
        
        if np.random.randint(0, 2) == 1:
            extra_label = "7"
            extra_value_to_img = "7"
            
        if np.random.randint(0, 5) == 1:
            sus = np.random.choice(suspended_chords)
            extra_label = sus
            extra_value_to_img = sus

        if symbol == "None":
            symbol = ""
        else:
            symbol_label = alterations_dictionary[symbol]
        
        if np.random.randint(0, 2) == 1:
            if len(extra) == 1 and extra[0] != None:
                alteration_choiced = np.random.choice(keys_dict_alterations)
                extra_label = extra_label + " {}{}".format(dict_alterations[alteration_choiced], extra[0])
                extra_value_to_img = extra_value_to_img + " {}{}".format(alteration_choiced, extra[0])
            else:
                for interval in extra:

                    if interval == None:
                        pass
                    else: 
                        add_string = "add" if np.random.randint(0, 2) == 1 else ""
                        extra_label = extra_label + " {} {}".format(add_string, interval)
                        extra_value_to_img = extra_value_to_img + " {} {}".format(add_string, interval)

          
        x = "{0}{1} {2}".format(root,symbol,extra_value_to_img)
        y = "{0} {1} {2}".format(root, symbol_label, extra_label)
        chords_list.append([x, y])
        if len(x) > maxlen:
            maxlen = len(x)

    font_families = ["arial.ttf"]

    for (chord, label) in chords_list:
        img = Image.new('RGB', (200, 50), color=(255, 255, 255))
        fnt = ImageFont.truetype(r'{}'.format(np.random.choice(font_families)), 18)
        d = ImageDraw.Draw(img)
        d.text((5, 15), chord, font=fnt, fill=(0, 0, 0))
        lab = chord + " "*(maxlen-len(chord))
        img.save(path+"/{}.png".format(lab))

    with open(path+"/max.txt", 'w') as f:
        f.write(f"{maxlen}\n")


if __name__=='__main__':
    parser = argparse.ArgumentParser(description='OCR using CNN+RNN+CTC')
    parser.add_argument('--path', type=non_or_str, help='path to the directory')
    parser.add_argument('--count', type=int, help="No. of images to create")
    args = parser.parse_args() 

    gen_data(args.path, args.count)

















