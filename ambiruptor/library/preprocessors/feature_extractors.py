import random
import numpy as np
import os.path
import re
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

from ambiruptor.base.core import FeatureExtractor
from ambiruptor.library.preprocessors.tokenizers import word_tokenize
from ambiruptor.library.preprocessors.data_structures \
    import AmbiguousData, TrainData
from nltk.stem import WordNetLemmatizer


class AmbiguousExtraction(object):

    def __init__(self):
        """Init the feature extractor"""
        self.features = []

    def add_feature(self, f):
        """Add one feature"""
        if not isinstance(f, FeatureExtractor):
            raise TypeError("An instance of FeatureExtractor was expected")
        self.features.append(f)

    def extract_features(self, words, ambiguous_word):
        """Extract a feature vector"""

        # words is an array of words...
        assert isinstance(words, np.ndarray)
        lemmatizer = WordNetLemmatizer()
        ambiguous_word = lemmatizer.lemmatize(ambiguous_word)

        # Extract targets
        targets = []
        for i in range(0, len(words)):
            if lemmatizer.lemmatize(words[i]) == ambiguous_word:
                targets.append(i)
        # Extract features
        tmp_data = []
        for f in self.features:
            tmp = f.extract_features(words, targets)
            assert isinstance(tmp, np.ndarray)
            assert tmp.shape[0] == len(targets)
            tmp_data.append(tmp)
        data = np.concatenate(tmp_data, axis=1)

        # Return an AmbiguousData object
        return AmbiguousData(data, words, targets)

class CorpusExtraction(object):

    def __init__(self):
        """Init the feature extractor"""
        self.features = []

    def add_feature(self, f):
        """Add one feature"""
        if not isinstance(f, FeatureExtractor):
            raise TypeError("An instance of FeatureExtractor was expected")
        self.features.append(f)

    def extract_features(self, corpora):
        """Extract a feature vector"""
        senses = []
        res_data = []

        for n, corpus in enumerate(corpora):
            print("\r(", n, "/", len(corpora), ")", end="", flush=True)
            # Corpus is already tokenized (using word_tokenize)
            words = []
            targets = []
            for i, x in enumerate(corpus):
                if type(x) is tuple:
                    targets.append(i)
                    senses.append(x[1])
                    words.append(x[0])
                else:
                    words.append(x)
            words = np.array(words)

            # Extract features
            tmp_data = []
            for f in self.features:
                tmp = f.extract_features(words, targets)
                assert isinstance(tmp, np.ndarray)
                assert tmp.shape[0] == len(targets)
                tmp_data.append(tmp)
            res_data.append(np.concatenate(tmp_data, axis=1))
        print("\r" + 20 * " " + "\r", end="", flush=True)

        # Return an TrainData object
        return TrainData(np.concatenate(res_data, axis=0), senses)


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

    # these functions are totally dummy-functions for test
    def get_feature1(self):
        return random.uniform(1.0, 5.0)

    def get_feature2(self):
        return random.uniform(1.0, 5.0)

    def get_feature3(self):
        return random.uniform(1.0, 5.0)

    def get_feature4(self):
        return random.uniform(1.0, 5.0)

    def extract_features(self, words, targets):
        data = np.zeros((len(targets), len(self.feature_names)))
        for t, target in enumerate(targets):
            for i, name in enumerate(DummyFeatureExtractor.feature_names):
                data[t,i] = getattr(self, "get_%s" % (name))()
        return data

class PartOfSpeechFeatureExtractor(FeatureExtractor):
    """Extract the part of speech of the words in a window around the target"""

    def __init__(self):
        self.window_size = 10

    def set_window_size(self, s):
        self.window_size = s

    # List of possible values for the function pos_tag
    pos_list = ['CC', 'CD', 'DT', 'EX', 'FW', 'IN', 'JJ', 'JJR', 'JJS',
                'LS', 'MD', 'NN', 'NNP', 'NNPS', 'PDT', 'POS', 'PRP', 'PRP$',
                'RB', 'RBR', 'RBS', 'RP', 'SYM', 'TO', 'UH', 'VB', 'VBD',
                'VBG', 'VBN', 'VBZ', 'WDT', 'WP', 'WP$', 'WRB']
    pos_to_int = dict(zip(pos_list, range(0, len(pos_list))))

    def extract_features(self, words, targets):
        data = np.zeros((len(targets), 2 * self.window_size + 1))
        for t, target in enumerate(targets):
            window_begin = max(0, target - self.window_size)
            window_end = target + self.window_size + 1
            pos = np.array(pos_tag([" " if len(w) == 0 else w for w in words[window_begin:window_end]]))
            for i in range(0, 2 * self.window_size + 1):
                j = i + target - self.window_size
                if j < 0 or j >= len(words):
                    data[t, i] = -1
                else:
                    k = i - max(0, self.window_size - target)
                    if pos[k][1] in self.pos_to_int:
                        data[t, i] = self.pos_to_int[pos[k][1]]
                    else:
                        data[t, i] = 0
        return data

