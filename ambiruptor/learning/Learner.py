class Learner:
    """Abstract class for learning"""

    def __init__(self):
        """Init the learning model"""
        print("Learning")
        pass

    def load(self):
        """Load a model from a binary file"""
        pass

    def export(self):
        """Store a model into a binary file"""
        pass

    def set_training_set(self, training_set):
        """
        Set the training set
        @param(training_set) : list of couple (features vector, word sense)
        """
        pass

    def guess(self, vector):
        """
        Guess the best sense for a features vector
        @param(vector) : features vector
        @return : word sense
        """
        pass

    def train(self):
        """Train the model using the training set"""
        pass
