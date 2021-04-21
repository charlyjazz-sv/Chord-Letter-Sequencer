# Chord-Letter-Sequencer


## Dependencies

```
pip install numpy pillow matplotlib tensorflow
```


## Generate the Datasets

The dataset generates the images to size 50x200. If you decide to change the size in the script, make sure to change it in `dataset.py` as well.

```
mkdir chord_train
python gen_dataset.py --path chord_train --count 3200
mkdir chord_eval
# here make sure to have a big enough dataset so that all of the vocabulary has been included, otherwise if less, the model 
will not resume properly as the no. of output neurons depends on the vocabulary.
python gen_dataset.py --path chord_eval --count 3200
```


## Train the Model

The dataset is used to get the list of the available vocabulary hence defining the no. of output neurons.

```
mkdir checkpoint
python main.py --dataset ./chord_train
```


## Evaluate the Model

```
python main.py --dataset ./chord_eval --resume ./checkpoint/best.h5 <--eval/--eval_chords>
```

## Test a single Image

```
python main.py --dataset ./chord_train --resume ./checkpoint/best.h5 --eval_img <path to image>
```


## For RNN+CTC

RNN only model is simpler and trains slow but it gives more accuracy (for what I observed).

```
uncomment line 87 in dataset.py to shape the input properly for RNN
change the input layer, and pass it to lstm and neurons for lstm to 128, comment out the entire 'CNV' part
in trainer.py change the lines 114-117 to use the last dim as 0 
```

## Adding a Single Character Chord

1. Add a chord entry in the `gen_dataset.py`. e.g. I randomly tired `"<" = "mycord"` and generate the dataset.

2. Add the same corresponding entry in the `inverse_chord_map` in the `trainer.py`.

3. Train.


## Adding a Multiple Character Chord

1. Add a chord entry in the `gen_dataset.py`. e.g. I randomly tired `"9/6" = "9add6"` and generate the dataset.

2. Add the same corresponding entry in the if conditions in `decode_chord` in the `trainer.py`.

3. Train.


