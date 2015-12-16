""" Core base classes """

from abc import ABCMeta, abstractmethod


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
    """Abstract class for learning"""

    __metaclass__ = DocStringInheritor

    def __init__(self):
        """Init the learning model"""
        pass

    @abstractmethod
    def train(self, train_data):
        """Train the model using the training set"""
        pass

    @abstractmethod
    def predict(self, data):
        """
        Guess the best sense for a features vector
        @param(vector) : features vector
        @return : word sense
        """
        pass

    @abstractmethod
    def load(self, filename):
        """Load a model from a binary file"""
        pass

    @abstractmethod
    def export(self, filename):
        """Store a model into a binary file"""
        pass


class Miner(object):
    """Abstract class for data mining"""

    __metaclass__ = DocStringInheritor

    def __init__(self):
        """Init"""
        pass

    @abstractmethod
    def build(self, word):
        """
        Build a corpus for the ambiguous word
        @param(word) : string
        """
        print("Data mining : " + word)
        pass

    @abstractmethod
    def get_corpus(self):
        """
        Get the corpus
        @return : to be defined...
        """
        pass


class FeatureExtractor(object):
    """Abstract class for feature extraction"""

    def __init__(self):
        """Init the feature extractor"""
        pass

    @abstractmethod
    def build(self, word):
        """
        Build the feature extractor with the ambiguous word
        @param(word) : string
        """
        pass

    @abstractmethod
    def load(self):
        """Load a feature extractor from a binary file"""
        pass

    @abstractmethod
    def export(self):
        """Store a feature extractor into a binary file"""
        pass

    @abstractmethod
    def extract(self, window, pos):
        """
        Extract a features vector.
        @param(window) : string
        @param(pos) : integer (position of the word in the sentence)
        @return : vector of features
        """
        pass
