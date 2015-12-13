#!/usr/bin/python3

import os.path, re

from ambiruptor.data_mining.wikipedia import DataMining
from ambiruptor.feature_extraction import FeatureExtraction
from ambiruptor.learning import Learning

data = DataMining()
if not os.path.isfile("data/wikilinks.bin") :
    data.build("data/wikidump.xml")
    data.export("data/wikilinks.bin")
else :
    data.load("data/wikilinks.bin")
print(data.get_corpus("Bar"))

#feature = FeatureExtraction()
#feature.build("Bar")

#learning = Learning()
