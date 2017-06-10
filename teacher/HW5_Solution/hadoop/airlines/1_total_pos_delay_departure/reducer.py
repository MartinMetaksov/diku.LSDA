#!/usr/bin/env python
import sys

total_delay = 0.0
old_airport = None

for line in sys.stdin:

    line = line.strip()
    line = line.split('\t')
    if len(line) != 2:
        continue

    airport, delay = line

    try:
        delay = float(delay)
    except ValueError:
        continue

    # ignore negative delays (or: continue)
    if delay < 0.0:
        delay = 0.0

    if (old_airport is not None) and (old_airport != airport):
        print('%s\t%f' % (old_airport, total_delay))
        total_delay = 0.0

    old_airport = airport
    total_delay += delay

if old_airport is not None:
    print('%s\t%f' % (old_airport, total_delay))
