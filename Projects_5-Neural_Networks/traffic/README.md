The problem and it's full description is avaliable in the link: 
https://cs50.harvard.edu/ai/2024/projects/5/traffic/

## Introduction:

This project aims at creating a neural network capable of classifying road signs based on an image of those signs.

For this project, Tensorflow's Keras (a high-level neural networks API) was utilized to create a convolutional network, while using the German Traffic Sign Recognition Benchmark (GTSRB) dataset for training and testing. 

The neural network was created through multiple tests and experimentation, which were recorded on the file experimentation_process.md, and was focused on achieving for the highest accuracy possible while still making quick predictions.

As a step beyond what I should do, and for the sake of practice and curiosity, I also created an automated version meant to train an Ai until it achieves a certain accuracy on both training and testing.

The Files Traffic_ai.h5 and Traffic_ai.keras are two Ai created through that automation, both achieved an accuracy of 0.995 (or slightly higher) on both its last epoch and test while needing 50-60ms to predict a single image.

## Utilization:

* cd inside traffic

* pip3 install -r requirements.txt (only need to be done once)

### Traffic.py:

* Run in the terminal: python traffic.py gtsrb 

* The terminal will show the progress of the Ai's training. On which epoch it's, it's progress on that epoch, how log it took to train in that epoch, the time in milliseconds per batch on that epoch, it's accuracy, loss, precision and recall (Will be explained in obs2.)

* After the last epoch, it will show the progress on the evaluation (test), showing the same metrics as in the training. This test show how well the model deals with unseen data.

* Lastly, it will show the progress of predicting a single image and the time it took to do so.

* if you'd like both to train and save an Ai, run in the terminal : python traffic.py gtsrb [model_name.h5 or model_name.keras]

* Obs: The training has a Callback function that will exit the training should the model reach an accuracy of 0.995. This is done to quickly save an Ai that reached a high accuracy. 

* Obs2: the Metric Loss symbolizes how well the model's prediction matches the true value, the lower, the better. Precision is the ratio of correctly predicted positive observations to the total predicted positives. Recall (Sensitivity) is the ratio of correctly predicted positive observations to all observations in actual class.

### Traffic_automated_version.py:

* works in the exact same manner as traffic.py and uses the same commands.

* Main difference being that it will continue training the same Ai till it reaches a set accuracy on both training and testing.

* That accuracy and most constants utilized in the training are present and explained at the start of the file, allowing for an easier control over the training.

* the default values are EPOCHS = 100, MAX_EPOCHES = 500, MAX_TRAINING_ROW = 100, MAX_RESETS = 50, TRAINING_ACCURACY = 0.995, TEST_ACCURACY = 0.995

* Obs: be warned that reaching an accuracy of 0.995 on both training and test is rare, so if using default values, expect this program to run for long periods of times, and it may yet fail to create such model at times.

* Obs2: The accuracy showed at the last epoch is not the final accuracy of a epoch. When Keras reports the accuracy during training, it's giving this running average at the current point in the epoch. This means that early batches have a larger influence on this reported accuracy than later batches. So don't be surprised if the program keeps training even if keras returned an accuracy of 0.995, nor if the print showing the accuracy is different from Keras.

## Background:

As research continues in the development of self-driving cars, one of the key challenges is computer vision, allowing these cars to develop an understanding of their environment from digital images. In particular, this involves the ability to recognize and distinguish road signs – stop signs, speed limit signs, yield signs, and more.

In this project, I’ll use TensorFlow to build a neural network to classify road signs based on an image of those signs. To do so, I’ll need a labeled dataset: a collection of images that have already been categorized by the road sign represented in them.

Several such data sets exist, but for this project, we’ll use the German Traffic Sign Recognition Benchmark (GTSRB) dataset, which contains thousands of images of 43 different kinds of road signs.

## Understanding:

First, take a look at the data set by opening the gtsrb directory. You’ll notice 43 subdirectories in this dataset, numbered 0 through 42. Each numbered subdirectory represents a different category (a different type of road sign). Within each traffic sign’s directory is a collection of images of that type of traffic sign.

Next, take a look at traffic.py. In the main function, we accept as command-line arguments a directory containing the data and (optionally) a filename to which to save the trained model. The data and corresponding labels are then loaded from the data directory (via the load_data function) and split into training and testing sets. After that, the get_model function is called to obtain a compiled neural network that is then fitted on the training data. The model is then evaluated on the testing data. Finally, if a model filename was provided, the trained model is saved to disk.

The load_data and get_model functions were left to me to implement.

## Specification:

### traffic.py:

#### load_data:

* Accept as an argument data_dir, representing the path to a directory where the data is stored, and return image arrays and labels for each image in the data set.

* Returns a tuple (images, labels). Images is a list of all images in the data set, where each image is represented as a numpy.ndarray of the appropriate size. Labels is a list of integers, representing the category number for each of the corresponding images in the images list.
* This function is platform-independent: that is to say, it works regardless of operating system.

#### get_model:

* Return a compiled neural network model.

#### MyCallback:

* when the model's accuracy reaches 0.995 or higher, it will stop training

### experimentation_process.md:

* documents my experimentation process. What I tried, what worked well, what didn’t work well, What I noticed.

### traffic_automated_version.py:

#### Main():

* Works akin to the original, but has nested loops and more constants, allowing it to train a Model util it reaches a certain accuracy or reaches the maximum set amount of reset. If the model passes both accuracy test and a filename was given, that model will saved.

#### Load_data and Get_model:

* Same as the original. 

#### MyCallback:

* Saves the amount of times this model was trained in a roll (without reset) and the number of times this model reached low accuracy during a same training.

* If this model achieves an accuracy equal or higher than a given TRAINING_ACCURACY, stop training and checks its test's accuracy.

* If this model reaches low accuracy 6 times during the same training, it stops training and is reset. (This means this model was stuck at low accuracy)

* If this model trained the set MAX_EPOCHES amount of epoches, stop training and is evaluated. (Meaning, this model will be reset if it didn't reach the set accuracy.)