from nltk.stem.porter import *
from nltk.corpus import stopwords
import pickle


class FeatureExtraction :
    """Abstract class for feature extraction"""
    
        
    def __init__(self, word) :
        """ Initialize the feature extractor. """
        try :
            self.load("data/close_words/"+word+".data")
        except FileNotFoundError :
            self.build(word)
    
        
    
    
    def build(self, word) :
        """
        Build the feature extractor with the ambiguous word
        @param(word) : string
        """
        print("Feature extraction : " + word)
        
        word=word.lower()

        corpus_text='I am a happy corpus of bar text that contains a lot of different occurences of the word word! Hopefully these occurences use the word in all different meanings. I hope I did not bore you with this little paragraph!'
     
        stemmer = PorterStemmer()
        
        sentences=corpus_text.replace("!", ".").replace("?", ".").split('. ')
        words_same_sentence=()        
        #fill the list of words
        for sent in sentences :
            if(word in sent):
                sent=sent.replace("\n", " ").replace(", ", " ").replace('=', '').split(" ")
                for other_word in sent :
                    if(not(other_word.lower() in stopwords.words("english")) and not (other_word=='')):
                        words_same_sentence += (stemmer.stem(other_word.lower()), )
        #count the occurence of each other word that appear in the same sentence
        words_same_sentence_occ=list(set(words_same_sentence)-set([word]))
        for w in range(len(words_same_sentence_occ)):
            words_same_sentence_occ[w]=[words_same_sentence_occ[w], words_same_sentence.count(words_same_sentence_occ[w])]
            
        #sort by decreasing order of count
        words_same_sentence_occ.sort(key=lambda x: -x[1])
        
        #take the first size words
        size=15
        self.usual_words=[x[0] for x in words_same_sentence_occ][:size]
       # self.export("data/close_words/"+word+".data")
        
    
    def load(self, filename) :
        """Load a feature extractor from a binary file"""
        f = open(filename, "rb")
        self.usual_words = pickle.load(f)
        f.close()
    
    def export(self, filename) :
        """Store the feature extractor into a binary file"""
        f = open(filename, "wb")
        pickle.dump(self.usual_words, f)
        f.close()
        
        
    
    def extract(self, window, pos) :
        """
        Extract a features vector.
        @param(window) : string
        @param(pos) : integer (position of the word in the sentence)
        @return : vector of features
        """

        if(not(self.usual_words==None)):
            vector=[window.lower().count(other_word) for other_word in self.usual_words]
            return vector
