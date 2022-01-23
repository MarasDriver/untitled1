# -*- coding: utf-8 -*-

"""
Title: TIE RawData Analyser
Author: Łukasz Dąbrowski <LDabrowski@advaoptical.com>

Module is designed to open and analyse *.txt.gz files containing
partial TIE data retrieved from OSA541x devices.
Data is merged from all selected files and then plotted using
matplotlib library (http://matplotlib.org).

It requires matplotlib version 1.4.2

Changelog:
2015-05-20  1.0.1   added check for non-contiguous data
                    save last used directory path to a file
2014-12-10  1.0.0   initial version

"""

import gzip
import re
import os.path
import matplotlib as mpl
import matplotlib.pyplot as plt
from Tkinter import Tk
from tkFileDialog import askopenfilenames

mpl.rcParams['agg.path.chunksize'] = 1000

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
__cfgfile__ = os.path.join(__location__, 'analyze')


class Measurement(object):
    """Class for storing TIE (x,y) data for further plotting.
    It also retrieves and keeps information on measurement, read from
    first imported data string
    """

    # RE pattern to recognise measurement information
    info_RE = re.compile(r"#(?P<attr>.+)\: (?P<value>.+)")

    def __init__(self):
        self.datax = []
        self.mask1 = []
        self.mask2 = []
        self.datay = []
        self.info = {}
        self.name = "TIE Measurement"

    def set_name(self, name):
        """Configure measurement name, used as a plt title."""
        self.name = str(name)

    def add_data(self, data):
        """Add TIE (x,y) and info data to measurement.

        Expected argument is a pre-formatted, multiline string, usually
        read from file.
        """
        for idx, line in enumerate(data):
            line = line.strip()
            try:
                x, y = line.split(', ')
            except ValueError:
                if line:
                    m = self.info_RE.match(line)
                    if m:
                        if not self.info.get(m.group('attr')):
                            self.info[m.group('attr')] = m.group('value')
                    else:
                        print "Error parsing line", idx + 1, ':', line
            else:
                if self.datax and float(x) < self.datax[-1]:
                    print ('Warning: Data point time is earlier '
                           'than previous ({} < {})'.format(float(x),
                                                            self.datax[-1]))
                elif self.datax and float(x) == self.datax[-1]:
                    print ('Warning: Data point time is the same '
                           'as previous ({} == {})'.format(float(x),
                                                           self.datax[-1]))
                else:

                    self.datax.append(float(x))
                    self.datay.append(float(y))

    def data_correct(self):
        """Return True if TIE (x,y) data is present and complete."""
        return (self.datax and self.datay
                and len(self.datax) == len(self.datay))

    def plot(self):
        """Plot stored data in a separate window using Matplotlib library."""
        fig = plt.figure()
        fig.canvas.set_window_title(self.name)
        ax = fig.add_axes((0.05, 0.1, 0.70, 0.85))
        plt.xlabel('Time [s]')
        plt.ylabel('TIE [s]')
        plt.grid(True)
        plt.plot(self.datax, self.datay)



        fig.text(.78, .9, self.infotext, fontsize=12, verticalalignment='top')

        plt.show()

    @property
    def infotext(self):
        attrs = ['Type', 'Start', 'Frequency', 'TimeMultiplier', 'Multiplier',
                 'Title', 'Adva Probe', 'Adva Reference',
                 'Adva Reference Expected QL', 'Adva Source',
                 'Adva Direction', 'Adva PTP Flow Point', 'Adva Master',
                 'Adva Slave', 'Adva IP Version', 'Adva MTIE Mask',
                 'Adva Mask Margin']
        text = ""
        for attr in attrs:
            text += "{}: {}\n".format(attr, self.info.get(attr))
        return text


# Read working path from configuartion file
try:
    with open(__cfgfile__, 'r') as cfgfile:
        def_dir = cfgfile.readline()
except IOError:
    def_dir = ''

# Initialize measurement object
measurement = Measurement()

# Open file selection dialog
tk = Tk()
tk.withdraw()
filenames = askopenfilenames(
    initialdir=def_dir,
    filetypes=[('Packed TIE data', '.txt.gz')]
)
# Close Tk window
tk.destroy()

if filenames:
    # dirty fix for Python 2.7.6 (bug!)
    # filenames = filenames.strip('{')
    # filenames = filenames.strip('}')
    # filenames = filenames.split("} {")
    filenames = list(filenames)
    filenames.sort()

    # Write current path to cfgfile
    with open(__cfgfile__, 'w') as cfgfile:
        cfgfile.write('{}\n'.format(os.path.dirname(filenames[0])))

    # Read the files and collect the data
    for filename in filenames:
        print filename
        try:
            f_data = gzip.open(filename, 'rb')
            measurement.add_data(f_data.readlines())
        except IOError:
            print 'Error opening file'
        f_data.close()

    # Plot the measurement data
    if measurement.data_correct():
        title = os.path.basename(filenames[0])
        title = os.path.splitext(title)[0]
        measurement.set_name(title)
        print measurement.infotext
        measurement.plot()
    else:
        raise ValueError('Incorrect data!')
