#!/usr/bin/env python
import sys
import json

old_aid = None
f_delays={}

for line in sys.stdin:

    line = line.strip()
    line = line.split('\t')
    if len(line) != 3:
        print("line not a triple: %s" % line)
        continue

    aid, fid, delay = line

    try:
        delay = float(delay)
        fid = int(fid)
    except ValueError as e:
        print("problem with casting in combiner: %s" % e)
        continue


    if (old_aid is not None) and (old_aid != aid):
        print('%s\t%s' % (old_aid, json.dumps(f_delays, separators=(',',':'),sort_keys=True)))
        f_delays={}
        old_aid=None
        
    old_aid = aid
    if fid not in f_delays.keys():
        f_delays[fid]=delay
    else:
        f_delays[fid]+=delay
if old_aid is not None:
    print('%s\t%s' % (old_aid, json.dumps(f_delays, separators=(',',':'),sort_keys=True)))
