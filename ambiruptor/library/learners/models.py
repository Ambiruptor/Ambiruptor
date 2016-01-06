"""
A collection of classes implementing learning models for diasmbiguation

"""

import numpy as np
import pickle
from sklearn.svm import LinearSVC
from sklearn.multiclass import OneVsRestClassifier

from ambiruptor.base.core import Learner


class LinearSVMClassifier(Learner):
    def __init__(self):
        """Init the learning model"""
        self.model = OneVsRestClassifier(LinearSVC())

    def train(self, train_data):
        """Train the model using the training set"""
        self.model.fit(train_data.data, train_data.senses)

    def predict(self, ambiguous_data):
        return self.model.predict(ambiguous_data.data)


# TODO : New models...
