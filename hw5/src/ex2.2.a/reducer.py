#!/usr/bin/env python
import sys

total_delay = 0
old_airport = None

# Input from stdin (handled via Hadoop Streaming)
for line in sys.stdin:
    count=0
    # Remove whitespace and split up lines
    line = line.strip()
    line = line.split('\t')
    if len(line) != 2:
        continue

    # Get airport and delay
    airport, delay = line

    try:
        delay = eval(delay)
    except ValueError:
        continue

    # This if-statement only works because Hadoop sorts 
    # the output of the mapping phase by key (here, by 
    # airports) before it is passed to the reducers. Each 
    # reducer gets all the values for a given key. Each 
    # reducer might get the values for MULTIPLE keys.
    if (old_airport is not None) and (old_airport != airport):
        print('%s\t%s' % (old_airport, total_delay))
        total_delay = 0        

    old_airport = airport
    total_delay += delay

# We have to output the airport delay for the last airport!
if old_airport is not None:
    print('%s\t%s' % (old_airport, total_delay))
