This project arose out of the 'need' to keep track of blood pressure
readings.  The easiest way to do this was to set up a text file using
vim and after some explanatory text at the top along with a header
line, each BP reading was recorded by first entering the date using:
!!date
Then the bp and pulse were appended to the line with the date.

Assuming one is running a 'nix type OS..
and that your relevant code base is in the $HOME/Git/BP directory..
and your data file is 'bps.txt' within that directory..
The following lines in ~/.bashrc:
    export BPS=$HOME/Git/BP/bps.txt
    alias bpdate="date +'%a %b %d %H:%M %Y' >> $BPS && vim $BPS"
... allow one to issue the command 'bpdate' 
and find yourself within vim ready to enter a BP reading following a
time stamp already provided.

The problem was that the `date` output included much more than was
necessary. This script was written to shorten each line- also the
month and year were made into a group header instead of appearing
on each line.

Development then moved towards presenting the data in two columns to
keep the listing shorther.  In the current iteration, one can use
command line arguments to set the number of columns to any integer.
Also added has been the ability to set a threashold systolic reading
and when so set, readings that exceede this limit are marked by an
alarm character which defaults to '!' but is configurable (command
line parameter) and then reported separately.

Finally, another command line option has been made available to
have the output report how many readings fall into each of the
American Heart Association's 5 categories.

Try:

    ./bp.py --help

for details.

A typical source file is provided: bps.txt

Command line options and arguments are implemented using the
non-standard library module `docopt`.  Use either `virtualenv`
    pip --user install docopt
    or
    sudo pip install docopt


Note: my .bashrc contains the following lines:
    export BPS=$HOME/Git/BP/bps.txt
    alias bpdate="date +'%a %b %d %H:%M %Y' >> $BPS && vim $BPS"
...so the command 'bpdate' sets up my bp data file for another entry.

