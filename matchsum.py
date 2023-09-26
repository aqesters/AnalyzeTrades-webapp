#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 21:43:11 2023

@author: aesters
"""

# sum up identically labeled values and return a pair of lists in sorted key-value format
# Inputs:
    # keys == list of labels, nums with the same label will be summed
    # nums == list of int or float that will be summed based on their labels
# Returns: a list of paired elements, where each paired element contains a unique
# label and the sum of all values that had that label
    
def matchsum(keys, nums, sortkeys=False, sortvals=False):
    length = len(keys)
    if length != len(nums):
        print('ERROR: Input list arguments for \"matchsum\" function must be of equal length. Returning zero.')
        return 0
    else:
        dic = {}
        for i in range(length):
            key = keys[i]
            num = float(nums[i])
            try:  # if key already exists in dictionary, add new value to old value
                dic[key] += num
            except KeyError:  # if key does not exist, create new key
                dic[key] = num
        # either sort and return the dict, or return as is
        if sortkeys is True:  # attempt to sort the keys (e.g., ticker symbols)
            sortedList = [ [i, dic[i]] for i in sorted(dic) ]
            return sortedList
        elif sortvals is True:  # arrange by amount
            swapdic = { dic[i]: i for i in dic}
            sortedList = [[swapdic[i], i] for i in sorted(swapdic) ]
            return sortedList
        else:
            unsortedList = [ [i,  dic[i]] for i in dic ]
            return unsortedList