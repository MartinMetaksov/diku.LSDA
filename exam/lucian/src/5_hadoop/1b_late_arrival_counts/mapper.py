#!/usr/bin/env python
import sys
import string


for line in sys.stdin:

    line = line.strip()
    words = line.split(',')
    # treat missing values as 0
    if words[8] == "":
        words[8] = "0"
    
    # attempt to parse the line. If anything fails, we skip it
    try:
        #print(words)
        aid = int(words[1])
        adel = float(words[8])
        if adel <= 0:
            adel = 0
        else:
            adel = 1
    except ValueError as e:
        # print ("Error .. skipping bad line %s \n due to %s ... " % (str(words),str(e)));
        continue
    print('%s\t%s' % (aid, adel))