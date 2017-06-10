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

# training phase (DO NOT CHANGE PARAMETERS)
print("Fitting model ...")
model = KNeighborsRegressor(n_neighbors=10, algorithm="brute")
model.fit(Xtrain, ytrain)
print("Model fitted!")

# application phase (apply model to test set)
print("Loading testing data ...")
data_test = numpy.genfromtxt("data/test.csv", comments="#", delimiter=",")
Xtest, ytest = data_test[:,:-1], data_test[:,-1]
print("Loaded testing data: n=%i, d=%i" % (Xtest.shape[0], Xtest.shape[1]))

# create store and data sets
import h5py
store = h5py.File("data/test.csv.h5", 'w')
ytest = ytest.reshape((len(ytest),1))
dsetX = store.create_dataset("X", Xtest.shape, compression="lzf")
dsety = store.create_dataset("y", ytest.shape, compression="lzf")
dsetX[:,:] = Xtest
dsety[:,:] = ytest
store.close()

preds = []
chunk_size = 5000

start = time.time()

store = h5py.File("data/test.csv.h5", 'r')
dsetX = store.get("X")
dsety = store.get("y")

chunk_start = 0
chunk_end = chunk_size

while True:
    try:
        Xchunk, ychunk = dsetX[chunk_start:chunk_end], dsety[chunk_start:chunk_end]
        preds += list(model.predict(Xchunk))
        print("Predictions computed for %i patterns ..." % len(preds))
        chunk_start += chunk_size
        chunk_end += chunk_size
    except:
        break

end = time.time()

# output (here, 'preds' must be a list containing all predictions)
print("Predictions computed for %i patterns ...!" % len(preds))
print("Mean of predictions: %f" % numpy.mean(numpy.array(preds)))
print("Runtime for testing phase: %f" % (end-start))
