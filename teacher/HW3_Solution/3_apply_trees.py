import pickle
import numpy
    
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

def avg_error_from_file(fname, chunk_size=1000000):

    n_all = 0
    n_errors = 0

    for chunk in chunk_generator(fname, chunk_size=chunk_size):
        chunk = numpy.array(chunk)
        yvals, preds_val = chunk[:,0], chunk[:,1]
        n_errors += (yvals != preds_val).sum()
        n_all += len(chunk)
        print("Errors computed for %i patterns ..." % n_all)

    return float(n_errors) / float(n_all)

# IMPORTANT
print("""Note: If executed again, you have to remove the 
         files 'validation.csv' and 'predictions_test.csv' 
         beforehand; otherwise, you will append more and 
         more lines to them ...
      """)

# Load model from file again
print("Loading model ...")
model = pickle.load(open("model.save", "rb"))

# Validation phase
print("Validation phase ...")

for chunk in chunk_generator("landsat_train_remaining.csv", chunk_size=1000000):

    chunk = numpy.array(chunk)
    yval, preds_val = chunk[:,0], model.predict(chunk[:,1:])
    data_val = numpy.empty((yval.shape[0], 2))
    data_val[:,0] = yval
    data_val[:,1] = preds_val

    with open('validation.csv','a') as ofile:
        numpy.savetxt(ofile, data_val.astype(int), fmt='%i', delimiter=",")

    print("Predictions computed for %i patterns ..." % len(preds_val))

err_val = avg_error_from_file("validation.csv")
print("Validation error is: %f" % err_val)

# Testing phase
print("Testing phase ...")

for chunk in chunk_generator("landsat_test.csv", chunk_size=1000000):

    chunk = numpy.array(chunk)
    preds_test = model.predict(chunk)

    with open('predictions_test.csv','a') as ofile:
        numpy.savetxt(ofile, preds_test.astype(int), fmt='%i', delimiter=",")

    print("Predictions computed for %i patterns ..." % len(preds_test))

