
# Shopping Project

## Problem Description

The full problem description is available at the following link: [CS50 AI Project 4 - Shopping](https://cs50.harvard.edu/ai/2024/projects/4/shopping/)

## Introduction

This project aims to develop a classifier AI that can reasonably predict whether a user on a shopping website will make a purchase or not. This is achieved by training an AI with information on about 12,000 users from that site, using the `KNeighborsClassifier` from `sklearn`. The project evaluates the AI's performance by calculating its Sensitivity (True Positive Rate: how often the AI correctly predicts a purchase) and Specificity (True Negative Rate: how often the AI correctly predicts no purchase).

## Utilization

1. If not already installed, run `pip3 install scikit-learn` to install the `scikit-learn` package.
2. Run the following command in the terminal:
   ```bash
   python shopping.py data
   ```
   Or, if you are using the provided CSV file, run:
   ```bash
   python shopping.py shopping.csv
   ```
3. The terminal will display the number of correct and incorrect predictions, as well as the sensitivity and specificity.

## Background

When users shop online, not all will end up making a purchase. Most visitors to an online shopping website don’t complete a purchase during that session. Predicting whether a user intends to make a purchase could be useful for a shopping website, allowing it to display different content, such as discount offers, to users who may not complete their purchase. Machine learning can help determine a user’s purchasing intent.

The task in this project is to build a nearest-neighbor classifier to solve this problem. Given user information—such as the number of pages visited, whether it's a weekend, the web browser used, etc.—the classifier predicts whether the user will make a purchase. Though not perfectly accurate, it should perform better than random guessing. The classifier is trained using data from about 12,000 user sessions from a shopping website.

Accuracy is measured by running the classifier on testing data and calculating the proportion of correctly classified user intents. However, this accuracy percentage might be misleading. For instance, if 15% of users make a purchase, a classifier that always predicts no purchase would be 85% accurate but not very useful.

Therefore, two metrics are measured: sensitivity (true positive rate) and specificity (true negative rate). Sensitivity is the proportion of users who made a purchase and were correctly identified, while specificity is the proportion of users who did not make a purchase and were correctly identified. An “always guess no” classifier would have perfect specificity (1.0) but no sensitivity (0.0). The goal is to build a classifier that performs reasonably on both metrics.

## Understanding

This project consists of the files `shopping.csv` and `shopping.py`.

- `shopping.csv` contains the dataset with about 12,000 user sessions, each row representing a session. The dataset includes information about the session, such as the types of sites visited, time spent, and Google Analytics data. The "Special Day" column measures how close the session date is to a special day. The "VisitorType" column indicates whether the user is a returning visitor. The last column, "Revenue," indicates whether the user made a purchase (the label to be predicted).

- `shopping.py` contains the main function, which loads data from the CSV file, splits it into training and testing sets, trains a machine learning model, and makes predictions. The `evaluate` function determines the model's sensitivity and specificity, printing the results to the terminal.

The functions `load_data`, `train_model`, and `evaluate` were implemented as part of this project.

## Specification

### `load_data`

- Takes a CSV filename as an argument, opens the file, reads it, and returns a tuple `(evidence, labels)`.
- `Evidence` is a list of all the information contained in each row of the CSV.
- `Labels` is a list of all the labels in each row.
- To build a nearest-neighbor classifier, all data needs to be numeric. Non-numeric values in the evidence were converted to integers or floats.
- Each element in `labels` is either 1 (True) or 0 (False).

### `evaluate`

- Accepts a list of `labels` (the true values for testing) and a list of `predictions` (the labels predicted by the classifier). Returns two floating-point values: `sensitivity` and `specificity`.
- `Sensitivity` is a floating-point value from 0 to 1 representing the true positive rate: the proportion of actual positive labels accurately identified.
- `Specificity` is a floating-point value from 0 to 1 representing the true negative rate: the proportion of actual negative labels accurately identified.
- Assumes each label is 1 for positive results (users who made a purchase) or 0 for negative results (users who did not make a purchase).
- Assumes the list of true labels contains at least one positive label and one negative label.
```

Feel free to make any adjustments or let me know if there are any additional details you'd like to include!