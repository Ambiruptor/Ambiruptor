import time, pickle, os.path
import ambiruptor.library.preprocessors.feature_extractors as fe

t = time.time()
print("============== Building list of ambiguous words ===================")
filename_ambiguouswords = "data/ambiguous_words.txt"
with open(filename_ambiguouswords, 'r') as f:
    ambiguous_words = { x.rstrip() for x in f.readlines() }
    if "" in ambiguous_words :
        ambiguous_words.remove("")

nb_ambiguous_words = len(ambiguous_words)
print("Done,", time.time() - t, "s")

t = time.time()
print("======================== Build features ============================")
for n, w in enumerate(ambiguous_words):
    t2 = time.time()
    print("%s (%d/%d)" % (w, n, nb_ambiguous_words))
    filename_corpus = "data/corpora/" + w + ".dump"
    filename_features = "data/feature_extractors/" + w + ".dump"
    if not os.path.isfile(filename_corpus):
        print("No corpus file.")
        continue
    if os.path.isfile(filename_features):
        print("Already done.")
        continue
    with open(filename_corpus, 'rb') as f:
        corpus = pickle.load(f)
    feature = fe.CloseWordsFeatureExtractor()
    feature.build_typicalwords(corpus)
    feature.export(filename_features)
    print("ok (%f s)" % (time.time() - t2))
print("Done,", time.time() - t, "s")
