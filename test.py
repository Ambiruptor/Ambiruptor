#!/usr/bin/python3

from ambiruptor.data_mining import DataMining
from ambiruptor.feature_extraction import FeatureExtraction
from ambiruptor.learning import Learning

data = DataMining()
data.build("Bar")

feature = FeatureExtraction()
feature.build("Bar")

learning = Learning()
