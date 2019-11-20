#!/usr/bin/env python3

import argparse
import re
from os.path import basename

class CmdlineParse():
    """ Command-line argument parser """

    def __init__(self, desc, ftype, help_msg):

        self._parser = argparse.ArgumentParser(description = desc)
        self._parser.add_argument('-i', '--input', metavar=ftype, help=help_msg,
                                type = self._file_validator, required = True, )
        self._parser.add_argument('-o', '--outpath',metavar='/path/to/out/dir',
                    type=str, help='Path to directory where subdir "parsed" '
                    'will be created and the parsed files put inside it')

        # Expose the command-line args as public properties of the class
        self.input = self._parser.parse_args().input
        self.outpath = self._parser.parse_args().outpath

    def _file_validator(self, full_in_fname):
        """ Validate file name and return itself if valid """
        # Regex check
        rex = re.compile('((2[0-1][0-9]{2}|19[0-9]{2})-(0[1-9]|1[0-2])\.xls)')
        if not rex.match(basename(full_in_fname)):
            raise argparse.ArgumentTypeError("must be in the form YYYY-MM.xls")
        else:
            return full_in_fname

if __name__ == "__main__":
    desc = "Parse data from <investment> file provided as <format>"
    ftype = "File type, e.g. yyyy-mm.xml"
    help_msg = ('File downloaded from <investment> website, must have the name '
                'provided as <name format>')
    cmdline = CmdlineParse(desc, ftype, help_msg)
    print("File name is: " + cmdline.input)
    try:
        print("Output path is: " + cmdline.outpath)
    except TypeError:
        print("Output path is wrong or not set")