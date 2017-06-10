import time
import numpy
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error

# load data
print("Loading training data ...")
data_train = numpy.genfromtxt("data/train.csv", comments="#", delimiter=",")
Xtrain, ytrain = data_train[:,:-1], data_train[:,-1]
print("Loaded training data: n=%i, d=%i" % (Xtrain.shape[0], Xtrain.shape[1]))

# training phase
print("Fitting model ...")
model = KNeighborsRegressor(n_neighbors=10, algorithm="kd_tree")
model.fit(Xtrain, ytrain)
print("Model fitted!")

# testing phase
print("Loading testing data ...")
data_test = numpy.genfromtxt("data/test.csv", comments="#", delimiter=",")
Xtest, ytest = data_test[:,:-1], data_test[:,-1]
print("Loaded test data: n=%i, d=%i" % (Xtest.shape[0], Xtest.shape[1]))

print("Applying model ...")
start = time.time()
preds = model.predict(Xtest)
end = time.time()

# output
print("Predictions computed for %i patterns ...!" % len(preds))
print("Mean squared error: %f" % mean_squared_error(ytest, preds))
print("Runtime for testing phase: %f" % (end-start))
