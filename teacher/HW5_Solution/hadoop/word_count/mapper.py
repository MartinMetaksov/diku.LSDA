#!/usr/bin/env python
import sys

# Where do these lines come from?
# This is done by Hadoop Streaming ...
for line in sys.stdin:

    # Remove whitespace and split up line
    # into words (whitespace as delimiter)
    line = line.strip()
    line = line.replace(".","")
    line = line.replace(",","")
    line = line.replace("!","")
    line = line.replace(":","")
    line = line.replace("?","")
    words = line.split()

    for word in words:

        # The output is written to 'stdout' and will
        # be used as input by the reducers. Hadoop
        # Streaming will split up the work and will
        # feed these new lines to the reducers!
        print('%s\t%s' % (word, 1))
