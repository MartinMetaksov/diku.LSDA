#!/usr/bin/env python
import sys
import numpy as np
import pickle


model = pickle.load(open("/home/lsda/work/exam/5_hadoop/2_landsat_stats/model.save", "rb"))
chunk_sz = 40000
Xtest = np.zeros([chunk_sz,9])
ix = 0
for line in sys.stdin:
    
    line = line.split(',')

    if len(line) != 9:
        #print("badly formatted line %s", str(line))
        continue

    # parse label and features
    x = np.array(line, dtype=np.float).reshape((1,9))
    Xtest[ix,:]=x
    ix += 1

    if ix==chunk_sz:
        # output a single key, the error, and a count
        yhat = model.predict(Xtest)
        #print(yhat)
        for i_y in range(ix):
            y = yhat[i_y]
            print('%s\t%i' % (y, 1))
        ix=0
if ix>0:
    yhat = model.predict(Xtest[0:ix,:])
    #print(yhat)
    for i_y in range(ix):
        y = yhat[i_y]
        print('%s\t%i' % (y, 1))
