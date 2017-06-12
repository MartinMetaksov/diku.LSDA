#!/usr/bin/env python
import sys
import json
from collections import Counter

old_aid = None # airline_id
tot_delays=None
highest10_del=[]
call_count = 0

# Input from stdin (handled via Hadoop Streaming)
for line in sys.stdin:

    # Remove whitespace and split up lines
    #print(line)
    
    line = line.strip()
    line = line.split('\t')
    if len(line) != 2:
        print("badly formatted line %s", str(line))
        continue

    # Get word and count
    aid, f_del = line

    try:
        aid = int(aid)
        f_del = json.loads(f_del)
    except ValueError as e:
        print ("Error .. skipping bad line %s \n due to %s ... " % (line,e));
        continue
        
    if (old_aid is not None) and (old_aid != aid):
        for k, v in Counter(tot_delays).most_common(10):
            highest10_del.append((str(k),v))
        print('%s\t%s' % (old_aid, highest10_del))
        #print("Reducer processed %i inputs for Airline ID %s" %(call_count,old_aid))
        old_aid = None
        tot_delays=None
        highest10_del = []
        call_count = 0
        
    old_aid = aid
    #print("reducing for aid : %s" % aid)
    call_count += 1
    if tot_delays is None:
        tot_delays = f_del
    else:
        for k,v in f_del.iteritems():
            if k in tot_delays.keys():
                tot_delays[k]+=v
            else:
                tot_delays[k]=v
if old_aid is not None:
    for k, v in Counter(tot_delays).most_common(10):
        highest10_del.append((str(k),v))
    print('%s\t%s' % (old_aid, highest10_del))