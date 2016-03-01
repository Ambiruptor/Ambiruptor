
"""
Testing the implemented models with cross-validation
"""
from ambiruptor.library.learners.models import LinearSVMClassifier
from ambiruptor.library.learners.models import RbfSVMClassifier
from ambiruptor.library.learners.models import NaiveBayesClassifier
from ambiruptor.library.learners.models import DecisionTreeClassifier
from ambiruptor.library.learners.models import RandomForestClassifier


def benchmark(models, train_data):
    pass


if __name__ == '__main__':
    # grid search of best parameters for LinearSVM
    best_linear_C = None

    # grid search of best parameters for SVM RBF kernel
    best_rbf_gamma = None
    best_rbf_C = None

    # grid search of best parameters for Random Forests
    best_n_estimators = None

    # List of all models implemented:
    # if parametrized - with the best parameters found by grid search
    models = [("SVM Linear Kernel C=%f" % best_linear_C,
               LinearSVMClassifier()),
              ("SVM RBF Kernel C=%f gamma=%f" % (best_rbf_C, best_rbf_gamma),
               RbfSVMClassifier()),
              ("Gaussian Naive Bayes",
               NaiveBayesClassifier()),
              ("Decision Tree",
               DecisionTreeClassifier()),
              # ("Random Forests with %d estimators" % best_n_estimators,
              #  RandomForestClassifier())
              ]

    benchmark(models)
