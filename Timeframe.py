#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 22:25:27 2023

@author: aesters
"""
import datetime as dt

# Inputs: 
    # dates == contains datetime objects arranged in ascending order
    # N == user input, the script will summarize data over the last N days
# Returns: starting index corresponding to the last N days

def Timeframe(dates, N):    
    # find index that matches desired timeframe
    delta = dt.timedelta(N)
    lastdate = dates[-1]
    startdate = lastdate - delta
    for i in range(len(dates)):
        if dates[i] >= startdate:
            break
    return i
