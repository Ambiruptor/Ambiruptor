class FeatureExtraction :
    """Abstract class for feature extraction"""
    
    def __init__(self) :
        """Init the feature extractor"""
        pass
    
    def build(self, word) :
        """
        Build the feature extractor with the ambiguous word
        @param(word) : string
        """
        print("Feature extraction : " + word)
        pass
    
    def load(self) :
        """Load a feature extractor from a binary file"""
        pass
    
    def export(self) :
        """Store a feature extractor into a binary file"""
        pass
    
    def extract(self, window, pos) :
        """
        Extract a features vector.
        @param(window) : string
        @param(pos) : integer (position of the word in the sentence)
        @return : vector of features
        """
        pass
