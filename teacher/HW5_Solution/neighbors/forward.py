import copy
import numpy
from sklearn.metrics import mean_squared_error

class ForwardSelector(object):
    
    def __init__(self, model, n_features):

        self.model = model
        self.n_features = n_features

    def fit(self, Xtrain, ytrain, Xval, yval):

        features = numpy.zeros(Xtrain.shape[1], dtype=numpy.int)
        valerrors = []

        # incrementally add features
        for i in xrange(self.n_features):
            
            print("Adding additional feature ...")
            
            # compute validation errors for new potential 
            # features and return best feature index and error
            best_idx, best_error = self._compute_best_feature(Xtrain, ytrain, Xval, yval, features)
            print("Best feature index is: %i. Best validation error is: %f" % (best_idx, best_error))

            # select best feature            
            features[best_idx] = 1

            # store validation error (for plotting purposes)
            valerrors.append(best_error)

        # update features and validation errors
        self.features = features
        self.valerrors = valerrors

        # recompute final model 
        self.model.fit(Xtrain[:,self.features.astype(bool)], ytrain)

    def predict(self, X):
        
        return self.model.predict(X[:, self.features.astype(bool)])

    def get_validation_errors(self):

        return self.valerrors

    def _compute_best_feature(self, Xtrain, ytrain, Xval, yval, features):

        valerrors = numpy.inf * numpy.ones(Xtrain.shape[1], dtype=numpy.float)

        for j in xrange(Xtrain.shape[1]):

            # only check/add feature in case it is not selected yet
            if features[j] != 1:

                current_features = copy.deepcopy(features)
                current_features[j] = 1
                # fit model and compute validation error
                self.model.fit(Xtrain[:, current_features.astype(bool)], ytrain)
                preds = self.model.predict(Xval[:, current_features.astype(bool)])
                err = mean_squared_error(yval, preds)
                print("\tValidation error for feature %i: %f" % (j, err))
                valerrors[j] = err

        # compute index with smallest validation error
        best_idx = numpy.argmin(valerrors)
        best_err = numpy.min(valerrors)

        return best_idx, best_err

