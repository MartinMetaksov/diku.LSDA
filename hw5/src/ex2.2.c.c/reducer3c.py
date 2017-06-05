#!/usr/bin/env python
import sys
counter=0
total_counter = 0
total_count=0
old_airport = None
max_val = 0
# Input from stdin (handled via Hadoop Streaming)
for line in sys.stdin:
    count=0
    # Remove whitespace and split up lines
    line = line.strip()
    line = line.split('\t')
    if len(line) != 3:
        continue

    # Get word and count
    airport, counter,total_delay = line
    try:
        counter = eval(counter)
        total_delay= eval(total_delay)
    except ValueError:
        continue

    # This if-statement only works because Hadoop sorts 
    # the output of the mapping phase by key (here, by 
    # word) before it is passed to the reducers. Each 
    # reducer gets all the values for a given key. Each 
    # reducer might get the values for MULTIPLE keys.
    if (old_airport is not None) and (old_airport != airport):
        average=total_count/total_counter
        print('%s\t%s' % (old_airport, average))
	total_count=0
        total_counter=0        

    old_airport = airport
    total_count+=total_delay
    total_counter+=counter

# We have to output the word count for the last word!
if old_airport is not None:
    average=total_count/total_counter
    print('%s\t%s' % (old_airport, average))
