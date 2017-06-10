import time
import numpy
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error
import matplotlib

from forward import ForwardSelector

n_features = 15

# training data
print("Loading training data ...")
data_train = numpy.genfromtxt("data/train.csv", comments="#", delimiter=",")
Xtrain, ytrain = data_train[:,:-1], data_train[:,-1]
print("Loaded training data: n=%i, d=%i" % (Xtrain.shape[0], Xtrain.shape[1]))

# validation data
print("Loading validation data ...")
data_validation = numpy.genfromtxt("data/validation.csv", comments="#", delimiter=",")
Xval, yval = data_validation[:,:-1], data_validation[:,-1]
print("Loaded validation data: n=%i, d=%i" % (Xval.shape[0], Xval.shape[1]))

# training phase
print("Fitting model ...")
model = KNeighborsRegressor(n_neighbors=10, algorithm="kd_tree")
nnselector = ForwardSelector(model, n_features)
nnselector.fit(Xtrain, ytrain, Xval, yval)
print("Model fitted! Selected features: %s" % str(nnselector.features))

import matplotlib.pyplot as plt
plt.plot(nnselector.get_validation_errors())
plt.ylabel('validation errors')
plt.savefig("validation_errors_all.png")
