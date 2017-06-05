#!/usr/bin/env python
import sys
counter=0
total_count = 0
old_word = None
max_val = 0
# Input from stdin (handled via Hadoop Streaming)
for line in sys.stdin:
    count=0
    # Remove whitespace and split up lines
    line = line.strip()
    line = line.split('\t')
    if len(line) != 2:
        continue

    # Get word and count
    word, count = line
    try:
        count = eval(count)
    except ValueError:
        continue

    # This if-statement only works because Hadoop sorts 
    # the output of the mapping phase by key (here, by 
    # word) before it is passed to the reducers. Each 
    # reducer gets all the values for a given key. Each 
    # reducer might get the values for MULTIPLE keys.
    if (old_word is not None) and (old_word != word):
        average=total_count/counter
        print('%s\t%s' % (old_word, average))
	total_count=0
        counter=0        

    old_word = word
    total_count+=count
    counter+=1

# We have to output the word count for the last word!
if old_word is not None:
    average=total_count/counter
    print('%s\t%s' % (old_word, average))
