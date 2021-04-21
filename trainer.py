import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

import tensorflow as tf
from tensorflow import keras

from model import CRNN
from dataset import DataSet



class OCRTrainer:
    def __init__(self, args):
        self.args = args

        self.dataset = DataSet(self.args.dataset, self.args.batch_size)
        self.model = CRNN(args.lr, self.dataset.img_width, self.dataset.img_height, self.dataset.total_labels)
        
        # restoring the model weights        
        if self.args.resume is not None:
            print(f"Resuming from checkpoint: {self.args.resume}")
            self.model.load_weights(self.args.resume)

        # inverse chord map for single character -> name used in decode chord
        self.inverse_chord_map = {
            "Δ":"major",
            "M": "major",
            "m": "minor",
            "+": "augmented",
            "-" : "diminished",
            "o": "diminished ",
            "ø": "half diminished",
            "#": "sharp",
            "b": "bimol",
            # "<"   : "mychord",
        }


    def decode_chord(self, pred_texts_batch):
        chord_batch = []
        for preds in pred_texts_batch:
            chord = ""
            i = 0
            # iterate over the chord prediction
            while(i < len(preds)):
                if preds[i:i+3] in ("Maj", "maj"):
                    chord += "major"
                    i += 3
                elif preds[i:i+3] == "min":
                    chord += "minor"
                    i += 3
                elif preds[i:i+3] == "dim":
                    chord += "diminished"
                    i += 3
                elif (preds[i] == "-") and (preds[i-1] in ("C", "D", "E", "F", "G", "A", "B")):
                    chord += "minor"
                    i += 1
                # elif preds[i:i+3] == "9\\6":
                #     chord += "6add9"
                #     i += 3
                elif preds[i:i+5] == "[UNK]": # ctc's unknown token
                    i += 5
                else:
                    # for single character try to get inverse chord mapping, if none, then return the same character
                    chord += self.inverse_chord_map.get(preds[i]) or preds[i]
                    i+=1
            # append the one completed chord
            chord_batch.append(chord)
        return chord_batch

    def train(self):
        # Train the model
        min_loss = 1000
        saved = ""
        for ep in range(self.args.epochs):
            loss = 0
            for idx, batch in enumerate(self.dataset.train_dataset):
                batch_images = batch["image"]
                batch_labels = batch["label"]
                loss += self.model.train_on_batch(batch_images, batch_labels)
            loss /= len(self.dataset.train_dataset)
            if loss < min_loss:
                self.model.save_weights("./checkpoint/best.h5")
                min_loss = loss
                saved = "Saving model at ./checkpoint/best.h5"
            print("Epoch {}/{}\tLoss = {:.5f}\t{}".format(ep+1, self.args.epochs, loss, saved))
            saved = ""
            # lr schdule
            if ep%self.args.interval == 0:
                self.model.optimizer.lr = self.model.optimizer.lr*0.1
        self.eval()

    def eval(self):
        #  Let's check results on some validation samples
        for batch in self.dataset.train_dataset.take(1):
            batch_images = batch["image"]
            batch_labels = batch["label"]
            # model prediction
            preds = self.model.predict(batch_images)
            # ctc decoding
            pred_texts = self.decode_batch_predictions(preds)
            # chord decoding
            pred_chord = self.decode_chord(pred_texts)
            # labels decoding
            orig_texts = []
            for label in batch_labels:
                label = tf.strings.reduce_join(self.dataset.num_to_char(label)).numpy().decode("utf-8")
                orig_texts.append(label)

            # plotting
            _, ax = plt.subplots(4, 4, figsize=(15, 5))
            for i in range(len(pred_chord)):
                # plotting from the RNN only model
                # img = (batch_images[i, :, :] * 255).numpy().astype(np.uint8)
                # plotting from the CNN + RNN model
                img = (batch_images[i, :, :, 0] * 255).numpy().astype(np.uint8)
                img = img.T
                title = f"{pred_chord[i]}"
                ax[i // 4, i % 4].imshow(img, cmap="gray")
                ax[i // 4, i % 4].set_title(title)
                ax[i // 4, i % 4].axis("off")
        plt.savefig('eval.png')
        plt.show()


    def eval_chords(self):
        correct = 0
        for idx, batch in enumerate(self.dataset.train_dataset):
            batch_images = batch["image"]
            batch_labels = batch["label"]
            preds = self.model.predict(batch_images)
            pred_texts = self.decode_batch_predictions(preds)
            pred_chord = self.decode_chord(pred_texts)
            orig_texts = []
            for label in batch_labels:
                label = tf.strings.reduce_join(self.dataset.num_to_char(label)).numpy().decode("utf-8")
                orig_texts.append(label)
            # comparing predicted OCR text with labels to compute accuracy
            for i,j in zip(orig_texts, pred_texts):
                correct += 1 if i == j else 0
        print("Accuracy: {:.2f}%".format((correct/self.dataset.len)*100))


    def eval_img(self, path):
        # passing the single image to the dataloader
        img = self.dataset.encode_single_sample(path, "None")["image"]
        # adding batch dim
        img = tf.expand_dims(img, 0)
        
        # the numpy and PIL image way
        # imgp = Image.open(path).convert('L')
        # imgp = imgp.resize(size=(self.dataset.img_width, self.dataset.img_height))
        # imgp = np.asarray(imgp)
        # imgp = imgp.T
        # imgp = np.expand_dims(imgp, 0)
        # imgp = np.expand_dims(imgp, -1)
        # imgn = imgp/imgp.max()

        preds = self.model.predict(img)
        pred_texts = self.decode_batch_predictions(preds)
        pred_chord = self.decode_chord(pred_texts)[0]
        print(f"Predicted OCR: {pred_texts[0]}, Predicted Chord: {pred_chord}")

        # plotting from the RNN only model
        # img = (img[0, :, :] * 255).numpy().astype(np.uint8)

        # plotting from the CNN + RNN model
        # img = (img[0, :, :, 0] * 255).numpy().astype(np.uint8)

        # for plotting
        # img = img.T
        # plt.imshow(img, cmap="gray")
        # plt.title(f"{pred_chord}")
        # plt.axis("off")
        # plt.show()


    # A utility function to decode the output of the network
    def decode_batch_predictions(self, pred):
        input_len = np.ones(pred.shape[0]) * pred.shape[1]
        # Use greedy search. For complex tasks, you can use beam search
        results = keras.backend.ctc_decode(pred, input_length=input_len, greedy=True)[0][0][
            :, :self.dataset.max_length
        ]
        # Iterate over the results and get back the text
        output_text = []
        for res in results:
            res = tf.strings.reduce_join(self.dataset.num_to_char(res)).numpy().decode("utf-8")
            output_text.append(res)
        return output_text





