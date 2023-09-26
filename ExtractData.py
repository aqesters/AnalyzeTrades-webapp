#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 22:07:44 2023

@author: aesters
"""

import re 
import csv

# Input:
    # 'filepath' == path to transactions CSV file uploaded by user
# Returns:
    # 'trades' == raw trading data from input CSV file
    # 'filedir' == directory of the input CSV file
    
def ExtractData(file):
    '''
    # get the directory for this file, save data here later
    parts = re.split('/', filepath)
    i = -1 * len(parts[-1])  # index right before filename
    filedir = filepath[:i]
    '''
    
    # import data from file
    print("Extracting...")
    with open(file, newline='') as csvfile:
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
    return trades
