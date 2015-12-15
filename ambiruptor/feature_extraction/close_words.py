from nltk.stem.porter import *
from nltk.corpus import stopwords

class FeatureExtraction :
    """Abstract class for feature extraction"""
    
    self
    
    def __init__(self) :
        """ Initialize the feature extractor. """
        self.corpus_text=	"I am a happy corpus of text that contains a lot of different occurences of the word!
        					hopefully these occurences use the word in all different meanings. I hope I did not
        					bore you with this little paragraph!"
        pass
    
    def build(self, word) :
        """
        Build the feature extractor with the ambiguous word
        @param(word) : string
        """
        print("Feature extraction : " + word)
        __init__(self)
 
		stemmer = PorterStemmer()
		if(not(self.corpus_text==None)):
			sentences=self.text.replace("!", ".").replace("?", ".").split('. ')
	      	words_same_sentence=()		    
		    #fill the list of words
		    for sent in sentences :
		    	if(word in sent):
		    		sent=sent.replace("\n", " ").replace(", ", " ").replace('=', '').split(" ")
		    		for(other_word in sent):
		    			if(not(other_word.lower() in stopwords.words("english") and not (other_word=='')):
		    				words_same_sentence += (stemmer.stem(other_word.lower()), )
		    
		    #count the occurence of each other word that appear in the same sentence
		    words_same_sentence_occ=list(set(words_same_sentence)-set([word]))
		    for w in range(len(words_same_sentence_occ)):
		    	words_same_sentence_occ[w]=[words_same_sentence_occ[w], words_same_sentence.count(words_same_sentence_occ[w])]
		    
		    #sort by decreasing order of count
		    self.words_same_sentence_occ.sort(key=lambda x: -x[1])
        
        
        
        
    
    def load(self, filename) :
        """Load a feature extractor from a binary file"""
        pass
    
    def export(self, filename) :
        """Store the feature extractor into a binary file"""
        pass
    
    def extract(self, window, pos) :
        """
        Extract a features vector.
        @param(window) : string
        @param(pos) : integer (position of the word in the sentence)
        @return : vector of features
        """

        if(not(self.words_same_sentence_occ==None)):
        	size=15
        	vector=[window.lower().count(other_word[0]) for other_word in self.words_same_sentence_occ[:size]]
        	return vector
