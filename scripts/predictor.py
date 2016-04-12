import json
import re
import pickle
import os.path

import numpy as np
import ambiruptor.library.preprocessors.feature_extractors as fe

from ambiruptor.library.preprocessors.tokenizers import word_tokenize
    
def predictor(datadir, text):    
    # List of ambiguous words
    filename_ambiguouswords = datadir + "/ambiguous_words.txt"
    with open(filename_ambiguouswords, 'r') as f:
        ambiguous_words = {x.rstrip() for x in f.readlines()}
        if "" in ambiguous_words:
            ambiguous_words.remove("")

    # Word tokenize
    results = []
    words = np.array(word_tokenize(text.lower()))

    # Disambiguation
    for w in ambiguous_words:
        # Ambiguous word
        ambiguous_word = re.match(r"[^_]+", w).group(0).lower()
        # Feature extraction
        filename_features = datadir + "/feature_extractors/" + w + ".dump"
        if not os.path.isfile(filename_features):
            continue
        feature = fe.CloseWordsFeatureExtractor()
        feature.load(filename_features)
        
        ambiguous_extractor = fe.AmbiguousExtraction()
        ambiguous_extractor.add_feature(feature)
        ambiguous_data = ambiguous_extractor.extract_features(words, ambiguous_word)
        
        if ambiguous_data.data.shape[0] == 0:
            continue
        # Model prediction
        filename_models = datadir + "/models/" + w + ".dump"
        if not os.path.isfile(filename_models):
            #print("No models file for word '%s'." % w)
            continue
        with open(filename_models, "rb") as f:
            model = pickle.load(f)
            predictions = model.predict(ambiguous_data)
            #print(predictions)
            for index, meaning in zip(ambiguous_data.targets, predictions):
                result = dict()
                result["begin"] = sum([len(words[i]) for i in range(index)])
                result["end"] = result["begin"] + len(words[index])
                result["all_senses"] = model.model.classes_.tolist()
                result["meaning"] = result["all_senses"].index(meaning)
                result["url"] = "https://en.wikipedia.org/wiki/%s" % meaning
                results.append(result)

    # Return results
    return results

if __name__ == '__main__':
    print(predictor("data/", "Today I eat a bar. It was delicious !"))
