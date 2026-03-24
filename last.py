#!/usr/bin/env python3

# File: last.py

"""
reads bps.txt and returns the last 1000 characters
"""

chars_allowed = 1000

def get_last():
    with open("bps.txt", 'r') as bps:
        all_chars = bps.read()
    allowed_part = all_chars[-chars_allowed:]
    first_cr = allowed_part.find("\n")
    return allowed_part[first_cr+1:]

print(get_last())
