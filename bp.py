#!/usr/bin/env python3

# File: bp.py

"""
A Python utility to help analyse blood presure (and pulse) recordings.

Usage:
    t.py [-c n -a char -t sysbp] INFILE
    t.py [-c n -a char -r] INFILE

Options:
    -h --help     Show this screen.
    --version     Show version.
    -c <n>, --columns=<n>  Specify number of columns.  [default: 2]
    -a <char>, --alarm=<char>  Specify the alarm character. [default: !]
    -t <sysbp>, --threashold=<sysbp>  Specify a threashold systolic blood
    preasure which will trigger the alarm character to be displayed
    [default: 0]
    -r --report  Report how the American Heart Association criteria
    apply. Each elevated pressure reading will be separated from its
    corresponding pulse reading by a digit representing how elevated
    the pressure is- ' ' if normal, '1' = elevated, '2' = stage 1,
    '3' = stage 2, '4' = crisis.

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

from aha import AHA

import re
import sys
import docopt

args = docopt.docopt(__doc__, version="v0.0")
#print(args)

# Configurable "constants" come from command line via docopt:
try:
    N_COLUMNS = int(args["--columns"])
except TypeError:
    print("'--columns' option must be an integer (and >0.)")
    sys.exit()
if not N_COLUMNS > 0:
    print("'--columns' option must be an integer >0.")
    print("...changing it to the default of 2.")
    N_COLUMNS = 2
try:
  SYS = int(args["--threashold"])
except TypeError:
    print("'--threashold' option must be an integer.")
    sys.exit()
if SYS < 0:
    print(
    "'--threashold' option can not be <0. Being set to 0- not used")
if not SYS:
    ALARM = " "
else:
    ALARM = args["--alarm"]
    if len(ALARM) > 2:
        args["--alarm"] = args["--alarm"][1:-1]
    if len(ALARM) > 1:
        print("'--alarm' must be a single character: changing it to '!'.")
        ALARM = '!'

# Constants:
INPUT_HEADER =    "Day Date   Time         Year sys/di pulse"
INPUT_UNDERLINE = "--- ------ ------------ ---- --- -- --"

COLUMN_SPACER = ("     ")
COLUMN_HEADER =    ("Day Time   sys/di pulse")
COLUMN_UNDERLINE = ("--- ----   -----  -----")
FORMATTER = "{}"
header_line = COLUMN_HEADER
underline = COLUMN_UNDERLINE 
formatting_string = FORMATTER
for n in range(1, N_COLUMNS):
    header_line = header_line + COLUMN_SPACER + COLUMN_HEADER
    underline = underline + COLUMN_SPACER + COLUMN_UNDERLINE
    formatting_string = formatting_string + COLUMN_SPACER + FORMATTER

# Reg Ex:
line_re = r"""
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
[ ]+
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
month = None
year = None
list_of_readings = []
high_systolics = []
superfluous_lines = []

def process_non_reading(line):
    if not ((INPUT_HEADER in line) or (INPUT_UNDERLINE in line)):
        return line.strip()

def clear_readings():
    global list_of_readings, headers_printed
    #### DEBUG ####
#   print("DEBUG:")
#   n = 0
#   for reading in list_of_readings:
#       n += 1
#       print("{:>3d}. {}".format(n, reading))
#   print("end of DEBUG")
    #### END DEBUG ####
    n_readings = len(list_of_readings)
    if n_readings:
        modulo = n_readings % N_COLUMNS
        if modulo:
            for i in range(N_COLUMNS - modulo):
                list_of_readings.append(COLUMN_UNDERLINE)
                n_readings += 1
        fraction_of_n = n_readings//N_COLUMNS
        terminator = fraction_of_n
        i = 0
        while i < terminator:
            tup = (list_of_readings[i], )
            for j in range(1, N_COLUMNS):
                tup = (*tup, list_of_readings[i + fraction_of_n * j])
            print(formatting_string.format(*tup))
            i += 1
        list_of_readings = []

def process_line(line, aha):
    global year, month, list_of_readings
    global superfluous_lines, high_systolics
    global headers_printed, alarm_declared
    match = line_pattern.search(line)
    if match:  # it's a reading
        if not alarm_declared and SYS:
            print("Systolic alarm ('{}') threshold set to {}.".format
                (ALARM, SYS))
            alarm_declared = True
        if not headers_printed:
            print(header_line)
            print(underline)
            headers_printed = True
        mo = match.group("month")
        date = match.group("date")
        time = match.group("time")
        yr = match.group("year")
        systolic = int(match.group("systolic"))
        diastolic = int(match.group("diastolic"))
        pulse = int(match.group("pulse"))
        if SYS and systolic > SYS:
            high_systolics.append(systolic)
        if year != yr or month != mo:
            clear_readings()
            year = yr
            month = mo
            print("{} {}:".format(year, month))
        if args["--report"]:
            cat = aha.category_int(systolic, diastolic) 
            alarm = aha.categories[cat]["level"]
        elif systolic > SYS:
            alarm = ALARM
        else:
            alarm = " "
        list_of_readings.append("{:>2}: {}: {:>3}/{:<3}{}{:>3} ".format(
            date, time, systolic, diastolic, alarm, pulse))
        aha.add_reading(systolic, diastolic, pulse)
    else:  # line is not a BP reading.
        if list_of_readings:
            current_reading = list_of_readings[-1]  # Save the reading so
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
    aha = AHA()
    global headers_printed, alarm_declared, month, year
    global list_of_readings, high_systolics, superfluous_lines
    with open(args["INFILE"], 'r') as f_object:
        for line in f_object:
            process_line(line, aha)
    clear_readings()
    if aha.n_readings:
        avg_systolic, avg_diastolic, avg_pulse = (
            aha.average_all_readings())
#       print()
        cat = aha.category_int(avg_systolic, avg_diastolic)
        print(
        "Summary: For a total of {} readings, average is {:.0f}/{:.0f} {:.0f}"
            .format(aha.n_readings,
                avg_systolic,
                avg_diastolic,
                avg_pulse)
        + "  That's '{}'."
            .format(aha.categories[cat]["expanded_name"]))
        n_highs = len(high_systolics)
        if n_highs and SYS:
            sysbp = SYS
            preamble1 = ("Of the {} (systolic) readings: "
                .format(n_readings))
            preamble2 = " " * len(preamble1)
            preamble = preamble1
            while n_highs:
                print("{}{:>3} were above {:>3}."
                    .format(preamble, n_highs, sysbp))
                preamble = preamble2
                sysbp = sysbp + 10
                next_level = [reading for reading in high_systolics
                        if reading > sysbp]
                n_highs = len(next_level)
        elif args["--report"]:
#           print()
            for line in aha.show_category_breakdown(
                with_headers=True):
                print(line)
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
#   print(args)
    main()
