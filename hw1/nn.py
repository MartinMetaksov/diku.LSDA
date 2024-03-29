# NOTE: Use your the virtual machine to execute this code and
#       keep the memory allocated for the machine to 2GB!

import numpy
from sklearn.neighbors import KNeighborsRegressor

# load data
print("Loading training data ...")
data_train = numpy.genfromtxt("data/train.csv", comments="#", delimiter=",")
Xtrain, ytrain = data_train[:, :-1], data_train[:, -1]
print("Loaded training data: n=%i, d=%i" % (Xtrain.shape[0], Xtrain.shape[1]))

# training phase
print("Fitting model ...")
# nearest neighbor regression model (DO NOT CHANGE PARAMETERS!)
model = KNeighborsRegressor(n_neighbors=10, algorithm="brute")
model.fit(Xtrain, ytrain)
print("Model fitted!")

# testing phase (apply model to a big test set!)
print("Loading testing data ...")
data_test = numpy.genfromtxt("data/test.csv", comments="#", delimiter=",")
Xtest, ytest = data_test[:, :-1], data_test[:, -1]
print("Loaded testing data: n=%i, d=%i" % (Xtest.shape[0], Xtest.shape[1]))

print("Applying model ...")
# FIXME: Fitting the model on all test points causes a MemoryError! 
preds = model.predict(Xtest)

# output (here, 'preds' must be a list containing all predictions)
print("Predictions computed for %i patterns ...!" % len(preds))
print("Mean of predictions: %f" % numpy.mean(numpy.array(preds)))
