import cv2
import numpy as np
import os
import sys
import tensorflow as tf

from sklearn.model_selection import train_test_split

import random

EPOCHS = 100
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python traffic.py data_directory [model.h5]")

    # Get image arrays and labels for all image files
    images, labels = load_data(sys.argv[1])

    # Split data into training and testing sets
    labels = tf.keras.utils.to_categorical(labels)
    x_train, x_test, y_train, y_test = train_test_split(
        np.array(images), np.array(labels), test_size=TEST_SIZE
    )

    # Get a compiled neural network
    model = get_model()

    # Fit model on training data
    model.fit(x_train, y_train, epochs=EPOCHS,callbacks=[MyCallback()])

    # Evaluate neural network performance
    model.evaluate(x_test,  y_test, verbose=2)

    ## Student made
    # making a prediction to check how long it tooks to make a prediction
    test = random.choice(x_test)
    test = np.expand_dims(test, axis=0)
    predictions = model.predict(test)


    # Save model to file
    if len(sys.argv) == 3:
        filename = sys.argv[2]
        model.save(filename)
        print(f"Model saved to {filename}.")


def load_data(data_dir):
    """
    Load image data from directory `data_dir`.

    Assume `data_dir` has one directory named after each category, numbered
    0 through NUM_CATEGORIES - 1. Inside each category directory will be some
    number of image files.

    Return tuple `(images, labels)`. `images` should be a list of all
    of the images in the data directory, where each image is formatted as a
    numpy ndarray with dimensions IMG_WIDTH x IMG_HEIGHT x 3. `labels` should
    be a list of integer labels, representing the categories for each of the
    corresponding `images`.
    """

    labels = os.listdir(data_dir)
    tuples = []

    for label in labels:
        Full_label_path = os.path.join(data_dir, label)
        list_images_names = os.listdir(Full_label_path)
        
        for image_name in list_images_names:
            Full_image_path = os.path.join(Full_label_path, image_name)
            image = cv2.imread(Full_image_path)
            if image is not None:
                resized_img = cv2.resize(image, (IMG_WIDTH, IMG_HEIGHT))
                tuples.append((resized_img, label))

    Images, Labels = zip(*tuples)
    
    return Images, Labels

    raise NotImplementedError


def get_model():
    """
    Returns a compiled convolutional neural network model. Assume that the
    `input_shape` of the first layer is `(IMG_WIDTH, IMG_HEIGHT, 3)`.
    The output layer should have `NUM_CATEGORIES` units, one for each category.
    """

    # Create a convolutional neural network
    model = tf.keras.models.Sequential([

    # Convolutional layer. Learn 32 filters using a 3x3 kernel
    tf.keras.layers.Conv2D(
        32, (3, 3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)
    ),

    # averange - pooling layer, using 3x3 pool size
    tf.keras.layers.AveragePooling2D(pool_size=(3, 3)),


    # Convolutional layer. Learn 96 filters using a 3x3 kernel
    tf.keras.layers.Conv2D(
        258, (3, 3), activation="sigmoid"
    ),

    # Max-overlapping-pooling layer, using 3x3 pool size with a stride of 2x2
    tf.keras.layers.MaxPooling2D(pool_size=(3, 3), strides=(2, 2)),

    # Flatten units
    tf.keras.layers.Flatten(),

    # Add a hidden layer with dropout
    tf.keras.layers.Dense(128, activation="sigmoid"),
    tf.keras.layers.Dropout(0.5),

    # Add an output layer with output units for all categories
    tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax")
    ])

    model.compile(
        optimizer="adam",
        loss="categorical_crossentropy",
        metrics=['accuracy', tf.keras.metrics.Precision(), tf.keras.metrics.Recall()]
        )

    return model

    raise NotImplementedError

class MyCallback(tf.keras.callbacks.Callback):
    def on_epoch_end(self, epoch=EPOCHS, logs=None):
        if logs.get('accuracy') > 0.995:
            self.model.stop_training = True


if __name__ == "__main__":
    main()
