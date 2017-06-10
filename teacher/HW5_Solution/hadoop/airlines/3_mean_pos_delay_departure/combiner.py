#!/usr/bin/env python
import sys

total_count = 0
total_delay = 0.0
old_airport = None

for line in sys.stdin:

    line = line.strip()
    line = line.split('\t')
    if len(line) != 3:
        continue

    airport, delay, count = line

    try:
        delay = float(delay)
        count = int(count)
    except ValueError:
        continue

    # ignore negative delays
    if delay < 0.0:
        continue

    if (old_airport is not None) and (old_airport != airport):
        print('%s\t%f\t%i' % (old_airport, total_delay, total_count))
        total_delay = 0.0
        total_count = 0

    old_airport = airport
    total_delay += delay
    total_count += count

if old_airport is not None:
    print('%s\t%f\t%i' % (old_airport, total_delay, total_count))
