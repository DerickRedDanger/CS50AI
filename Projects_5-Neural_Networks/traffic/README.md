# Neural Network for Road Sign Classification

## Problem Description
The full problem description is available at the following link: [CS50 AI Project 5: Traffic](https://cs50.harvard.edu/ai/2024/projects/5/traffic/).

## Introduction

This project aims to create a neural network capable of classifying road signs based on images. Using TensorFlow's Keras API, a high-level neural networks API, I created a convolutional neural network trained and tested on the German Traffic Sign Recognition Benchmark (GTSRB) dataset.

The neural network was developed through multiple tests and experiments, which are recorded in the `experimentation_process.md` file. The focus was on achieving the highest possible accuracy while maintaining quick prediction times.

As an additional step, I created an automated version that trains the AI until it reaches a specified accuracy on both training and testing datasets. The resulting models, `Traffic_ai.h5` and `Traffic_ai.keras`, achieved an accuracy of 0.995 on both the final epoch and test, with a prediction time of 50-60ms per image.

## Utilization

### Prerequisites

- Navigate to the project directory: `cd traffic`
- Install the required dependencies: `pip3 install -r requirements.txt` (only needs to be done once).

### Running `traffic.py`

1. Run in the terminal: `python traffic.py gtsrb`.
2. The terminal will display the AI's training progress, including the current epoch, time taken for each epoch, time per batch in milliseconds, accuracy, loss, precision, and recall.
3. After the final epoch, the evaluation (test) progress will be displayed, showing the same metrics as during training. This tests how well the model handles unseen data.
4. Finally, the terminal will display the progress of predicting a single image and the time taken for the prediction.
5. To train and save an AI model, run: `python traffic.py gtsrb [model_name.h5 or model_name.keras]`.

**Note:** The training process includes a callback function that will stop training once the model reaches an accuracy of 0.995. This is to quickly save a highly accurate AI model.

**Metrics Explanation:**
- **Loss:** Indicates how well the model's predictions match the true values. Lower is better.
- **Precision:** Ratio of correctly predicted positive observations to total predicted positives.
- **Recall (Sensitivity):** Ratio of correctly predicted positive observations to all actual positives.

### Running `traffic_automated_version.py`

1. This script works similarly to `traffic.py` and uses the same commands.
2. The main difference is that it continues training the same AI model until it reaches a set accuracy on both training and testing datasets.
3. The accuracy and most constants used in the training are defined and explained at the start of the file for easier control over the training process.

**Default Values:**
- `EPOCHS = 100`
- `MAX_EPOCHS = 500`
- `MAX_TRAINING_ROW = 100`
- `MAX_RESETS = 50`
- `TRAINING_ACCURACY = 0.995`
- `TEST_ACCURACY = 0.995`

**Note:** Achieving an accuracy of 0.995 on both training and test is rare, so expect the program to run for extended periods, and it may sometimes fail to create such a model.

**Accuracy Note:** The accuracy reported during training is a running average at the current point in the epoch, meaning early batches influence it more. The program might keep training even if Keras reports an accuracy of 0.995, and the printed accuracy might differ from Keras's reported value.

## Background

As research in self-driving cars progresses, one key challenge is computer vision, enabling cars to understand their environment from digital images. This involves recognizing and distinguishing road signs such as stop signs, speed limit signs, yield signs, and more.

In this project, TensorFlow is used to build a neural network to classify road signs based on images. The GTSRB dataset, containing thousands of images of 43 different road sign types, is used for training and testing.

## Understanding the Data

The `gtsrb` directory contains 43 subdirectories, each representing a different type of road sign (numbered 0 through 42). Within each subdirectory are images of that traffic sign type.

## Code Overview

### `traffic.py`

- **Main Function:** Accepts a data directory and optionally a filename to save the trained model. Loads data and labels from the data directory, splits it into training and testing sets, compiles a neural network, trains it, evaluates it, and saves the model if a filename is provided.

- **Functions:**
  - `load_data(data_dir)`: Returns image arrays and labels for the dataset. Returns a tuple `(images, labels)`, where `images` is a list of `numpy.ndarray` representing images, and `labels` is a list of integers representing the category numbers.
  - `get_model()`: Returns a compiled neural network model.
  - `MyCallback`: Stops training when the model's accuracy reaches 0.995 or higher.

### `traffic_automated_version.py`

- **Main Function:** Similar to the original, but includes nested loops and additional constants for training until a set accuracy is reached or maximum resets are achieved. Saves the model if it passes accuracy tests and a filename is given.

- **Functions:**
  - `load_data(data_dir)`: Same as the original.
  - `get_model()`: Same as the original.
  - `MyCallback`: Tracks training iterations and resets. Stops training if the model reaches the set accuracy or a specified number of resets.

## Experimentation Process

The `Experimentation_Summary.md` file documents the experimentation process, detailing what was tried, what worked well, what didn’t, and observations made during the process.

The `Experimentation_Process.md` file documented the experimentation process in more details