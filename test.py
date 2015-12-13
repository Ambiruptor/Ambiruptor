#!/usr/bin/python3

import os.path

from ambiruptor.data_mining.wikipedia import DataMining
from ambiruptor.feature_extraction import FeatureExtraction
from ambiruptor.learning import Learning

data = DataMining()
data.load_wikipedia_file("data/wikidump.xml")
if os.path.isfile("data/wikidump_pos.bin") :
    data.load_wikipedia_fpos("data/wikidump_pos.bin")
else :
    data.build_wikipedia_fpos()
    data.export_wikipedia_fpos("data/wikidump_pos.bin")
print(len(data.wikipedia_fpos), "articles found.")

corpus = data.get_corpus(b'Bar')

#feature = FeatureExtraction()
#feature.build("Bar")

#learning = Learning()
