import random
import pickle
import numpy
from scipy.stats import mode
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier

def chunk_generator(fname, chunk_size=1000):

    data = []
    counter = 0

    with open(fname, 'r') as ifile:

        for line in ifile:
            if counter < chunk_size:
                line = line.split(",")
                data.append([float(p) for p in line])
                counter += 1
            if counter == chunk_size:
                counter = 0
                yield data
                data = []

        # process remaining elements
        if len(data) > 0:
            yield data

class BigRFClassifier(object):

    def __init__(self, n_estimators=10):
        
        self.n_estimators = n_estimators

    def fit(self, X, y):

        for i in xrange(self.n_estimators):

            print("Fitting estimator %i ..." % i)
            rstate = random.randint(0,1000000)

            model = RandomForestClassifier(n_estimators=1, 
                                           criterion='gini',
                                           max_depth=None, 
                                           min_samples_split=2, 
                                           max_features=None,
                                           random_state=rstate)
            model.fit(X,y)

            pickle.dump(model, open("trees/" + str(i) + ".tree", 'wb'))

    def predict(self, X):
        
        allpreds = numpy.empty((len(X), self.n_estimators), dtype=numpy.int32)

        for i in xrange(self.n_estimators):
            print("Processing predictions for tree %i ..." % i)
            model = pickle.load(open("trees/" + str(i) + ".tree", 'rb'))
            allpreds[:,i] = model.predict(X)

        preds, _ = mode(allpreds, axis=1)
        preds = preds[:, 0]

        return numpy.array(preds)


# Load data
print("Loading training data ...")
data_train = numpy.genfromtxt("landsat_train_subset_1m.csv", delimiter=",")
Xtrain, ytrain = data_train[:,1:], data_train[:,0]
print("Loaded training data: n=%i, d=%i" % (Xtrain.shape[0], Xtrain.shape[1]))

# Training phase
print("Fitting model ...")
model = BigRFClassifier(n_estimators=100)
model.fit(Xtrain, ytrain)
print("Model fitted!")

# Get predictions (accuracy should be close to 1.0)
preds = model.predict(Xtrain)
print("Training accuracy: %f" % accuracy_score(ytrain, preds))

# Testing phase
print("""Note: If executed again, you have to remove the file 'big_predictions_test.csv' 
         beforehand; otherwise, you will append more and more lines to them ...
      """)

print("Testing phase ...")
for chunk in chunk_generator("landsat_test.csv", chunk_size=1000000):

    chunk = numpy.array(chunk)
    preds_test = model.predict(chunk)

    with open('big_predictions_test.csv','a') as ofile:
        numpy.savetxt(ofile, preds_test.astype(int), fmt='%i', delimiter=",")

    print("Predictions computed for %i patterns ..." % len(preds_test))

