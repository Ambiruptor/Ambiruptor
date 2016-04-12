"""Core base classes"""

from abc import ABCMeta, abstractmethod
from sklearn import cross_validation, metrics, preprocessing

import pickle



class DocStringInheritor(ABCMeta):
    """A metaclass for inheriting docstrings form the parent class.
    (from stackoverflow answer: http://stackoverflow.com/questions/8100166/
    inheriting-methods-docstrings-in-python)
    """
    def __new__(meta, name, bases, clsdict):
        if not('__doc__' in clsdict and clsdict['__doc__']):
            for mro_cls in (mro_cls
                            for base in bases for mro_cls in base.mro()):
                doc = mro_cls.__doc__
                if doc:
                    clsdict['__doc__'] = doc
                    break
        for attr, attribute in clsdict.items():
            if not attribute.__doc__:
                for mro_cls in (mro_cls
                                for base in bases for mro_cls in base.mro()
                                if hasattr(mro_cls, attr)):
                    doc = getattr(getattr(mro_cls, attr), '__doc__')
                    if doc:
                        attribute.__doc__ = doc
                        break
        return ABCMeta.__new__(meta, name, bases, clsdict)


class Learner(object):
    """Abstract class for learning."""

    __metaclass__ = DocStringInheritor
    lb = None
    model = None

    def __init__(self):
        """Init the learning model."""
        pass
    
    def fit(self, train_data):
        """Provide the interface for scikit-learn utils
        simply calling the train method.
        """
        return self.train(train_data)
    
    def scoring(y_pred, y):
        scores = dict()
        scores["accuracy"] = metrics.accuracy_score(y_pred, y)
        scores["f1"] = metrics.f1_score(y_pred, y, average="macro")
        scores["precision"] = metrics.precision_score(y_pred, y, average="macro")
        scores["recall"] = metrics.recall_score(y_pred, y, average="macro")
        return scores

    def score(self, train_data):
        """Provide the scoring interface for scikit-learn utils."""
        return self.model.score(train_data.data, train_data.senses)
    
    def scores(self, train_data):
        """Provide the scoring interface for scikit-learn utils."""
        y_correct = train_data.senses
        y_predict = self.model.predict(train_data.data)
        return Learner.scoring(y_predict, y_correct)

    def get_params(self, deep=True):
        """Provide the get_params interface for scikit-learn utils."""
        return self.model.get_params(deep)


    def load(self, filename):
        """Load a model from a binary file."""
        with open(filename, 'rb') as f:
            tmp_dict = pickle.loads(f)
        if tmp_dict is not None:
            self.__dict__ = tmp_dict

    def export(self, filename):
        """Store a model into a binary file."""
        with open(filename, 'wb') as f:
            pickle.dump(self.__dict__, f)

    def cross_validation_scores(self, train_data, cv=10):
        """Wrapper of the scikit-learn cross validation function."""
        
        y_correct = train_data.senses
        y_predict = cross_validation.cross_val_predict(
            self.model,
            train_data.data,
            train_data.senses,
            cv=cv)
        """
        result = dict()
        for s in list(scores[0]):
            result[s] = np.average([ score[s] for score in scores ])"""
        return Learner.scoring(y_predict, y_correct)
        
    def train(self, train_data):
        """Train the model using the training set"""
        return self.model.fit(train_data.data, train_data.senses)

    def predict(self, ambiguous_data):
        return self.model.predict(ambiguous_data.data)


class Miner(object):
    """Abstract class for data mining."""

    __metaclass__ = DocStringInheritor

    def __init__(self):
        """Init."""
    pass

    @abstractmethod
    def build(self):
        """Build a corpus."""
        pass

    @abstractmethod
    def get_corpus(self, word):
        """Get the corpus."""
        pass

    def load(self, filename):
        """Load a model from a binary file."""
        with open(filename, 'rb') as f:
            tmp_dict = pickle.load(f)
        if tmp_dict is not None:
            self.__dict__ = tmp_dict

    def export(self, filename):
        """Store a model into a binary file."""
        with open(filename, 'wb') as f:
            pickle.dump(self.__dict__, f)


class FeatureExtractor(object):
    """Abstract class for feature extraction."""

    __metaclass__ = DocStringInheritor

    def __init__(self):
        """Init the feature extractor."""
        pass

    @abstractmethod
    def extract_features(words, targets):
        """Extract feature vectors
        words -- vector of word
        targets -- list of target's indexes
        return -- 2D-vector containing features.
        """

    def load(self, filename):
        """Load a model from a binary file."""
        with open(filename, 'rb') as f:
            tmp_dict = pickle.load(f)
        if tmp_dict is not None:
            self.__dict__ = tmp_dict

    def export(self, filename):
        """Store a model into a binary file."""
        with open(filename, 'wb') as f:
            pickle.dump(self.__dict__, f)
