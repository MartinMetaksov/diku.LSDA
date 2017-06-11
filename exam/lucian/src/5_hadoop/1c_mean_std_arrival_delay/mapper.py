#!/usr/bin/env python
import sys
import string

# Where do these lines come from?
# This is done by Hadoop Streaming ...
for line in sys.stdin:

    line = line.strip()
    words = line.split(',')
    # treat missing values as 0
    try:
        if words[8] == "":
            words[8] = "0"
    except ValueError:
        words[8] = "0"
    # attempt to parse the line. If anything fails, we skip it
    try:
        #print(words)
        a_id = int(words[1])
        a_del = float(words[8])
    except ValueError as e:
        #print ("Error .. skipping bad line %s \n due to %s ... " % (str(words),e));
        continue
    print('%s\t%s' % (a_id, a_del))