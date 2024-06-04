# Read me

The problem and it's full description is avaliable in the link: 
https://cs50.harvard.edu/ai/2024/projects/4/shopping/

## Introduction:

This project aim to write a classifier Ai that can reasonably predict whether a user on a shopping website will purchase something or not. This is done by training an Ai with that site's information on about 12,000 users, together with the KneighborsClassifiers from Sklearn. At the end, this project shows the Ai Sensitivity (True positive rate, how many of the times that the user purchased something and the Ai predicted he would) and it's Specificity (True negative rate, how many of the times the user didn't purchase something, the Ai predicted he wouldn't).

## Utilization

* if you didn't before, run pip3 install scikit-learn to instal Scikit-learn pakage

* Run in the terminal: python shopping.py data (python shopping.py shopping.csv if you are running it using the csv in this project.)

* The terminal will show the number of correct and incorrect predictions, as well as the sensitivity and specificity.

## Background:
When users are shopping online, not all will end up purchasing something. Most visitors to an online shopping website don’t end up going through with a purchase during that web browsing session. Though, it might be useful for a shopping website to be able to predict whether a user intends to make a purchase or not: perhaps displaying different content to the user, like showing the user a discount offer if the website believes the user isn’t planning to complete the purchase. How could a website determine a user’s purchasing intent? That’s where machine learning will come in.

My task in this problem is to build a nearest-neighbor classifier to solve this problem. Given information about a user — how many pages they’ve visited, whether they’re shopping on a weekend, what web browser they’re using, etc. — My classifier will predict whether the user will make a purchase. Meanwhile it won't be perfectly accurate, it should be better than guessing randomly. To train this classifier, I was provided with some data from a shopping website from about 12,000 users sessions.

How do we measure the accuracy of a system like this? If we have a testing data set, we could run our classifier on the data, and compute what proportion of the time we correctly classify the user’s intent. This would give us a single accuracy percentage. But that number might be a little misleading. Imagine, for example, if about 15% of all users end up going through with a purchase. A classifier that always predicted that the user would not go through with a purchase, then, we would measure as being 85% accurate: the only users it classifies incorrectly are the 15% of users who do go through with a purchase. And while 85% accuracy sounds pretty good, that doesn’t seem like a very useful classifier.

Instead, we’ll measure two values: sensitivity (also known as the “true positive rate”) and specificity (also known as the “true negative rate”). Sensitivity refers to the proportion of positive examples that were correctly identified: in other words, the proportion of users who did go through with a purchase who were correctly identified. Specificity refers to the proportion of negative examples that were correctly identified: in this case, the proportion of users who did not go through with a purchase who were correctly identified. So our “always guess no” classifier from before would have perfect specificity (1.0) but no sensitivity (0.0). My goal is to build a classifier that performs reasonably on both metrics.

## Understanding:

This project is composed of the files Shopping.csv and shopping.py:

Shopping.csv contains the data set provided for this project. There are about 12,000 user sessions represented in that spreadsheet. Each row representing a user session. This file contains much information about that user's session, from which type of site they visited, how much time they spend there. Information from Google Analytics about the pages visited. Special day is the measure of how close the date of the user's session is to a special day. VisitorsType shower whether the user is a returning visitor or nor. While the last column show the Revenue, indicating whether the user ultimately made a purchase or not. this is the column that we’d like to learn to predict (the “label”), based on the values for all the other columns (the “evidence”).

Next, take a look at shopping.py. The main function loads data from a CSV spreadsheet by calling the load_data function and splits the data into a training and testing set. The train_model function is then called to train a machine learning model on the training data. Then, the model is used to make predictions on the testing data set. Finally, the evaluate function determines the sensitivity and specificity of the model, before the results are ultimately printed to the terminal.

The functions load_data, train_model, and evaluate were left for me to implement.

## Specification:

### Load_Data:

* Takes a CSV filename as argument, open that file, reads it and returns a tuple (evidence, labels).

* Evidence is a list of all the information contained in each row of the CSV.

* Labels is a list of all the labels on each row.

* To build a nearest-neighbor classifier, all of our data needs to be numeric. So any value in the evidence that wasn't numeric was turned into int or float.

* each element in label has either 1 (True) or 0 (False)

### Evaluate:

* Accepts a list of Labels (the Y test, or the true values to be used to test predictions) and a list of predictions (the labels predicted by the classifier). Returning two floating-point values (sensitivity, specificity).

* Sensitivity is a floating-point value from 0 to 1 representing the “true positive rate”: the proportion of actual positive labels that were accurately identified.

* Specificity is a floating-point value from 0 to 1 representing the “true negative rate”: the proportion of actual negative labels that were accurately identified.

* It was assumed that each label will be 1 for positive results (users who did go through with a purchase) or 0 for negative results (users who did not go through with a purchase).

* It was assumed that the list of true labels will contain at least one positive label and at least one negative label.