#!/usr/bin/env python3

import pandas as pd
import argparse
import os

# Parse input and output filenames
parser = argparse.ArgumentParser(description = 'Parse data from tesouro direto'
                                               'XLS file.')
parser.add_argument('-i', '--input', metavar='<yyyy-mm>.xls', type=str,
                    required = True, help='File downloaded from the Tesouro '
                    'Direto website. Must have the name provided as year-month')
args = parser.parse_args()

try:
    # Only works for a very specific use case
    dfs = pd.read_html(args.input, skiprows=3)
    grossval = dfs[0].iloc[0 , 3]/100
except FileNotFoundError as e:
    print("Input file error: " + repr(e))
else:
    # Save to csv
    fname = os.path.split(args.input)[1]
    fpath = os.path.split(args.input)[0]
    yyyy = fname.split("-")[0]
    mm = fname.split("-")[1].split(".")[0]
    
    # Create DataFrame to save as csv
    try:
        os.mkdir(os.path.join(fpath, 'parsed'))
    except FileExistsError:
        pass # Do nothing if path already exists

    data2csv = pd.DataFrame({'year': [yyyy], 'month': [mm], 'gross-value': [grossval]})
    print(data2csv)
    data2csv.to_csv(os.path.join(fpath, 'parsed', fname.split(".")[0] + ".csv"), index=False)