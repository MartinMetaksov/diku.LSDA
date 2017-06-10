#!/usr/bin/env python
import sys

max_delay = float("-inf")
old_airport = None

for line in sys.stdin:

    line = line.strip()
    line = line.split('\t')
    if len(line) != 2:
        continue

    # Get airport and delay
    airport, delay = line

    try:
        delay = float(delay)
    except ValueError:
        continue

    if (old_airport is not None) and (old_airport != airport):
        print('%s\t%f' % (old_airport, max_delay))
        max_delay = float("-inf")

    old_airport = airport
    max_delay = max(max_delay, delay)

if old_airport is not None:
    print('%s\t%f' % (old_airport, max_delay))
