#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 21:40:08 2023

@author: aesters
"""

# input: a list of numbers as strings (List of str)
# output: the sum of the numbers (float)
    
def SumString(strlist):
    total = 0
    for i in strlist:
        if i == '':
            continue
        else:
            total += float(i)
    return total