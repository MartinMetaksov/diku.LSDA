# NOTE: Use your the virtual machine to execute this code and
#       keep the memory allocated for the machine to 2GB!

import time
import numpy
from sklearn.neighbors import KNeighborsRegressor

# load data
print("Loading training data ...")
data_train = numpy.genfromtxt("data/train.csv", comments="#", delimiter=",")
Xtrain, ytrain = data_train[:,:-1], data_train[:,-1]
print("Loaded training data: n=%i, d=%i" % (Xtrain.shape[0], Xtrain.shape[1]))

# training phase
print("Fitting model ...")
# nearest neighbor regression model (DO NOT CHANGE PARAMETERS!)
model = KNeighborsRegressor(n_neighbors=10, algorithm="brute")
model.fit(Xtrain, ytrain)
print("Model fitted!")

# testing phase (apply model to a big test set!)
print("Applying model ...")

preds = []

start = time.time()
counter = 0
with open("data/test.csv", 'r') as ifile:
    for line in ifile:
        print("Processing line %i ..." % counter)
        if not line.startswith("#"):
            line = line.split(",")[:-1]
            x = numpy.array([float(p) for p in line])
            p = model.predict(x.reshape(1,-1))
            preds.append(p)
        counter += 1
end = time.time()

# output (here, 'preds' must be a list containing all predictions)
print("Predictions computed for %i patterns ...!" % len(preds))
print("Mean of predictions: %f" % numpy.mean(numpy.array(preds)))
print("Runtime for testing phase: %f" % (end-start))
