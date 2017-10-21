This project arose out of the 'need' to keep track of blood pressure
readings.  The easiest way to do this was to set up a text file using
vim and after some explanatory text at the top along with a header
line, each BP reading was recorded by first entering the date using:
!!date
Then the bp and pulse were appended.

The problem was that the date output included much more than was
necessary so this script was written to shorten each line- also the
year was made into a group header instead of appearing on each line.

A typical source file is provided: bp.source
