"""
A collection of classes implementing learning models for diasmbiguation
- SVM Classifier with Linear kernel
(http://scikit-learn.org/stable/modules/generated/sklearn.svm.LinearSVC.html)
- SVM Classifier with Radial Basis Function kernel
(http://scikit-learn.org/stable/auto_examples/svm/plot_rbf_parameters.html#example-svm-plot-rbf-parameters-py)
- Gaussian Naive Bayes Classifier
(http://scikit-learn.org/stable/modules/generated/sklearn.naive_bayes.GaussianNB.html#sklearn.naive_bayes.GaussianNB)
- Decision Tree Classifier
(http://scikit-learn.org/stable/modules/tree.html#classification)
- Forests of randomized trees
(http://scikit-learn.org/stable/modules/ensemble.html#forests-of-randomized-trees)
"""

import numpy as np
import pickle
from sklearn.svm import LinearSVC, SVC
from sklearn.multiclass import OneVsRestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier as DecisionTree
from sklearn.ensemble import RandomForestClassifier as RanomForest
from sklearn.neighbors import KNeighborsClassifier as KNeighbors

from ambiruptor.base.core import Learner

# Parametrized by 'C' - Penalty parameter of the error term.
class LinearSVMClassifier(Learner):
    def __init__(self, C=1.0):
        """Init the learning model"""
        self.model = OneVsRestClassifier(LinearSVC(C=C))

# Parametrized by
# 'C' that trades off misclassification of training examples against simplicity of the decision surface
# 'gamma' that defines how far the influence of a single training example reaches
# model parameters
class RbfSVMClassifier(Learner):
    def __init__(self, C=1.0, gamma='auto'):
        """Init the learning model"""
        self.model = OneVsRestClassifier(SVC(C=C, gamma=gamma, kernel='rbf'))

class NaiveBayesClassifier(Learner):
    def __init__(self):
        """Init the learning model"""
        self.model = OneVsRestClassifier(GaussianNB())

class DecisionTreeClassifier(Learner):
    def __init__(self):
        """Init the learning model"""
        self.model = OneVsRestClassifier(DecisionTree())

# Parametrized with number of estimators
# default 5 - ?
class RandomForestClassifier(Learner):
    def __init__(self, n_estimators=None):
        """Init the learning model"""
        self.model = OneVsRestClassifier(RandomForest(n_estimators))

class KNeighborsClassifier(Learner):
    def __init__(self, n_neighbors=1):
        """Init the learning model"""
        self.model = OneVsRestClassifier(KNeighbors(n_neighbors))


