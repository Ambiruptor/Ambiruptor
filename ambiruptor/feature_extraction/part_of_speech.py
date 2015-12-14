import nltk

class FeatureExtraction :
    """ Part of speech feature extractor """
    
    def __init__(self) :
        """ Initialize the feature extractor. """
        pass
    
    def build(self, word) :
        """
        Build the feature extractor with the ambiguous word
        @param(word) : string
        """
        pass
    
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
        size = 5
        vector = [x[1] for x in nltk.pos_tag(nltk.word_tokenize(window))]
        return [None] * max(0, size-pos) + vector[max(0, pos-size):pos+size+1] + [None] * max(0, size+pos+1-len(vector))
