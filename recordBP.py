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
    timestamp = now.strftime("%a %b %d: %H:%M")
    #Tuesday, March 24, 2026 at 01:00:57 PM
    while True:
        print("Enter BP and pulse in following format: Sys/Di pulse")
        bp_and_pulse = input("Sys/Di Pulse: ")
        data = bp_and_pulse.split()
        if len(data) != 2: continue
        pulse = data[1]
        bp = data[0].split("/")
        if len(bp) != 2: continue
        sy, di = bp
        break
    newline = f"{timestamp}  {sy}/{di} {pulse}"
    with open(bp_file, 'a') as f:
        f.write(newline)
    print(f"Appended to {bp_file}: {newline}.")


if __name__ == "__main__":
    append_bp_file()




