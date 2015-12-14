class DataMining :
    """Abstract class for data mining"""
    
    def __init__(self) :
        """ Initialize the data-miner. """
        pass
    
    def build(self, param) :
        """ Store the wini-miner into a binary file """
        pass
    
    def export(self, filename) :
        """ Store the wini-miner into a binary file """
        pass
    
    def load(self, filename) :
        """ Load the wini-miner from a binary file """
        pass
    
    def get_corpus(self, word) :
        """
        Get the corpus of the ambiguous word.
        @return : to be defined...
        """
        pass
