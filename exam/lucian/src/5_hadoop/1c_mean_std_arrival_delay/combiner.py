#!/usr/bin/env python
import sys

old_airport = None
n = 0
mean = 0.0
sum_squared_deltas = 0.0

for line in sys.stdin:

    line = line.strip()
    line = line.split('\t')
    if len(line) != 2:
        print("line not a tuple: %s" % line)
        continue

    airport, delay = line

    try:
        delay = float(delay)
    except ValueError:
        continue


    if (old_airport is not None) and (old_airport != airport):
        #from math import sqrt; print("local-only DEBUG .. total variance : %s" % sqrt(sum_squared_deltas/n))
        print('%s\t%f\t%f\t%i' % (old_airport, mean, sum_squared_deltas/n, n))
        n = 0
        mean = 0.0
        sum_squared_deltas = 0.0

    old_airport = airport
    n += 1
    delta_n0 = delay - mean
    mean += delta_n0/n
    delta_n1 = delay - mean
    sum_squared_deltas += delta_n0*delta_n1

if old_airport is not None:
    #from math import sqrt; print("local-only DEBUG .. total variance : %s" % sqrt(sum_squared_deltas/n))
    print('%s\t%f\t%f\t%i' % (old_airport, mean, sum_squared_deltas/n, n))
