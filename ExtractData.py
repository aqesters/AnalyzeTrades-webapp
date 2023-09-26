#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 22:07:44 2023

@author: aesters
"""

import re 
import csv
# Input:
    # 'file' == bytes object containing CSV file uploaded by user
# Returns:
    # 'trades' == raw trading data from input CSV file
    # 'filedir' == directory of the input CSV file
    
def ExtractData(file):
    
    # import data from file
    contents = csv.reader(file.splitlines())
    linenum = 1
    trades = []
    
    # iterate through each row
    for row in list(contents):
        if linenum == 1:  # first row has headers
            continue
        else:
            trades.append(row) # add row to list of trades
        linenum += 1
        
    # ignore last line, which says "END OF FILE"
    #trades.pop(-1)
    return list(contents)
