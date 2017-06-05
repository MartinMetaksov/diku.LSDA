#!/usr/bin/env python
import sys
import string
import numpy

# Where do these lines come from?
# This is done by Hadoop Streaming ...
count=0
for line in sys.stdin:
    if count==0:
       count+=1
       continue
   #split up lines- "," delimiter
    myline=line.split(',')
    if myline[6]=="":
	continue  
    if eval(myline[6])>=0:
        # The output is written to 'stdout' and will
        # be used as input by the reducers. Hadoop
        # Streaming will split up the work and will
        # feed these new lines to the reducers!
        print('%s\t%s' % (myline[3], myline[6]))
        
