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
for n,w in enumerate(ambiguous_words):
    t2 = time.time()
    print("%s (%d/%d)" % (w, n, nb_ambiguous_words))
    
    filename_corpus = "data/corpora/" + w + ".dump"
    filename_fe_ambig = "data/feature_extractors/" + w + ".dump"
    filename_fe_corpus = "data/feature_extractors/" + w + ".corpus.dump"
    
    if os.path.isfile(filename_fe_ambig) and os.path.isfile(filename_fe_corpus):
        print("Already done.")
        continue
    
    if not os.path.isfile(filename_corpus):
        print("No corpus file.")
        continue
    with open(filename_corpus, 'rb') as f:
        corpus = pickle.load(f)
    
    feature = fe.CloseWordsFeatureExtractor()
    feature.build_typicalwords(corpus)
    
    fe_ambig = fe.AmbiguousExtraction()
    fe_ambig.add_feature(feature)
    with open(filename_fe_ambig, 'wb') as f:
        pickle.dump(fe_ambig, f)
    
    fe_corpus = fe.CorpusExtraction()
    fe_corpus.add_feature(feature)
    with open(filename_fe_corpus, 'wb') as f:
        pickle.dump(fe_corpus, f)
    
    print("ok (%f s)" % (time.time() - t2))
print("Done,", time.time() - t, "s")
