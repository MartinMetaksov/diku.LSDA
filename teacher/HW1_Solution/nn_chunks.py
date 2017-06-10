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

# application phase (apply model to test set)
print("Applying model ...")

preds = []
chunk_size = 1000

start = time.time()

def chunk_generator(fname, chunk_size=1000):

    data = []
    counter = 0

    with open(fname, 'r') as ifile:

        for line in ifile:
            if not line.startswith("#") and counter < chunk_size:
                line = line.split(",")[:-1]
                data.append([float(p) for p in line])
                counter += 1
            if counter == chunk_size:
                counter = 0
                yield data
                data = []

        # process remaining elements
        if len(data) > 0:
            yield data

preds = []
    
for chunk in chunk_generator("data/test.csv", chunk_size=1000):

    preds += list(model.predict(numpy.array(chunk)))
    print("Predictions computed for %i patterns ..." % len(preds))

end = time.time()

# output (here, 'preds' must be a list containing all predictions)
print("Predictions computed for %i patterns ...!" % len(preds))
print("Mean of predictions: %f" % numpy.mean(numpy.array(preds)))
print("Runtime for testing phase: %f" % (end-start))
