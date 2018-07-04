#!/bin/bash

# golden = [('golden/sf.svg', (37.7749, -122.4194, 24, 0.125, True, None)),
#              ('golden/lon.svg', (51.5074, -0.1278, 12, 0.125, False, None)),
#              ('golden/syd.svg', (-33.8688, 151.2093, 40, 0.25, False, 10))]

python sundial.py --lat=37.7749 --lng=-122.4194 -d=24 -t=0.125 --dst -o golden/sf.svg
python sundial.py --lat=51.5074 --lng=-0.1278 -d=12 -t=0.125 > golden/lon.svg
python sundial.py --lat=-33.8688 --lng=151.2093 -d=40 -t=0.25 --adapt_for_meridian=10 -o golden/syd.svg