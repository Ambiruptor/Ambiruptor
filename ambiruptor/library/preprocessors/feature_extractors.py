import random
import numpy as np
from nltk import word_tokenize

from ambiruptor.base.core import FeatureExtractor
from ambiruptor.library.preprocessors.data_structures import AmbiguousData


class DummyFeatureExtractor(FeatureExtractor):
    """
    Static attribute that for every
    implementation of feature extractor will
    contain list with the name of features
    """
    feature_names = ["feature1",
                     "feature2",
                     "feature3",
                     "feature4"]

    def __init__(self):
        self.targets = list()

    # these functions are totally dummy-functions for test
    def get_feature1(self):
        return random.uniform(1.0, 5.0)

    def get_feature2(self):
        return random.uniform(1.0, 5.0)

    def get_feature3(self):
        return random.uniform(1.0, 5.0)

    def get_feature4(self):
        return random.uniform(1.0, 5.0)

    def extract_targets(self, text, senses):
        """
        Takes plain text and
        dict of ambiguous words to look for
        as arguments
        """
        words = word_tokenize(text)
        for i, w in enumerate(words):
            if w in senses.keys():
                self.targets.append((i, w))

    def extract_features(self, text, senses):
        """
        """
        # We extract targets words for disambiguation
        self.extract_targets(text, senses)
        # We extract features for the target words
        targets = self.targets
        data = np.zeros((len(self.targets), len(self.feature_names)))
        # here we prepopulate features with dummy data
        for t, target in enumerate(self.targets):
            for i, name in enumerate(DummyFeatureExtractor.feature_names):
                data[t, i] = getattr(self, "get_%s" % (name))()
        return AmbiguousData(text, targets, data)
