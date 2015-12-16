import abstract

import pickle
from sklearn.svm import LinearSVC


class LinearSVMClassifier(abstract.Learning):
    def __init__(self):
        """Init the learning model"""
        # TODO: pass the parameters of the model
        # (for now, default parameters are set)
        self.model = LinearSVC()

    def train(self, train_data):
        """Train the model using the training set"""
        self.word = train_data.word
        self.senses = train_data.senses
        self.model.fit(train_data.data, train_data.labels)
        return

    def predict(self, data):
        """
        Guess the best sense for a features vector
        @param(vector) : features vector
        @return : word sense
        """
        labels = self.model.predict(data)
        # preprocess labels somehow
        return labels

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
