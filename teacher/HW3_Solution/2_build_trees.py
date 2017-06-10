import pickle
import numpy
from sklearn.ensemble import RandomForestClassifier

# load data
print("Loading training data ...")
data_train = numpy.genfromtxt("landsat_train_subset.csv", delimiter=",")
Xtrain, ytrain = data_train[:,1:], data_train[:,0]
print("Loaded training data: n=%i, d=%i" % (Xtrain.shape[0], Xtrain.shape[1]))

# training phase
print("Fitting model ...")
model = RandomForestClassifier(n_estimators=10, 
                               criterion='gini',
                               max_depth=None, 
                               min_samples_split=2, 
                               max_features=None)
model.fit(Xtrain, ytrain)
print("Model fitted!")

# save model
pickle.dump(model, open("model.save", 'wb'))
