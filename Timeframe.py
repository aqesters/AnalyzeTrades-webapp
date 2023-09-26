#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 22:25:27 2023

@author: aesters
"""
import datetime as dt

# Input: 
    # "dates" input contains datetime objects arranged in ascending order
    # user input: to sum up over the last __ days
# Returns: starting index corresponding to the last __ days

def Timeframe(dates):
    # get user input for number of days
    allowed = False
    err = "ERROR: Number of days must be a whole number greater than zero (1,2,3...)"
    pastdays = input("---> Sum up trades over the last how many days? Enter here: ")
    while allowed == False:
        try:
            pastdays = int(pastdays)
            allowed = (pastdays >= 1)
        except ValueError or TypeError:  # input is not a number
            print(err)
            pastdays = input("---> Sum up trades over the last how many days? Enter here: ")
            continue
        if allowed == False:  # input is zero or negative number
            print(err)
            pastdays = input("---> Sum up trades over the last how many days? Enter here: ")
    
    # find index that matches desired timeframe
    delta = dt.timedelta(pastdays)
    lastdate = dates[-1]
    startdate = lastdate - delta
    for i in range(len(dates)):
        if dates[i] >= startdate:
            break
    return i