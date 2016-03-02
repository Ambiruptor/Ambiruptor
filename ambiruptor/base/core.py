"""Core base classes"""

from abc import ABCMeta, abstractmethod
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

    def __init__(self):
        """Init the learning model."""
        pass

    @abstractmethod
    def train(self, train_data):
        """Train the model using the training set train_data -- instance of TrainData.
        """
        pass

    def fit(self, train_data):
        """Provide the interface for scikit-learn utils
        simply calling the train method.
        """
        return self.tain(train_data)

    def score(self, ambiguous_data):
        """Provide the scoring interface for scikit-learn utils."""
        return self.model.score(ambiguous_data.data, ambiguous_data.targets)

    def get_params(self, deep=True):
        """Provide the get_params interface for scikit-learn utils."""
        return self.model.get_params(deep)

    @abstractmethod
    def predict(self, data):
        """Guess the best sense for a features vector data -- instance of
        AmbiguousData.
        """
        pass

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
        print(self.__dict__)
        with open(filename, 'wb') as f:
            pickle.dump(self.__dict__, f)
