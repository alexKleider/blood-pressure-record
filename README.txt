This project arose out of the 'need' to keep track of blood pressure
readings.  The easiest way to do this was to set up a text file using
vim and after some explanatory text at the top along with a header
line, each BP reading was recorded by first entering the date using:
!!date
Then the bp and pulse were appended to the line with the date.

The problem was that the date output included much more than was
necessary so this script was written to shorten each line- also the
year was made into a group header instead of appearing on each line.

Development then moved towards presenting the data in two columns to
keep the listing shorther.  In the current iteration, one can use
command line arguments to set the number of columns to any integer.  Also added has
been the ability to set a threashold systolic reading and when so set,
readings that exceede this limit are marked by an configurable alarm
character (which can also be set as a command line parameter) and
then reported separately.

Finally, another command line option was added to have the output
report how many readings fell into each of the American Heart
Association's 5 categories.

    ./bp.py --help

for details.

A typical source file is provided: bp.source

Python 3.6 syntax is used: specifically some static typing is
included.  If these are removed, the script will probably run
using earlier versions of Python, including 2.7.
