#!/usr/bin/env python3

# File: /home/alex/Git/BP/recordBP.py

"""
Python equvalent of bash alias bpdate
but with abreviated year. ('26 vs 2026)
"""

bp_file = "pressures.txt"

def append_bp_file():
    from datetime import datetime
    now = datetime.now()
    timestamp = now.strftime("%a %b %d '%y %H:%M %p")
    #Tuesday, March 24, 2026 at 01:00:57 PM
    bp_and_pulse = input("Sys/Di Pulse: ")
    newline = f"\n{timestamp}  {bp_and_pulse}"
    with open(bp_file, 'a') as f:
        f.write(newline)


if __name__ == "__main__":
    append_bp_file()




