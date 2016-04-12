import pickle
import sklearn.tree

model = pickle.load(open("data/models/Bar_(disambiguation).dump", "rb"))
features = pickle.load(open("data/feature_extractors/Bar_(disambiguation).dump", "rb"))
sklearn.tree.export_graphviz(model.model.estimators_[0], class_names=model.lb.classes_, feature_names=list(features.features[0].typicalwords))
