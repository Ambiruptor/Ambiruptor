import numpy as np

class TrainData:
    def __init__(self, data, senses):
        assert isinstance(data, np.ndarray)
        assert isinstance(senses, list)
        assert data.shape[0] == len(senses)
        assert len(data.shape) == 2
        self.data = data
        self.senses = senses


class AmbiguousData:
    def __init__(self, data, words, targets):
        assert isinstance(data, np.ndarray)
        assert isinstance(words, np.ndarray)
        assert isinstance(targets, list)
        assert data.shape[0] == len(targets)
        assert len(words.shape) == 1
        assert len(data.shape) == 2
        self.data = data
        self.words = words
        self.targets = targets
