#!/usr/bin/env python3

import pandas as pd
import os

class TesouroDireto():
    """ Class to handle exported files from Tesouro Direto"""

    def __init__(self):
        pass


    def _parse_in_filename(self, fname):
        """ Extract data from the input filename """
        self._full_in_fname = fname
        self._in_fpath = os.path.dirname(fname)
        self._in_basename = os.path.basename(fname)
        self._yyyy = self._in_basename.split("-")[0]
        self._mm = self._in_basename.split("-")[1].split(".")[0]
        if self._in_basename.split("-")[1].split(".")[1] != "xls":
            raise ValueError("Filename extension is different from .xls")


    def _gen_out_filename(self, full_out_fpath, extension):
        """ Generate output filename, including full path
            Must be called after """

        # Path to output file
        try:
            self._out_fpath = os.path.join(full_out_fpath)
        except TypeError:
            self._out_fpath = self._in_fpath

        # Create "parsed" directory inside path to output file
        try:
            os.mkdir(os.path.join(self._out_fpath, 'parsed'))
        except FileExistsError:
            pass # Do nothing if path already exists

        # Generate output filename from input filename and extension
        self._out_fname = os.path.join( self._out_fpath, 'parsed',
                                        self._in_basename.split(".")[0] +
                                        "." + extension)


    def _parse_in_contents(self):
        """ Parse the gross value for an exported file from Tesouro Direto
            with a single treasury fund. If more than one treasury fund is
            present, the parsing might silently fail. """
        try:
            # Only works for a very specific use case
            dfs = pd.read_html(self._full_in_fname, skiprows=1)
            investment = dfs[0].iloc[0 , 0]
            grossval = dfs[0].iloc[2 , 3]/100
        except FileNotFoundError as e:
            print("Input file error: " + repr(e))
        else:
            self._parsed_df = pd.DataFrame(
                {'year': [self._yyyy], 'month': [self._mm], 'gross-value': [grossval],
                'investment': [investment]})
            print(self._parsed_df)


    def _preprocess(self, fname, full_out_fpath, extension="csv"):
        """ Join all preprocessing functions into a single call """
        self._parse_in_filename(fname)
        self._gen_out_filename(full_out_fpath, extension)
        self._parse_in_contents()

    def to_csv(self, fname, full_out_fpath=None):
        """ Save parsed data as csv. If full_out_fpath dir is provided, save the csv
            in <full_out_fpath/parsed>, otherwise use <input file path/parsed>"""
        #Create DataFrame to save as csv
        self._preprocess(fname, full_out_fpath, "csv")

        # Save dataframe as csv
        self._parsed_df.to_csv(self._out_fname, index=False)


if __name__ == "__main__":
    from spinparse.common.cmdline_parse import CmdlineParse

    # Parse input filename
    desc = "Parse data from tesouro direto XLS file"
    ftype = "<yyyy-mm>.xls"
    help_msg = ('File downloaded from the Tesouro Direto website, must have '
                'the name provided as <year-month>.xls')
    args = CmdlineParse(desc, ftype, help_msg)

    # Generate csv file
    td = TesouroDireto()
    td.to_csv(args.input, args.outpath)