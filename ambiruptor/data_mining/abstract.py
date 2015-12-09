class DataMining :
    """Abstract class for data mining"""
    
    def __init__(self) :
        """Init the learning model"""
        pass
    
    def build(self, word) :
        """
        Build a corpus for the ambiguous word
        @param(word) : string
        """
        print("Data mining : " + word)
        pass
    
    def get_corpus(self) :
        """
        Get the corpus
        @return : to be defined...
        """
        pass
