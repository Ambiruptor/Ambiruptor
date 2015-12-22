from sklearn import datasets
import numpy as np
import os.path
import re

from ambiruptor.library.preprocessors.data_structures import TrainData
from ambiruptor.library.preprocessors.feature_extractors \
    import DummyFeatureExtractor
from ambiruptor.library.learners.models import LinearSVMClassifier
from ambiruptor.library.miners.wiki_miners import DataMining


def generate_train_data():
    iris = datasets.load_iris()
    X1, y1 = iris.data, iris.target
    X2, y2 = iris.data, iris.target
    X3, y3 = iris.data, iris.target

    def assign_label_iris1(n):
        if (n == 0):
            return "Setosa"
        elif (n == 1):
            return "Lactosa"
        elif (n == 2):
            return "Spinosa"

    def assign_label_iris2(n):
        if (n == 0):
            return "Rice"
        elif (n == 1):
            return "Pasta"
        elif (n == 2):
            return "Pure"

    def assign_label_iris3(n):
        if (n == 0):
            return "Positive"
        elif (n == 1):
            return "Negavite"
        elif (n == 2):
            return "Neutral"

    y1 = np.array([assign_label_iris1(l) for l in y1])
    y2 = np.array([assign_label_iris2(l) for l in y2])
    y3 = np.array([assign_label_iris3(l) for l in y3])

    words = ["flower", "food", "thething"]
    senses = {
        "flower": ["Setosa", "Lactosa", "Spinosa"],
        "food": ["Rice", "Pasta", "Pure"],
        "thething": ["Positive", "Negative", "Neutral"]
    }

    x = {"flower": X1, "food": X2, "thething": X3}
    y = {"flower": y1, "food": y2, "thething": y3}

    train_data = TrainData(words, senses, x, y)
    return train_data


if __name__ == '__main__':
    data = DataMining()
    data.set_wikidump_filename("data/wikidump.xml")
    data.set_database_filename("data/wikidump.db")
    data.build()
    print(data.get_corpus("Bar"))

    # Test learning with Dummy Feature Extarctor
    train_data = generate_train_data()

    model = LinearSVMClassifier()
    model.train(train_data)

    text = """Lorem flower ipsum dolor sit amet, thething food
     consectetur adipiscing elit, sed do thething eiusmod
     tempor incididunt ut labore et dolore magna aliqua. Ut enim
     ad food minim veniam, flower quis nostrud exercitation ullamco
     laboris nisi ut aliquip food ex ea commodo consequat. Duis aute
     irure dolor in food reprehenderit flower in voluptate velit esse
     cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat
     food cupidatat non food proident thething, sunt in culpa qui thething
     officia flower deserunt mollit anim id est laborum"""

    fe = DummyFeatureExtractor()
    data = fe.extract_features(text, train_data.senses)
    labels = model.predict(data)
    print(labels)
