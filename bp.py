# File: bp.py
# usage: python3.6 bp.py [> outfile]

"""
Reads a file and looks for a time stamp of the format returned by the
date utility.  Each line with such a time stamp is replaced by just
the hour and minutes part without the time zone and year components.
The day of week and date components are not disturbed.
Provided also is the ability to specify a 'header' line and 
its 'underline' so that these can also be replaced.
The input file is specified as the first parameter. 
Output goes to stdout.
"""

import re
import sys

sample = """
Sun Sep 24 09:18:48 PDT 2017 129/67 59 +
          ^     ^  ^   ^    ^
          |     |  |   |    \ 
          |     |  |   \     --29
          |     |  \    -------24
          |     \   -----------20
          \      --------------17
           --------------------11
"""

year = None

time_re = r'\b\d{2,2}:\d{2,2}:\d{2,2}\b'
time_pattern = re.compile(time_re)
year_re = r'\b\d{4}\b'
year_pattern = re.compile(year_re)

header = "Day Date   Time         Year sys/di pulse"
underline = "--- ------ ------------ ---- --- -- --"

replacement_header = "Day Date   Time  sys/di pulse"
replacement_underline = "--- ------ ----- --- -- --"

def process_header(line):
    if header in line:
        return replacement_header
    if underline in line:
        return replacement_underline


def process_line(line):
    global year
    header = process_header(line)
    if header:
        return header
    match_object = time_pattern.search(line)
    if match_object:
        ret = []
        b, e = match_object.span()
        match_object = year_pattern.search(line)
        if match_object:
            yr = match_object.group()
            if year != yr:
                year = yr
                ret.append(yr)
        new_data_line = line[:b + 5] + line[e + 9:]
        ret.append(new_data_line.strip())
        return '\n'.join(ret)
    else:
        return line.strip()

def test():
    for line in sample.split('\n'):
        match_object = time_pattern.search(line)
        if match_object:
            b, e = match_object.span()
            print(line)
            modified_line = line[:b + 5] + line[e + 9:]
            print(modified_line)
            print(match_object.span())
        print(line)

if len(sys.argv) > 1:
    if sys.argv[1] == "test":
        test()
    else:
        with open(sys.argv[1], 'r') as f_object:
            for line in f_object:
                print(process_line(line))

