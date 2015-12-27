
class TrainData:
    def __init__(self, word, senses, x=None, labels=None):
        # TODO: check input data consistency
        self.word = word
        self.senses = senses
        self.X = x
        self.labels = labels


class AmbiguousData:
    def __init__(self, words, targets, data):
        self.words = words
        self.targets = targets
        self.data = data
