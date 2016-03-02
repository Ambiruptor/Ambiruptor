
"""
Testing the implemented models with cross-validation
"""
from ambiruptor.library.preprocessors.data_structures import TrainData
from ambiruptor.library.preprocessors.data_structures import AmbiguousData

from ambiruptor.library.learners.models import LinearSVMClassifier
from ambiruptor.library.learners.models import RbfSVMClassifier
from ambiruptor.library.learners.models import NaiveBayesClassifier
from ambiruptor.library.learners.models import DecisionTreeClassifier
# from ambiruptor.library.learners.models import RandomForestClassifier

from sklearn.cross_validation import train_test_split
from sklearn.datasets import load_iris

import numpy as np
import time
import matplotlib.pyplot as plt


def benchmark(models, X, y):
    """Output the benchmark on provided learning models.

    calculate score and train time for each of them and
    output summary to the barplot.
    """
    print("---------------------------------------")
    print("Benchmark for different learning models:\n")
    scores_timed = []
    i = 1
    for name, model in models:
        print("%d) %s: \n" % (i, name))
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.33, random_state=42)
        train_data = TrainData(X_train, y_train.tolist())
        t = time.time()
        model.train(train_data)
        t = time.time() - t
        test_data = AmbiguousData(X_test, np.ndarray([0, 0]), y_test.tolist())
        print("Score: %.2f" % model.score(test_data))
        print("Training time: %f" % t)
        print("\n")
        i += 1
        scores_timed.append([model.score(test_data), t])
    scores_timed = np.array(scores_timed)

    # Plotting part
    ind = np.arange(scores_timed.shape[0])
    width = 0.35       # the width of the bars

    plt.figure(1)

    plt.subplot(211)
    plt.barh(ind, scores_timed[:, 0], width, color='#e93f4b', align='center')
    plt.title('Classification Scores')
    plt.xlabel('Score')
    plt.yticks(ind, [model[0] for model in models])
    plt.grid(True)

    plt.subplot(212)
    plt.barh(ind + width, scores_timed[:, 1], width, color='#4bdcb0',
             align='center')
    plt.grid(True)
    plt.title('Train time')
    plt.xlabel('Time in ms')
    plt.yticks(ind, [model[0] for model in models])

    plt.subplots_adjust(left=0.45, right=0.9, top=0.9, bottom=0.1)
    plt.tight_layout()

    plt.show()


if __name__ == '__main__':
    print("************* Learning Models Comparison ***************")

    # Here I load temporary dummy data
    iris = load_iris()
    X = iris.data
    y = iris.target

    print("-----------------------------------------------")
    print("Grid search of best C parameter for Linear SVM:\n")
    C_range = np.logspace(-2, 10, 13)

    # If we have used cross-validation, we could also choose the model
    # with the max accuracy, min training time
    scores_timed = []
    for C in C_range:
        model = LinearSVMClassifier(C=C)
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.33, random_state=42)
        train_data = TrainData(X_train, y_train.tolist())
        t = time.time()
        model.train(train_data)
        t = time.time() - t
        test_data = AmbiguousData(X_test, np.ndarray([0, 0]), y_test.tolist())
        scores_timed.append([C, model.score(test_data), t])

    scores_timed = np.array(scores_timed)
    best_linear_C = scores_timed[np.argmax(scores_timed[:, 1])][0]

    print("The best parameter is C=%.2f with a score of %.2f"
          % (best_linear_C, scores_timed[np.argmax(scores_timed[:, 1])][1]))

    print("------------------------------------------------------")
    print("Grid search of best C and gamma parameters for RBF SVM:\n")

    gamma_range = np.logspace(-9, 3, 13)

    scores_timed = []
    for C in C_range:
        for gamma in gamma_range:
            model = RbfSVMClassifier(C=C, gamma=gamma)
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.33, random_state=42)
            train_data = TrainData(X_train, y_train.tolist())
            t = time.time()
            model.train(train_data)
            t = time.time() - t
            test_data = AmbiguousData(X_test, np.ndarray([0, 0]), y_test.tolist())
            scores_timed.append([C, gamma, model.score(test_data), t])

    scores_timed = np.array(scores_timed)
    best_rbf_c = scores_timed[np.argmax(scores_timed[:, 2])][0]
    best_rbf_gamma = scores_timed[np.argmax(scores_timed[:, 2])][1]

    print("The best parameters are C=%.2f and gamma=%.2f with a score of %.2f"
          % (best_rbf_c, best_rbf_gamma, scores_timed[np.argmax(scores_timed[:, 2])][2]))

    # # grid search of best parameters for Random Forests
    # # best_n_estimators = None

    # List of all models implemented:
    # if parametrized - with the best parameters found by grid search
    models = [("SVM Linear Kernel C=%.2f" % best_linear_C,
               LinearSVMClassifier(C=best_linear_C)),
              ("SVM RBF Kernel C=%.2f gamma=%.2f" %
              (best_rbf_c, best_rbf_gamma),
               RbfSVMClassifier(C=best_rbf_c,
                                gamma=best_rbf_gamma)),
              ("Gaussian Naive Bayes",
               NaiveBayesClassifier()),
              ("Decision Tree",
               DecisionTreeClassifier()),
              # ("Random Forests with %d estimators" % best_n_estimators,
              #  RandomForestClassifier())
              ]

    benchmark(models, X, y)
