#!/usr/bin/env python
import sys

total_count = 0
total_value = 0.0
old_key = None

for line in sys.stdin:

    line = line.strip()
    line = line.split('\t')
    if len(line) != 3:
        continue

    key, value, count = line

    try:
        value = float(value)
        count = int(count)
    except ValueError:
        continue

    if (old_key is not None) and (old_key != key):
        print('%s\t%f\t%i' % (old_key, total_value, total_count))
        total_value = 0.0
        total_count = 0

    old_key = key
    total_value += value
    total_count += count

if old_key is not None:
    print('%s\t%f\t%i' % (old_key, total_value, total_count))
