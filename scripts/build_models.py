import time, os.path, pickle

from ambiruptor.library.preprocessors.data_structures import TrainData
import ambiruptor.library.preprocessors.feature_extractors as fe

from ambiruptor.library.learners.models import LinearSVMClassifier
from ambiruptor.library.learners.models import RbfSVMClassifier
from ambiruptor.library.learners.models import NaiveBayesClassifier
from ambiruptor.library.learners.models import DecisionTreeClassifier
from ambiruptor.library.learners.models import RandomForestClassifier
from ambiruptor.library.learners.models import KNeighborsClassifier

t = time.time()
print("============== Building list of ambiguous words ===================")
filename_ambiguouswords = "data/ambiguous_words.txt"
with open(filename_ambiguouswords, 'r') as f:
    ambiguous_words = { x.rstrip() for x in f.readlines() }
    if "" in ambiguous_words :
        ambiguous_words.remove("")

nb_ambiguous_words = len(ambiguous_words)
print("Done,", time.time() - t, "s")


print("======================== Build models =============================")

models = [ ("KNeighbors", KNeighborsClassifier),
           ("Naive Bayes", NaiveBayesClassifier),
           ("Decision Tree", DecisionTreeClassifier),
           ("Linear SVM", LinearSVMClassifier),
           ("Rdf SVM", RbfSVMClassifier), ]

for n,w in enumerate(ambiguous_words):
    t2 = time.time()
    print("%s (%d/%d)" % (w, n, nb_ambiguous_words))
    
    filename_corpus = "data/corpora/" + w + ".dump"
    filename_features = "data/feature_extractors/" + w + ".corpus.dump"
    filename_models = "data/models/" + w + ".dump"
    if not os.path.isfile(filename_corpus):
        print("No corpus file.")
        continue
    if not os.path.isfile(filename_features):
        print("No features file.")
        continue
    if os.path.isfile(filename_models):
        print("Already done.")
        #continue
    
    with open(filename_features, 'rb') as f:
        corpus_extractor = pickle.load(f)
    
    with open(filename_corpus, 'rb') as f:
        corpus = pickle.load(f)
    
    train_data = corpus_extractor.extract_features(corpus)
    
    # Temporary : Sanitize the corpus (if less than 10 links, forget)
    senses = dict()
    for x in train_data.senses:
        if x not in senses:
            senses[x] = 0
        senses[x] = senses[x] + 1
    #print(senses)
    
    import numpy as np
    X = []
    Y = []
    for x,y in zip(train_data.data, train_data.senses):
        if senses[y] >= 10:
            X.append(x)
            Y.append(y)
    X = np.asarray(X)
    train_data = TrainData(X, Y)
    #print(X.shape)
    # End of sanitize
    
    
    # Export model
    model = DecisionTreeClassifier()
    model.fit(train_data)
    with open(filename_models, 'wb') as f:
        pickle.dump(model, f)
    
    for name, model in models:
        t2 = time.time()
        print("------------ %s -------------" % name)
        m = model()
        m.fit(train_data)
        scores = m.scores(train_data)
        print(scores)
        print("ok (%f s)" % (time.time() - t2))
