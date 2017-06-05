#!/usr/bin/env python
import sys
import string
import numpy
#new dictionary
my_dict={}
# Where do these lines come from?
# This is done by Hadoop Streaming ...
count=0
for line in sys.stdin:
    if count==0:
       count+=1
       continue
    # split up line
    # into words ("," as delimiter)
    myline=line.split(',')
    if myline[6]=="":
	continue  
    if eval(myline[6])>=0:
    #store the values into dictionary
    #used dictionary as combiner 
        if myline[3] not in my_dict:
           new_value=1,eval(myline[6])
           my_dict[myline[3]]=new_value
        else:
           old_value=my_dict[myline[3]]
           new_value=old_value[0]+1,old_value[1]+eval(myline[6])
           my_dict[myline[3]]=new_value
        #print('%s\t%s' % (myline[3], myline[6]))
count=0
 # The output is written to 'stdout' and will
        # be used as input by the reducers. Hadoop
        # Streaming will split up the work and will
        # feed these new lines to the reducers! 
        #print the whole dictionary
for k in my_dict:
    my_dict_values=my_dict[k]
    print('%s\t%s\t%s') % (k,my_dict_values[0],my_dict_values[1])
    count+=1
          
