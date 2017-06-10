#!/usr/bin/env python
import sys

lowest_ad = sys.maxint # airport_distance
old_aid = None # airline_id

# Input from stdin (handled via Hadoop Streaming)
for line in sys.stdin:

    # Remove whitespace and split up lines
    line = line.strip()
    line = line.split('\t')
    if len(line) != 2:
        print("badly formatted line %s", str(line))
        continue

    # Get word and count
    aid, ad = line

    try:
        ad = float(ad)
        aid = int(aid)
    except ValueError as e:
        print ("Error .. skipping bad line %s \n due to %s ... " % (line,e));
        continue

    if (old_aid is not None) and (old_aid != aid):
        print('%s\t%s' % (old_aid, lowest_ad))
        lowest_ad = sys.maxint
        old_aid = None

    old_aid = aid
    if (ad < lowest_ad):
        lowest_ad = ad

# We have to output the word count for the last airline ID!
if old_aid is not None:
    print('%s\t%s' % (old_aid, lowest_ad))