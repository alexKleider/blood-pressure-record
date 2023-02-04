#!/usr/bin/env python3

# File: gather_data.py

"""
Began work on this in early August 2022
after beginning to collaborate with Leam Hall on
his bp_tracker project. 
"""

infile = "bps.txt"


def bps_from_file(bp_file):
    """
    Each line in bp_file ending in xxx/xx xx
    is interpreted as a (systolic diastolic pulse)
    3 tuple which is collected into a list which is returned.
    """
    collector = []
    with open(bp_file, 'r') as instream:
        for line in instream:
            line = line.strip()
            words = line.split()
            if words:
                if words[0].startswith('#'):
                    continue
                if '!' in words[-1]:
                    words = words[:-1]
                if len(words) >= 2:
                    bp, pulse = words[-2:]
                    try:
                        pulse = int(pulse)
                    except ValueError:
                        print("Invalid line: '{}'.".format(line))
                        continue
                    systolic, diastolic = bp.split('/')
                    collector.append((systolic, diastolic, pulse, ))
    return collector


if __name__ == '__main__':
    values = bps_from_file(infile)
    for value in values:
        print("{}/{} {}".format(*value))

