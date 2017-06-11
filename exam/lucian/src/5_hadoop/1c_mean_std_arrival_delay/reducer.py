#!/usr/bin/env python
import sys
from math import sqrt

old_aid = None # airline_id
tot_mean = 0
tot_count = 0
tot_var= 0
# Input from stdin (handled via Hadoop Streaming)
for line in sys.stdin:

    # Remove whitespace and split up lines
    line = line.strip()
    line = line.split('\t')
    if len(line) != 4:
        print("badly formatted line %s", str(line))
        continue

    # Get word and count
    aid, dmean, dvar, dcount = line

    try:
        aid = int(aid)
        dcount = int(dcount)
        dmean = float(dmean)
        dvar = float(dvar)
    except ValueError as e:
        print ("Error .. skipping bad line %s \n due to %s ... " % (line,e));
        continue

    if (old_aid is not None) and (old_aid != aid):
        print('%s\t%s\t%s' % (old_aid, tot_mean, sqrt(tot_var)))
        old_aid = None
        tot_mean = 0
        tot_count = 0
        tot_var= 0

    old_aid = aid
    delta = dmean - tot_mean
    tot_mean = (tot_count*tot_mean + dcount*dmean)/(tot_count + dcount)
    tot_sum_squared_deltas = dvar*dcount + tot_var*tot_count + delta ** 2 * (tot_count*dcount)/(tot_count + dcount)
    tot_count += dcount
    tot_var=tot_sum_squared_deltas/tot_count
    

if old_aid is not None:
    print('%s\t%s\t%s' % (old_aid, tot_mean, sqrt(tot_var)))