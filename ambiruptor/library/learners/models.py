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
        # TODO: pass the parameters of the model
        # (for now, default parameters are set)
        # Default constructor will initialize empty dict of models
        self.models = dict()

    def train(self, train_data):
        """Train the model using the training set"""
        # TODO: pass the parameters of the model
        # (for now, default parameters are set)
        for word in train_data.senses:
            self.models.update({
                word: (train_data.senses[word],
                       OneVsRestClassifier(LinearSVC()))
            })
        # Here maybe preprocessor of the labels etc
            self.models[word][1].fit(train_data.X[word],
                                     train_data.labels[word])
        return

    def predict(self, data):
        """
        Guess the best sense for a features vector
        @param(vector) : features vector
        @return : word sense
        """
        result = np.zeros((len(data.targets)), dtype=object)
        for word in self.models:
            local_indices = np.array([i for i, target in enumerate(data.targets) if target[1] == word])
            result[local_indices] = self.models[word][1].predict(
                data.data[local_indices, ])
        # preprocess labels somehow
        return result

    def load(self, filename):
        """Load a model from a binary file"""
        with open(filename, 'rb') as f:
            tmp_dict = pickle.loads(f)
        if tmp_dict is not None:
            self.__dict__.update(tmp_dict)
        return

    def dump(self, filename):
        """Store a model into a binary file"""
        with open(filename, 'w') as f:
            pickle.dump(self.__dict__, f)
        return