#!/usr/bin/env python
#from __future__ import division
import sys

no_flights = 0 # number of flights
no_delays = 0
old_aid = None # airline_id

# Input from stdin (handled via Hadoop Streaming)
for line in sys.stdin:

    # Remove whitespace and split up lines
    line = line.strip()
    line = line.split('\t')
    if len(line) != 2:
        #print("badly formatted line %s", str(line))
        continue

    aid, adel = line

    try:
        aid = int(aid)
        adel = int(adel)
    except ValueError as e:
        #print ("Error .. skipping bad line %s \n due to %s ... " % (str(line),str(e)));
        continue

    if (old_aid is not None) and (old_aid != aid):
        print('%s\t%s' % (old_aid, (no_flights, no_delays, no_delays*1.0/no_flights)))
        old_aid = None
        no_delays = 0
        no_flights = 0

    old_aid = aid
    no_delays += adel
    no_flights += 1
    
# We have to output the word count for the last airline ID!
if old_aid is not None:
    print('%s\t%s\t%s\t%s' % (old_aid, no_flights, no_delays, no_delays*1.0/no_flight)))
    