#!/usr/bin/env python
import sys

for line in sys.stdin:

    line = line.split(',')
    
    if len(line) != 12:
        continue

    airport, delay = line[4].strip(), line[8].strip()
    airport = airport.replace('"', '')

    if delay == "":
        delay = "0"

    print('%s\t%s' % (airport, delay))
