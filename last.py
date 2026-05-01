#!/usr/bin/env python3

# File: last.py

"""
Reads bps.txt and returns content
limited to <chars_allowed> characters.
(but retaining the top (header) lines.)
<chars_allowed> defaults to 1000.
"""

header_length = 127  # the top lines we keep
    # being replaced by n_header_lines
salutation = """Most recent readings...
"""
source_f  = "pressures.txt"
dest_f = "limited_BPs.txt"
chars_allowed = 1000 - header_length -len(salutation)
n_header_lines = 4  # number of header
                    # lines to preserve.

def get_last(source_f,
             dest_f=dest_f,
             n_header_lines=4,
             n_new_header = salutation,
             chars_allowed=chars_allowed,
             spaces2indent=0):
    def send2file(txt, dest_f):
        if dest_f == source_f:
            print(f"Bad to destroy {source_f}!!!")
            return
        else:
            with open(dest_f, 'w') as outf:
                print(txt, file=outf)

    indent = " " * spaces2indent 
    with open(source_f, 'r') as bps:
        headers = []
        while len(headers) < n_header_lines:
            headers.append(bps.readline())
        readings = bps.read()
    chars_allowed = chars_allowed-len(n_new_header)
#   allowed_part = readings[-(chars_allowed-3):]
    remaining_part = readings[-(chars_allowed):]
    first_cr = remaining_part.find("\n") + 1
    remaining_part = remaining_part[first_cr:]
    txt = "".join(headers) + remaining_part
    yn = input(f"Send to {dest_f}? (yn): ")
    if yn and yn[0] in "nN":
        alt_dest = input(
            "Enter alterate destination file (or blank): ")
        if not alt_dest:
            return txt
        else:
            send2file(salutation+txt, alt_dest)
    else:
        send2file(salutation+txt, dest_f)
    return txt

def ck_get_last():
    n2indent = input("Spaces to indent? (blank==0): ")
    if not n2indent: n2indent=0
    else: n2indent = int(n2indent)
    ret = get_last(source_f, dest_f,
                   spaces2indent=n2indent)
    yn = input(
            "Send result to terminal? (y/n): ")
    if yn and yn[0] in "yY":
        for line in ret:
            print(line)

if __name__ == "__main__":
    ck_get_last()

