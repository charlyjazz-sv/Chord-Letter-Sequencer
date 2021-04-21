import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

def CRNN(lr, img_width, img_height, total_labels):
    # Inputs to the CNN+RNN+CTC model
    input_img = layers.Input(shape=(img_width, img_height, 1), name="image", dtype="float32")
    
    # Inputs to the RNN+CTC model
    # input_img = layers.Input(shape=(img_width, img_height), name="image", dtype="float32")

    # ---------------------------------------------- CNV --------------------------------------------------
    # First conv block
    x = layers.Conv2D(
        32,
        (3, 3),
        activation="relu",
        kernel_initializer="he_normal",
        padding="same",
        name="Conv1",
    )(input_img)
    x = layers.MaxPooling2D((2, 2), name="pool1")(x)

    # Second conv block
    x = layers.Conv2D(
        64,
        (3, 3),
        activation="relu",
        kernel_initializer="he_normal",
        padding="same",
        name="Conv2",
    )(x)
    x = layers.MaxPooling2D((2, 2), name="pool2")(x)

    # We have used two max pool with pool size and strides 2.
    # Hence, downsampled feature maps are 4x smaller. The number of
    # filters in the last layer is 64. Reshape accordingly before
    # passing the output to the RNN part of the model
    new_shape = ((img_width // 4), (img_height // 4) * 64)
    x = layers.Reshape(target_shape=new_shape, name="reshape")(x)
    x = layers.Dense(64, activation="relu", name="dense1")(x)
    # x = layers.Dropout(0.2)(x)
    # ---------------------------------------------- CNV --------------------------------------------------


    # RNN
    # x = layers.GRU(128, return_sequences=True)(x)
    x = layers.Bidirectional(layers.LSTM(64, return_sequences=True, dropout=0.25))(x)

    # Output layer
    output = layers.Dense(total_labels + 1, activation="softmax", name="dense2")(x)

    # Define the model
    model = keras.models.Model(
        inputs=input_img, outputs=output, name="ocr_model_v1"
    )

    def ctcloss(y_true, y_pred):
        batch_len = tf.cast(tf.shape(y_true)[0], dtype="int64")
        input_length = tf.cast(tf.shape(y_pred)[1], dtype="int64")
        label_length = tf.cast(tf.shape(y_true)[1], dtype="int64")
        input_length = input_length * tf.ones(shape=(batch_len, 1), dtype="int64")
        label_length = label_length * tf.ones(shape=(batch_len, 1), dtype="int64")
        loss = keras.backend.ctc_batch_cost(y_true, y_pred, input_length, label_length)
        return loss 

    # Optimizer
    opt = keras.optimizers.Adam(lr=lr)
    # Compile the model and return
    model.compile(optimizer=opt, loss=ctcloss)
    model.summary()

    return model

if __name__ == '__main__':
    model = CRNN(0.001, 200, 50, 19)







