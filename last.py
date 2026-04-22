#!/usr/bin/env python3

# File: last.py

"""
Reads bps.txt and returns content
limited to <chars_allowed> characters.
(but retaining the top (header) lines.)
<chars_allowed> defaults to 1000.
"""

header_length = 127  # the top lines we keep
chars_allowed = 1000 - header_length
source_f  = "pressures.txt"
dest_f = "limited_pressures.txt"

def get_last(source_f=source_f, 
             dest_f = dest_f,
             header_length=127,
             chars_allowed=chars_allowed,
             spaces2indent=0):
    indent = " " * spaces2indent 
    with open(source_f, 'r') as bps:
        headers = bps.read(header_length)
        readings = bps.read()
    allowed_part = readings[-chars_allowed:]
    first_cr = allowed_part.rindex("\n")
    txt = headers + allowed_part[:first_cr]
    yn = input(f"Send to {dest_f}? (yn): ")
    if yn and yn[0] in "nN":
        alt_dest = input(
            "Enter alterate destination file (or blank): ")
        if not alt_dest:
            return txt
        else:
            if alt_dest == source_f:
                print(f"Bad to destroy {source_f}!!!")
                return
            dest_f = alt_dest
    with open(dest_f, 'w') as outf:
        for line in txt.split("\n"):
            print(line, file=outf)
    return txt

print(get_last())
