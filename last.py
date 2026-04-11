#!/usr/bin/env python3

# File: new_last.py

"""
reads bps.txt and returns content limited to 1,000 characters
(but retaining the top (header) lines.)
"""

header_length = 127  # the top lines we keep
chars_allowed = 1000 - header_length
source_f  = "pressures.txt"

def get_last():
    with open(source_f, 'r') as bps:
        headers = bps.read(header_length)
        readings = bps.read()
    allowed_part = readings[-chars_allowed:]
    first_cr = allowed_part.rindex("\n")
    return headers + allowed_part[:first_cr]

print(get_last())
