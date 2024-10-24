import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    # Using dictionaries to simplify the list comprehension
    month = {
        'Jan': 0,
        'Feb': 1,
        'Mar': 2,
        'May': 3,
        'Apr': 4,
        'June': 5,
        'Jul': 6,
        'Aug': 7,
        'Sep': 8,
        'Oct': 9,
        'Nov': 10,
        'Dec': 11,

    }

    visitorType = {
        'Returning_Visitor': 1,
        'New_Visitor': 0,
        'Other': 0,
    }

    weekend = {
        'FALSE': 0,
        'TRUE': 1,
    }

    revenue = {
        'TRUE': 1,
        'FALSE': 0,
    }

    with open(filename) as f:
        reader = csv.DictReader(f)
        # using list comprehension to create a List of tuples, making a tuple so it only loops once.
        # Since many row were being returned as str, I added the int/float to turn them in the appropriated type.
        # other options would make the comprehension harder to understand.
        data = [(int(revenue[row["Revenue"]]), [int(row['Administrative']), float(row['Administrative_Duration']),
                                                int(row['Informational']), float(row['Informational_Duration']),
                                                int(row['ProductRelated']), float(row['ProductRelated_Duration']),
                                                float(row['BounceRates']), float(row['ExitRates']), float(row['PageValues']),
                                                float(row['SpecialDay']), int(month[row['Month']]), int(row['OperatingSystems']),
                                                int(row['Browser']), int(row['Region']), int(row['TrafficType']),
                                                int(visitorType[row['VisitorType']]),
                                                int(weekend[row['Weekend']])]) for row in reader]
    
    # Using Zip to unpack the list of tuples into two lists
    label, evidence = zip(*data)

    return evidence, label

    raise NotImplementedError


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """

    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence, labels)

    return model

    raise NotImplementedError


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    sensitivity = 0
    specificity = 0
    
    # number of times the label returned 0 or 1
    n0 = 0
    n1 = 0
    
    for prediction, label in zip(predictions, labels):
        if prediction == label:
            if prediction == 1:
                sensitivity += 1
                n1 += 1

            elif prediction == 0:
                specificity += 1
                n0 += 1

        else:
            if label == 1:
                n1 += 1

            elif label == 0:
                n0 += 1

    return (sensitivity/n1, specificity/n0)

    raise NotImplementedError


if __name__ == "__main__":
    main()
