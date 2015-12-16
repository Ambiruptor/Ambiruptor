
class TrainData:
    def __init__(self, word, senses, x=None, labels=None):
        # TODO: check input data consistency
        self.word = word
        self.senses = senses
        self.X = x
        self.labels = labels


class AmbiguousData:
    def __init__(self, raw_text, targets, data):
        self.raw_text = raw_text
        self.targets = targets
        self.data = data
