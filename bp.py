#!/usr/bin/env python

# File: bp.py

"""
Requires python 3.6 but only because of the static typing syntax.
If this is removed, the script will probably run on earlier versions
including 2.7.

Usage:
    t.py [-c n -a char -t sysbp] INFILE

Options:
    -c n, --columns=n  Specify number of columns.  [default: 2]
    -a char, --alarm=char  Specify the alarm character. [default: !]
    -t sysbp, --threashold=sysbp  Specify a threashold systolic blood
    preasure which will trigger the alarm character to be displayed
    [default: 135]

INFILE is expected to be a text file beginning with some header text
and then possibly two lines defined by the constants INPUT_HEADER
and INPUT_UNDERLINE.  Following that it expects to find lines
beginning with out put of the `date` command followed by a space
and the SYS/DIA space PULSE readings provided by standard home
blood preasure reading device.  The following is an example of
such a line:
Sun Sep 24 09:18:48 PDT 2017 129/67 59
The accompanying `bps.txt` file provides an example INFILE.

The output is directed to `StdOut` (and can hence be redirected to
a text file of your choice.) It consists of a more compact version
of the data suitable for printing and submitting to your health care
provider. An average and break down of worrisome elevated values is
also included. By default it is presented in two columns but this can
be specified by the argument to the <columns> option.
"""

import re
import sys
from typing import Union, List
import docopt
args = docopt.docopt(__doc__, version="v0.0")
#print(args)

# Configurable "constants" come from command line via docopt:
try:
    N_COLUMNS = int(args["--columns"])
except TypeError:
    print("'--columns' option must be an integer (and >0.)")
    exit()
if not N_COLUMNS > 0:
    print("'--columns' option must be an integer >0.")
    print("...changing it to the default of 2.")
    N_COLUMNS = 2
try:
  SYS = int(args["--threashold"])
except TypeError:
    print("'--threashold' option must be an integer.")
    exit()
if SYS < 0:
    print(
    "'--threashold' option can not be <0. Being set to 0- not used")
if not sys:
    ALARM = " "
else:
    ALARM = args["--alarm"]
    if len(ALARM) > 2:
        args["--alarm"] = args["--alarm"][1:-1]
    if len(ALARM) > 1:
        print("'--alarm' must be a single character: changing it to '!'.")
        ALARM = '!'

# Constants:
INPUT_HEADER: str =    "Day Date   Time         Year sys/di pulse"
INPUT_UNDERLINE: str = "--- ------ ------------ ---- --- -- --"

COLUMN_SPACER: str = ("     ")
COLUMN_HEADER: str =    ("Day Time   sys/di pulse")
COLUMN_UNDERLINE: str = ("--- ----   -----  -----")
FORMATTER = "{}"
header_line: str = COLUMN_HEADER
underline: str = COLUMN_UNDERLINE 
formatting_string: str = FORMATTER
for n in range(1, N_COLUMNS):
    header_line = header_line + COLUMN_SPACER + COLUMN_HEADER
    underline = underline + COLUMN_SPACER + COLUMN_UNDERLINE
    formatting_string = formatting_string + COLUMN_SPACER + FORMATTER

# Reg Ex:
line_re: str = r"""
[SMTWF][uoehra][neduit]  # week day- discarded
[ ]
(?P<month>[JFMAJSOND][aepuco][nbrylgptvc])
[ ]
(?P<date>[\s|\d]\d)
[ ]
(?P<time>\d\d:\d\d)
:\d\d  # seconds- discarded
[ ]
[A-Z]{3,3}  # time zone- discarded
[ ]
(?P<year>\d{4,4})
[ ]
(?P<systolic>\d{2,3})
[/]
(?P<diastolic>\d{2,3})
[ ]
(?P<pulse>\d{2,3})
"""
line_pattern = re.compile(line_re, re.VERBOSE)

# Globals:
headers_printed = False
alarm_declared = False
month: Union[str, None] = None
year: Union[str, None] = None
n_readings = sum_systolic = sum_diastolic = sum_pulse = 0
readings = []
high_systolics = []
superfluous_lines = []

def process_non_reading(line: str) -> str:
    if not ((INPUT_HEADER in line) or (INPUT_UNDERLINE in line)):
        return line.strip()

