#!/usr/bin/env python
import sys

total_count = 0
old_y = None

for line in sys.stdin:

    line = line.strip()
    line = line.split('\t')
    if len(line) != 2:
        continue

    y, count = line

    try:
        y = float(y)
        count = int(count)
    except ValueError:
        continue

    if (old_y is not None) and (old_y != y):
        print('%s\t%i' % (old_y, total_count))
        total_count = 0

    old_y = y
    total_count += count

if old_y is not None:
    print('%s\t%i' % (old_y, total_count))
