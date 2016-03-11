import sys, time, pickle
from ambiruptor.library.miners.wiki_miners import DataMining

t = time.time()
print("======================== Build database ===========================")
data = DataMining()
data.set_wikidump_filename("data/wikidump.xml")
data.set_database_filename("data/wikidump.db")
data.build()
print("Done,", time.time() - t, "s")

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
print("======================== Build corpora ============================")
for n,w in enumerate(ambiguous_words):
    t2 = time.time()
    print("%s (%d/%d)" % (w, n, nb_ambiguous_words))
    corpus = data.get_corpus(w)
    filename = "data/corpora/" + w + ".dump"
    with open(filename, 'wb') as f:
        pickle.dump(corpus, f)
    print("ok (%f s)" % (time.time() - t2))
print("Done,", time.time() - t, "s")

