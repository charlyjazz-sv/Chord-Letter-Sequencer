import numpy as np
import matplotlib.pyplot as plt

import tensorflow as tf
from tensorflow import keras

from model import CRNN
from dataset import DataSet



class OCRTrainer:
    def __init__(self, args):
        self.args = args

        self.dataset = DataSet(self.args.batch_size)
        self.model = CRNN(self.args, self.dataset.img_width, self.dataset.img_height, self.dataset.total_labels)
        
        if self.args.resume is not None:
            print(f"Resuming from checkpoint: {self.args.resume}")
            self.model.model.load_weights(self.args.resume)

    def train(self):
        # Train the model
        self.model.train(self.dataset)
        self.eval()

    def eval(self):
        #  Let's check results on some validation samples
        for batch in self.dataset.validation_dataset.take(1):
            batch_images = batch["image"]
            batch_labels = batch["label"]

            preds = self.model.predict(batch_images)
            pred_texts = self.decode_batch_predictions(preds)

            orig_texts = []
            for label in batch_labels:
                label = tf.strings.reduce_join(self.dataset.num_to_char(label)).numpy().decode("utf-8")
                orig_texts.append(label)

            _, ax = plt.subplots(4, 4, figsize=(15, 5))
            for i in range(len(pred_texts)):
                img = (batch_images[i, :, :, 0] * 255).numpy().astype(np.uint8)
                img = img.T
                title = f"Prediction: {pred_texts[i]}"
                ax[i // 4, i % 4].imshow(img, cmap="gray")
                ax[i // 4, i % 4].set_title(title)
                ax[i // 4, i % 4].axis("off")
        plt.show()


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





