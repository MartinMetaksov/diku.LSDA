#!/usr/bin/env python
import sys
import string

# Where do these lines come from?
# This is done by Hadoop Streaming ...
for line in sys.stdin:

    line = line.strip()
    words = line.split(',')
    
    # attempt to parse the line. If anything fails, we skip it
    try:
        #print(words)
        a_id = int(words[1])
        a_d = float(words[10])
    except ValueError as e:
        #print ("Error .. skipping bad line %s \n due to %s ... " % (str(words),e));
        continue
    print('%s\t%s' % (a_id, a_d))