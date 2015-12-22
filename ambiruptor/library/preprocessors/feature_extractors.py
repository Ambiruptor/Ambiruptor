import random
import numpy as np
from nltk import word_tokenize

from ambiruptor.base.core import FeatureExtractor
from ambiruptor.library.preprocessors.data_structures import AmbiguousData


class DummyFeatureExtractor(FeatureExtractor):
    """
    Static attribute that for every
    implementation of feature extractor will
    contain list with the name of features
    """
    feature_names = ["feature1",
                     "feature2",
                     "feature3",
                     "feature4"]

    def __init__(self):
        self.targets = list()

    # these functions are totally dummy-functions for test
    def get_feature1(self):
        return random.uniform(1.0, 5.0)

    def get_feature2(self):
        return random.uniform(1.0, 5.0)

    def get_feature3(self):
        return random.uniform(1.0, 5.0)

    def get_feature4(self):
        return random.uniform(1.0, 5.0)

    def extract_targets(self, text, senses):
        """
        Takes plain text and
        dict of ambiguous words to look for
        as arguments
        """
        words = word_tokenize(text)
        for i, w in enumerate(words):
            if w in senses.keys():
                self.targets.append((i, w))

    def extract_features(self, text, senses):
        """
        """
        # We extract targets words for disambiguation
        self.extract_targets(text, senses)
        # We extract features for the target words
        targets = self.targets
        data = np.zeros((len(self.targets), len(self.feature_names)))
        # here we prepopulate features with dummy data
        for t, target in enumerate(self.targets):
            for i, name in enumerate(DummyFeatureExtractor.feature_names):
                data[t, i] = getattr(self, "get_%s" % (name))()
        return AmbiguousData(text, targets, data)


class CloseWordsFeatureExtractor(FeatureExtractor):
    '''
    Extracts a vector for the count
    of usual words in the text
    '''

    size=15
    '''size of the feature vector we build'''

    def __init__(self, word):
    """ Initialize the feature extractor. """
        self.targets=list()


    def build_typicalwords(self, word) :
        """
        Build the feature extractor with the ambiguous word
        @param(word) : string
        """
        word=word.lower()

        corpus_text='I am a happy corpus of bar text that contains a lot of different occurences of the word word! Hopefully these occurences use the word in all different meanings. I hope I did not bore you with this little paragraph!'

        stemmer = PorterStemmer()

        sentences=corpus_text.replace("!", ".").replace("?", ".").split('. ')
        words_same_sentence=[]
        #fill the list of words
        for sent in sentences :
            sent=sent.replace(", ", " ").replace('=', '').split()
            if word in sent :
                for other_word in sent :
                    if other_word.lower() not in stopwords.words("english") and other_word!='' :
                        words_same_sentence.append(stemmer.stem(other_word.lower()))
        #count the occurence of each other word that appear in the same sentence
        words_same_sentence_occ=[]
        for w in set(words_same_sentence)-{word} :
            words_same_sentence_occ.append((w, words_same_sentence.count(w)))

        #sort by decreasing order of count
        words_same_sentence_occ.sort(key=lambda x: -x[1])

        #export the first size words
        f=open(".../corpus/close_words/"+target+".data", "wb")
        pickle.dump([x[0] for x in words_same_sentence_occ], f)
        f.close

    def extract_features(self, text, senses):
        self.extract_targets(text, senses)
        data=np.zeroes((len(self.targets), size))
        for t, target in enumerate(self.targets):
            #load the list of usual words
            try :
                f=open(".../corpus/close_words/"+target+".data", "rb")
            except FileNotFoundError :
                self.build_typicalwords(target, size)
                f=open(".../corpus/close_words/"+target+".data", "rb")
            usual_words_for_target=pickle.load(f)
            f.close()

            sep=[stemmer.stem(w.lower()) for w in word_tokenize(text)]
            data[t]=[sep.count(typical_word) for typical_word in typical_words[:size]]

        return AmbiguousData(text, targets, data)


class CollocationsFeatureExtractor(FeatureExtractor):
    '''
    Extracts a vector for the count
    of collocations in the text
    '''

    size=15
    '''size of the feature vector we build'''

    def __init__(self, word):
    """ Initialize the feature extractor. """
        self.targets=list()

    def build_collocations(self, word):
    ''' Builds a list of frequent collocations'''
        text_corpus='blablabla bar'
        sentences=text_corpus.replace("?", ".").replace("!", ".").split(". ")
        all_collocs=[]

        word=word.lower()

        window_size=5
        #fill all_collocs
        for lo in range(-window_size, 0):
            for hi in range(0, window_size+1):
                #compute every collocation from lo to hi
                for sent in sentences:
                    sent=word_tokenize(sent)
                    if word in sent:
                        ind=sent.index(word)
                        if ind + lo > -1 and ind+hi < len(sent):
                            all_collocs.append(" ".join([x.lower() for x in sent[ind+lo:ind+hi+1]]))

        #compute counts
        all_collocs_occ=[]
        for col in set(all_collocs):
            all_collocs_occ.append((col, all_collocs.count(col)))

        #sort by decreasing order of count*(hi-lo) to give importance to long collocations
        all_collocs_occ.sort(key=lambda x: -(x[1]*len(x[0])))

        #export the first size collocations
        f=open('.../corpus/collocations/'+word+'.data', 'wb')
        pickle.dump([col[0] for col in all_collocs_occ])
        f.close()

    def extract_feature(self, text, senses):
        self.extract_targets(text, senses)
        data=np.zeroes((len(self.targets), size))
        for t, target in enumerate(self.targets):
            #load the list of collocations
            try :
                f=open(".../corpus/collocations/"+target+".data", "rb")
            except FileNotFoundError :
                self.build_typicalwords(target, size)
                f=open(".../corpus/collocations/"+target+".data", "rb")
            collocations_for_target=pickle.load(f)
            f.close()

            data[t]=[text.count(col) for col in collocations_for_target[:size]]

        return AmbiguousData(text, targets, data)
