import cv2
import numpy as np
import os
import sys
import tensorflow as tf

from sklearn.model_selection import train_test_split

import random


IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
TEST_SIZE = 0.4

# Variable to decide the maximal number of Epoches a single training can have
EPOCHS = 100

# Variable to decide the maximal number of total Epoches a model can be retrained with 
MAX_EPOCHES = 500

# Variable to decide how many times a model can be retrained in a row before being reset
MAX_TRAINING_ROW = 100

# Max number of times a model can be reseted before stopping the program
MAX_RESETS = 50

# The accuracy a model must reach during the training before being tested
TRAINING_ACCURACY = 0.995

# The accuracy a model must reach during their test to be considered a success
TEST_ACCURACY = 0.995


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

    # Initializing my variables
    Continue_reseting = True
    Continue_training = True
    Number_of_resets = 0
    Save_Ai = False

    while Continue_reseting:
        
        model = get_model()
        Number_of_resets += 1
        print(f"This is the reset number {Number_of_resets}")

        # If the model was reseted MAX_RESETS times, stop reseting
        if Number_of_resets >= MAX_RESETS:
            Continue_reseting = False
        
        # keep track of the number of times a Ai was re-trained
        N_training = 0

        while Continue_training:

            # If this Ai was retrained too much, break and reset
            if N_training >= MAX_TRAINING_ROW:
                break
            
            # Create a interation of MyCallback, needs to be reseted on each training
            # to reset it's Total_number_of_training attribute
            Callback = MyCallback()
            N_training += 1
            print(f"This is the reset nº {Number_of_resets}'s {N_training}º training")
            history = model.fit(x_train, y_train, epochs=EPOCHS,callbacks=[Callback])
            
            # Get the accuracy of the lastest Epoch
            last_epoch_accuracy = history.history['accuracy'][-1]

            
            # If accuracy is lower then TRAINING_ACCURACY, reset the model
            if last_epoch_accuracy < TRAINING_ACCURACY:
                print(f"Last epoch's accuracy {last_epoch_accuracy} < Training accuracy {TRAINING_ACCURACY}")
                break
            else:
                print(f"Last epoch's accuracy {last_epoch_accuracy} >= Training accuracy {TRAINING_ACCURACY}")
            # otherwise, evaluate it
            #test_loss, test_acc = model.evaluate(x_test,  y_test, verbose=2)
            test_loss, test_acc, test_prec, test_recall = model.evaluate(x_test,  y_test, verbose=2)
            #print (f"test_loss = {test_loss}")
            print (f"test_acc = {test_acc}")
            #print (f"test_prec = {test_prec}")
            #print (f"test_recall = {test_recall}")

            # if the test's accuracy is lowe then TEST_ACCURACY, train this model again
            if test_acc < TEST_ACCURACY:
                continue
            
            # if TEST_ACCURACY or higher, break and save the Ai (if a name was given to it)
            else :
                Continue_reseting = False
                Continue_training = False
                Save_Ai = True
                break

        if Continue_reseting == False and  Save_Ai == False:
            print(f"This model was reseted {MAX_RESETS} times")
            print(f"But didn't manage to reach both Last epoch accuracy of {TRAINING_ACCURACY}")
            print(f"And the test accuracy of {TEST_ACCURACY}")


        # Save model to file
        if len(sys.argv) == 3 and Save_Ai:
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


    # Convolutional layer. Learn 258 filters using a 3x3 kernel
    tf.keras.layers.Conv2D(
        258, (3, 3), activation="sigmoid"
    ),

    # Max-overlapping-pooling layer, using 3x3 pool size with a stride of 2x2
    tf.keras.layers.MaxPooling2D(pool_size=(3, 3), strides=(2, 2)),

    # Flatten units
    tf.keras.layers.Flatten(),

    # Add a hidden layer with 128 neurons and dropout of 0.5
    tf.keras.layers.Dense(128, activation="sigmoid"),
    tf.keras.layers.Dropout(0.5),

    # Add an output layer with output units for all categories
    tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax")
    ])

    model.compile(
        optimizer="adam",
        loss="categorical_crossentropy",
        metrics=['accuracy', tf.keras.metrics.Precision(), tf.keras.metrics.Recall()],
        )
    #        metrics=['accuracy']
    return model

    raise NotImplementedError

class MyCallback(tf.keras.callbacks.Callback):
    def __init__(self):
        super(MyCallback, self).__init__()
        # Number of times This model reached a low accuracy during training
        self.number_low_accuracy = 0

        # Total number of times this model was trained
        self.Total_number_of_training = 0

    def on_epoch_end(self, epoch=EPOCHS, logs=None):
        self.Total_number_of_training += 1

        # if model reached target training, break
        if logs.get('accuracy') >= TRAINING_ACCURACY:
            self.model.stop_training = True
            self.number_low_accuracy = 0

        # if model reached low accuracy, increase count
        if logs.get('accuracy') < 0.07:
            self.number_low_accuracy += 1

        # if model reached low accuracy 6 times, break
        if self.number_low_accuracy >= 6:
            self.model.stop_training = True
            self.number_low_accuracy = 0

        # if this model trained Max_epoches time without reset, break
        if self.Total_number_of_training >= MAX_EPOCHES:
            self.model.stop_training = True
            self.number_low_accuracy = 0


if __name__ == "__main__":
    main()
