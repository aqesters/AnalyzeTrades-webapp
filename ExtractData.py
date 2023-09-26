#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 22:07:44 2023

@author: aesters
"""

import tkinter as tk
from tkinter import filedialog
import re 
import csv

# import trade data from .csv file downloaded from TD Ameritrade
# Returns:
    # 'trades' == raw trading data from input CSV file
    # 'filedir' == directory of the input CSV file
    
def ExtractData():
    print("---> Open the transactions CSV file through the pop-up.\n")
    # select .csv file through dialog box
    root = tk.Tk()   # instantiates and creates top-level window
    root.withdraw()  # hide root window
    filepath = filedialog.askopenfilename(initialdir='./')
    root.destroy()
    
    # get the directory for this file, save data here later
    parts = re.split('/', filepath)
    i = -1 * len(parts[-1])  # index right before filename
    filedir = filepath[:i]
    
    # import data from file
    print("Extracting...")
    with open(filepath, newline='') as csvfile:
        contents = csv.reader(csvfile, delimiter=',')
        linenum = 1
        headers = []
        trades = []
        # iterate through each row
        for row in contents:
            if linenum == 1:  # first row has headers
                headers = row
            else:
                trades.append(row) # add row to list of trades
            linenum += 1
        # ignore last line, which says "END OF FILE"
        trades.pop(-1)

    print("Extraction complete!")    
    return trades, filedir