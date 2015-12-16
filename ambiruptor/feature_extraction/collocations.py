class FeatureExtraction :
    """Abstract class for feature extraction"""

    def __init__(self, word) :
        """ Initialize the feature extractor. """
        #try :
        #    self.load("data/collocations/"+word+".data")
        #except FileNotFoundError :
        self.build(word)

    def build(self, word) :
        """
        Build the feature extractor with the ambiguous word
        @param(word) : string
        """
        print("Feature extraction : " + word)

        text_corpus='blablabla bar'
        sentences=text_corpus.replace("?", ".").replace("!", ".").split(". ")
        all_collocs=()

        word=word.lower()

        window_size=5
        #fill all_collocs
        for lo in range(-window_size, 0):
            for hi in range(0, window_size+1):
                #compute every collocation from lo to hi
                for sent in sentences:
                    if word in sent:
                        sent=sent.replace("\n", " ").replace(",", "").split(" ")
                        ind=sent.index(word)
                        if ind + lo > -1 and ind+hi < len(sent):
                            print(sent)
                            all_collocs+=(" ".join([x.lower() for x in sent[ind+lo:ind+hi+1]]),)
                            print(lo,hi, " ".join([x.lower() for x in sent[ind+lo:ind+hi+1]]))

        #compute counts
        all_collocs_occ=list(set(all_collocs))
        for indcol in range(0, len(all_collocs_occ)):
            all_collocs_occ[indcol]=[all_collocs_occ[indcol], all_collocs.count(all_collocs_occ[indcol])]

        #sort by decreasing order of count*(hi-lo) to give importance to long collocations
        all_collocs_occ.sort(key=lambda x: -(x[1]*len(x[0])))

        size=10
        #take the first size collocations
        self.usual_collocs=[col[0] for col in all_collocs_occ[:size]]




    def load(self, filename) :
        """Load a feature extractor from a binary file"""
        f = open(filename, "rb")
        self.usual_collocs = pickle.load(f)
        f.close()

    def export(self, filename) :
        """Store the feature extractor into a binary file"""
        f = open(filename, "wb")
        pickle.dump(self.usual_collocs, f)
        f.close()

    def extract(self, window, pos) :
        """
        Extract a features vector.
        @param(window) : string
        @param(pos) : integer (position of the word in the sentence)
        @return : vector of features
        """
        print(self.usual_collocs)
        return([window.count(colloc) for colloc in self.usual_collocs])
