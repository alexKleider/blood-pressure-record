#!/usr/bin/env python

# File: t.py

"""
Usage:
    t.py [-c n -a char -t sysbp -t sysbp] INFILE

Options:
    -c n, --columns=n  Specify number of columns.  [default: 2]
    -a char, --alarm=char  Specify the alarm character. [default: ]
    -t sysbp, --threashold=sysbp  Specify a threashold systolic blood
    preasure which will trigger the alarm character to be displayed
    [default: 135]
"""

import docopt

args = docopt.docopt(__doc__, version=0.0)
if len(args["--alarm"]) > 2:
    args["--alarm"] = args["--alarm"][1:-1]

print(args)

