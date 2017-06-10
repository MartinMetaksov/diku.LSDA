#!/usr/bin/env python
import sys
import numpy
import pickle

# open model: we have to specify the absolute path here, i.e., 
# where the model is stored in the file system. For instance
# /home/lsda/HW5/hadoop/forest/model.save. 
# Another option is  to submit this file as well to the 
# Hadoop cluster by adding "-file mode.save" to the Hadoop command.
model = pickle.load(open("/home/lsda/HW5/hadoop/forest/model.save", "rb"))

for line in sys.stdin:

    line = line.split(',')

    if len(line) != 10:
        continue

    # parse label and features
    y = float(line[0])
    x = numpy.array(line[1:], dtype=numpy.float).reshape((1,9))

    # compute prediction and error
    pred = model.predict(x)[0]
    error = (y != pred).astype(int)

    # output a single key, the error, and a count
    print('%s\t%f\t%s' % ("key", error, 1))
