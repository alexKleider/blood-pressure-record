#!/usr/bin/env python3

# File: last.py

"""
reads bps.txt and returns content limited to 1,000 characters
(but retaining the top (header) lines.)
"""

header_length = 127  # the top lines we keep
chars_allowed = 1000 - header_length
source_f  = "pressures.txt"
dest_f = "limited_pressures.txt"
spaces_to_indent = 6
indent = " " * 6 

def get_last():
    with open(source_f, 'r') as bps:
        headers = bps.read(header_length)
        readings = bps.read()
    allowed_part = readings[-chars_allowed:]
    first_cr = allowed_part.rindex("\n")
    txt = headers + allowed_part[:first_cr]
    yn = input(f"Send to {dest_f}? (yn): ")
    if yn and yn[0] in "yY":
        with open(dest_f, 'w') as outf:
            for line in txt.split("\n"):
                print(line, file=outf)
    return txt

print(get_last())
