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
with open('data/test.csv') as f:
    next(f)
    for line in f:
        myline = numpy.fromstring(line, sep=",")
        Xtest=myline[:-1]
        Xtest=Xtest.reshape(1,-1)
        predi=model.predict(Xtest)
        preds.append(predi)
f.close()
end = time.time()

# TODO: Your code here, which processes the file line by line
# and that stores the output in the 'preds' list

# output (here, 'preds' must be a list containing all predictions)
print("Predictions computed for %i patterns ...!" % len(preds))
print("Mean of predictions: %f" % numpy.mean(numpy.array(preds)))
print("Runtime for testing phase: %f" % (end-start))
