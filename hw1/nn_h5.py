# NOTE: Use your the virtual machine to execute this code and
#       keep the memory allocated for the machine to 2GB!

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


preds = []
chunk_size = 5000
#print(dsetX[0*5000:(0+1)*3,:])
# TODO: Your code here, which processes all test instances in 
# chunks of size chunk_size using the h5 store object generated 
# above and which appends all predictions to the 'preds' list.
for x in range(0,20):
	predi=model.predict(dsetX[(x*chunk_size):((x+1)*chunk_size),:])
	preds.append(predi)
store.close()

# output (here, 'preds' must be a list containing all predictions)
print("Predictions computed for %i patterns ...!" % len(preds))
print("Mean of predictions: %f" % numpy.mean(numpy.array(preds)))
