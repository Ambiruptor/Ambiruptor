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
    corpus = data.get_corpus("Bar")
    print("Size of the corpus:", len(corpus), "articles")
    print("Done,", time.time() - t, "s")
    
    # Building features
    print("********************** Building features **************************")
    feature1 = fe.DummyFeatureExtractor()
    feature2 = fe.DummyFeatureExtractor()
    t = time.time()
    print("Done,", time.time() - t, "s")
    
    # Feature extraction (corpus)
    print("******************* Feature extraction (corpus) *******************")
    t = time.time()
    corpus_extractor = fe.CorpusExtraction()
    corpus_extractor.add_feature(feature1)
    corpus_extractor.add_feature(feature2)
    train_data = corpus_extractor.extract_features(corpus)
    print(train_data.data.shape)
    print("Done,", time.time() - t, "s")
    
    # Feature extraction (ambiguous text)
    print("************** Feature extraction (ambiguous text) ****************")
    t = time.time()
    ambiguous_extractor = fe.AmbiguousExtraction()
    ambiguous_extractor.add_feature(feature1)
    ambiguous_extractor.add_feature(feature2)
    
    text = """Lorem flower ipsum dolor sit amet, bar food
     consectetur adipiscing elit, sed do thething eiusmod
     tempor incididunt ut labore et dolore magna aliqua. Ut enim
     ad food minim veniam, flower quis nostrud exercitation ullamco
     laboris nisi ut aliquip food ex ea commodo consequat. Duis aute
     irure dolor in food reprehenderit flower in voluptate velit esse
     cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat
     food cupidatat non food proident thething, sunt in culpa qui thething
     officia flower deserunt mollit anim bar id est laborum"""
    
    ambiguous_data = ambiguous_extractor.extract_features(text, "bar")
    print(ambiguous_data.data.shape)
    print("Done,", time.time() - t, "s")
    
    # Learning model
    print("************************* Learning model **************************")
    t = time.time()
    model = LinearSVMClassifier()
    model.train(train_data)
    labels = model.predict(ambiguous_data)
    print(labels)
    print("Done,", time.time() - t, "s")
