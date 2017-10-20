#!/usr/bin/env python
# File: bp.py

"""
Usage:
    python bp.py FILE [> outfile]
    python bp.py test

Reads a file and in each line looks for a time stamp of the format
returned by the date utility.  Each line with such a time stamp is
replaced by just the hour and minutes part without the seconds, the
time zone and the year components.
The day of week and date components are not disturbed.
Provided also is the ability to specify a 'header' line and 
its 'underline' so that these can also be replaced. For this, you'd
have to modify the source.
The year is entered as a separate line above any sequence of lines
the originals of which all share the same year.
The input file is specified as the first parameter. 
Output goes to stdout.

If the fist parameter is 'test', the test function is run.

Works with both python v2.7 and v3 up to and including v3.6
"""

import re
import sys
from typing import Union, List

sample: str = """
Sun Sep 24 09:18:48 PDT 2017 129/67 59 +
          ^     ^  ^   ^    ^
          |     |  |   |    |
          |     |  |   |     --29
          |     |  |    -------24
          |     |   -----------20
          |      --------------17
           --------------------11
"""

year: Union[str, None] = None

time_re: str = r'\b\d{2,2}:\d{2,2}:\d{2,2}\b'
time_pattern = re.compile(time_re)
year_re: str = r'\b\d{4}\b'
year_pattern = re.compile(year_re)

header: str = "Day Date   Time         Year sys/di pulse"
underline: str = "--- ------ ------------ ---- --- -- --"

replacement_header: str = "Day Date   Time  sys/di pulse"
replacement_underline: str = "--- ------ ----- --- -- --"

def process_header(line: str) -> Union[str, None]:
    if header in line:
        return replacement_header
    elif underline in line:
        return replacement_underline
    else:
        return None

def process_line(line: str) -> str:
    global year
    header: str = process_header(line)
    if header:
        return header
    match_object = time_pattern.search(line)
    if match_object:
        ret: List[str] = []
        b, e = match_object.span()
        match_object = year_pattern.search(line)
        if match_object:
            yr: str = match_object.group()
            if year != yr:
                year = yr
                ret.append(yr)
        new_data_line: str = line[:b + 5] + line[e + 9:]
        ret.append(new_data_line.rstrip())
        return '\n'.join(ret)
    else:
        return line.rstrip()

def test() -> None:
    """
    Each line of the 'sample' gets printed more than once.
    The sample begins with a blank line, and as is true for
    all lines that don't 'match' (i.e. contain a time stamp)
    it is reproduced twice. Lines that do match, appear
    four times.
    """
    print("Running a test- read the test docstring to make sense!")
    for line in sample.split('\n'):
        print(process_line(line))
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
else:
    print(
"No command line argument (an input file would be nice) provided.")

