#!/usr/bin/env python
import sys

for line in sys.stdin:

    line = line.split(',')
    
    if len(line) != 12:
        continue

    airport, delay = line[3].strip(), line[6].strip()
    airport = airport.replace('"', '')

    if delay == "":
        delay = "0"

    print('%s\t%s\t%s' % (airport, delay, 1))
