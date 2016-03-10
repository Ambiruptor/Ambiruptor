import sys

if len(sys.argv) != 2:
    print('Usage: %s "wikipedia page"' % sys.argv[0])
    sys.exit(1)

filename_corpus = "data/corpora/" + sys.argv[1] + ".dump"
filename_feature = "data/feature_extractors/" + sys.argv[1] + ".dump"

import pickle

with open(filename_corpus, 'rb') as f:
    corpus = pickle.load(f)
    
import ambiruptor.library.preprocessors.feature_extractors as fe

feature = fe.CloseWordsFeatureExtractor()
feature.build_typicalwords(corpus)
feature.export(filename_feature)