class CloseWordsFeatureExtractor(FeatureExtractor):
    '''
    Extracts a vector for the count
    of usual words in the text
    '''

    def __init__(self):
        """ Initialize the feature extractor."""
        self.lang = "english"
        self.typicalwords = None
        self.stemmer = PorterStemmer()
        self.set_language("english")

    def normalize_word(self, s):
        return self.stemmer.stem(s.lower())

    def set_language(self, lang):
        self.lang = lang
        self.is_word = re.compile(r"\w+", re.UNICODE)
        self.forbidden = set(stopwords.words(lang))
        self.forbidden.add("")
    
    def is_forbidden(self, s):
        if self.is_word.fullmatch(s) is None:
            return True
        if self.normalize_word(s) in self.forbidden:
            return True
        return False 

    def get_score_function(self):
        return lambda i, j: 1. if abs(i - j) < 50 else 0.

    def build_typicalwords(self, corpora):
        """
        Build the feature extractor with the ambiguous word
        @param(word) : string
        """
        get_score = self.get_score_function()
        dictwords = dict()
        for corpus in corpora:
            for i, x in enumerate(corpus):
                if type(x) is tuple:
                    if x[1] not in dictwords:
                        dictwords[x[1]] = dict()
                    for j, y in enumerate(corpus):
                        if type(y) is not tuple:
                            word = self.normalize_word(y)
                            score = get_score(i, j)
                            if word not in dictwords[x[1]]:
                                dictwords[x[1]][word] = 0
                            dictwords[x[1]][word] += score
        typicalwords = set()
        for sense in dictwords:
            words = [x for x in dictwords[sense] if not self.is_forbidden(x)]
            scores = [dictwords[sense][x] for x in words ]
            bestwords = [x[1] for x in sorted(zip(scores, words))[-20:]]
            typicalwords.update(bestwords)
        self.typicalwords = dict(zip(typicalwords, range(len(typicalwords))))

    def print_typicalwords(self):
        print(self.typicalwords)

    def extract_features(self, words, targets):
        # Check whether typical words have been build/load.
        if self.typicalwords is None:
            raise Exception("You must call build_typicalwords")

        get_score = self.get_score_function()

        data = np.zeros((len(targets), len(self.typicalwords)))
        for t, target in enumerate(targets):
            scores = dict(zip(self.typicalwords, [0.] * len(self.typicalwords)))
            for i, w in enumerate(words):
                normalized_word = self.normalize_word(w)
                if normalized_word in self.typicalwords:
                    scores[normalized_word] += get_score(target, i)
            for w in self.typicalwords:
                data[t, self.typicalwords[w]] = scores[w]

        return data

"""
class CollocationsFeatureExtractor(FeatureExtractor):
    '''
    Extracts a vector for the count
    of collocations in the text
    '''

    # TODO: Rewrite this module according to the new design

    size=15
    '''size of the feature vector we build'''

    def __init__(self, word):
        ''' Initialize the feature extractor. '''
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
        f=open('.../corpus/collocations/'+word+'.data', 'wb') # TODO
        pickle.dump([col[0] for col in all_collocs_occ])
        f.close()

    def extract_feature(self, text, senses):
        self.extract_targets(text, senses)
        data=np.zeroes((len(self.targets), size))
        for t, target in enumerate(self.targets):
            #load the list of collocations
            try :
                f=open(".../corpus/collocations/"+target+".data", "rb") # TODO
            except FileNotFoundError :
                self.build_typicalwords(target, size)
                f=open(".../corpus/collocations/"+target+".data", "rb") # TODO
            collocations_for_target=pickle.load(f)
            f.close()

            data[t]=[text.count(col) for col in collocations_for_target[:size]]

        data
"""
