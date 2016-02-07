import numpy as np
import os.path
import re
import time

from ambiruptor.library.preprocessors.data_structures import TrainData
from ambiruptor.library.learners.models import LinearSVMClassifier
from ambiruptor.library.miners.wiki_miners import DataMining

import ambiruptor.library.preprocessors.feature_extractors as fe

if __name__ == '__main__':

    # Data Mining
    print("************************** Data mining ****************************")
    t = time.time()
    data = DataMining()
    data.set_wikidump_filename("data/wikidump.xml")
    data.set_database_filename("data/wikidump.db")
    data.build()
    corpus = data.get_corpus("Bar_(disambiguation)")
    print("Size of the corpus:", len(corpus), "articles")
    print("Done,", time.time() - t, "s")
    
    # Building features
    print("********************** Building features **************************")
    t = time.time()
    feature1 = fe.PartOfSpeechFeatureExtractor()
    feature2 = fe.CloseWordsFeatureExtractor()
    feature2.build_typicalwords(corpus)
    print("Done,", time.time() - t, "s")
    
    # Feature extraction (corpus)
    print("******************* Feature extraction (corpus) *******************")
    t = time.time()
    corpus_extractor = fe.CorpusExtraction()
    corpus_extractor.add_feature(feature2)
    train_data = corpus_extractor.extract_features(corpus)
    print("Shape of the matrix of features:", train_data.data.shape)
    print("Done,", time.time() - t, "s")
    
    # Feature extraction (ambiguous text)
    print("************** Feature extraction (ambiguous text) ****************")
    t = time.time()
    ambiguous_extractor = fe.AmbiguousExtraction()
    ambiguous_extractor.add_feature(feature2)
    
    text = """The bar of a mature tropical cyclone is a very dark gray-black
              layer of cloud appearing near the horizon as seen from an observer
              preceding the approach of the storm, and is composed of dense
              stratocumulus clouds. Cumulus and cumulonimbus clouds bearing
              precipitation follow immediately after the passage of the
              wall-like bar. Altostratus, cirrostratus and cirrus clouds are
              usually visible in ascending order above the top of the bar, while
              the wind direction for an observer facing toward the bar is
              typically from the left and slightly behind the observer."""
    
    ambiguous_data = ambiguous_extractor.extract_features(text, "bar")
    print("Shape of the matrix of features:", ambiguous_data.data.shape)
    print("Done,", time.time() - t, "s")
    
    # Learning model
    print("************************* Learning model **************************")
    t = time.time()
    model = LinearSVMClassifier()
    model.train(train_data)
    labels = model.predict(ambiguous_data)
    print(labels)
    print("Done,", time.time() - t, "s")