def clear_readings():
    global readings, headers_printed
    ## NOTE: n_readings here is NOT the global one.
    #### DEBUG ####
#   print("DEBUG:")
#   n = 0
#   for reading in readings:
#       n += 1
#       print("{:>3d}. {}".format(n, reading))
#   print("end of DEBUG")
    #### END DEBUG ####
    n_readings = len(readings)
    if n_readings:
        if not headers_printed:
            print(header_line)
            print(underline)
            headers_printed = True
        modulo = n_readings % N_COLUMNS
        if modulo:
            for i in range(N_COLUMNS - modulo):
                readings.append(COLUMN_UNDERLINE)
                n_readings += 1
        fraction_of_n = n_readings//N_COLUMNS
        terminator = fraction_of_n
        i = 0
        while i < terminator:
            tup = (readings[i], )
            for j in range(1, N_COLUMNS):
                tup = (*tup, readings[i + fraction_of_n * j])


            print(formatting_string.format(*tup))
            i += 1
        readings = []

def process_line(line: str):
    global sum_systolic, sum_diastolic, sum_pulse
    global year, month, readings, n_readings
    global superfluous_lines, high_systolics
    global headers_printed, alarm_declared
    match = line_pattern.search(line)
    if match:  # it's a reading
        if not headers_printed and  not alarm_declared and SYS:
            print("Systolic alarm ('{}') threshold set to {}.".format
                (ALARM, SYS))
            alarm_declared = True
        mo = match.group("month")
        date = match.group("date")
        time = match.group("time")
        yr = match.group("year")
        systolic = match.group("systolic")
        diastolic = match.group("diastolic")
        pulse = match.group("pulse")
        n_readings += 1
        if SYS and int(systolic) > SYS:
            high_systolics.append(int(systolic))
        sum_systolic += int(systolic)
        sum_diastolic += int(diastolic)
        sum_pulse += int(pulse)
        if year != yr or month != mo:
            clear_readings()
            year = yr
            month = mo
            print("{} {}:".format(year, month))
        if int(systolic) > SYS:
            alarm = ALARM
        else:
            alarm = " "
        readings.append("{:>2}: {}: {:>3}/{:<3}{}{:>3} ".format(
            date, time, systolic, diastolic, alarm, pulse))
    else:  # line is not a BP reading.
        if readings:
            current_reading = readings[-1]  # Save the reading so
            #                          can report were non reading
            #                          line was found.
            clear_readings()
        else:
            current_reading = "No reading yet"
        _line = process_non_reading(line) 
        if _line:
            if headers_printed:
                superfluous_lines.append((year, month, current_reading, _line))
            else:
                print(_line)

def main():
    global headers_printed, alarm_declared, month
    global year, n_readings, sum_systolic, sum_diastolic, sum_pulse
    global readings, high_systolics, superfluous_lines
    with open(args["INFILE"], 'r') as f_object:
        for line in f_object:
            process_line(line)
    clear_readings()
    if n_readings:

        avg_systolic = (sum_systolic/n_readings)
        avg_diastolic = (sum_diastolic/n_readings)
        avg_pulse = (sum_pulse/n_readings)
        print()
        print(
        "\tFor a total of {} readings, average is {:.0f}/{:.0f} {:.0f}"
            .format(n_readings, avg_systolic, avg_diastolic, avg_pulse)
        )
        n_highs = len(high_systolics)
        if n_highs and SYS:
            sys = SYS
            preamble1 = ("Of the {} (systolic) readings: "
                .format(n_readings))
            preamble2 = " " * len(preamble1)
            preamble = preamble1
            while n_highs:
                print("{}{:>3} were above {:>3}."
                    .format(preamble, n_highs, sys))
                preamble = preamble2
                sys = sys + 10
                next_level = [reading for reading in high_systolics
                        if reading > sys]
                n_highs = len(next_level)

        elif SYS:
            print("There are no systolics over the threashold")
    else:
        print("No readings to average.")

    if superfluous_lines:
        print()
        print(
        "Superfluous lines with readings after which they occured")
        print(
        "--------------------------------------------------------")
        for year, month, cur_r, sup_line in superfluous_lines:
            print("Line after '{} {}{}' is:  {}".format(
                year, month, cur_r, sup_line))
            
            
if __name__ == "__main__":
    print(args)
    main()
