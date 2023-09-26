#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 22:20:17 2023

@author: aesters
"""

import datetime as dt
import re

# Processing raw trading data and returning multiple lists with identical lengths
# each index corresponds to a trade

def ProcessData(trades):
    print("Processing trade data...")
    # add IDs for each field
    dateID = 0
    #descriptionID = 2
    quantityID = 3
    symbolID = 4
    priceID = 5
    commissionID = 6
    amountID = 7
    feeID = 8
    
    # extract relevant info from transactions file
    dates = []
    symbols = []
    amounts = []
    options = []
    comms = []
    fees = []
    quantities = []
    tickers = []
    #expired = []
    signedQty = []
    prices = []
    #expdates = []
    
    # save earliest and latest dates in raw data for reference
    firstdate = trades[0][dateID]
    lastdate = trades[-1][dateID]
    #lastdt = dt.datetime.strptime(lastdate, '%m/%d/%Y')
    
    # set up regex patterns for distinguishing stocks and options
    stockPattern = r'^[A-Z]+$'
    optionPattern = r'^([A-Z]+)\s(\w+\s\w+\s\w+)\s.*\s(\w+)$'
    
    # iterate through each row of raw data
    for i in range(len(trades)):
        date = trades[i][dateID]
        sym = trades[i][symbolID]
        amt = trades[i][amountID]
        comm = trades[i][commissionID]
        fee = trades[i][feeID]
        qty = trades[i][quantityID]
        price = trades[i][priceID]
        
        if sym != '':  # add entry only if it's a real trade
            
            matchStock = re.search(stockPattern, sym)
            matchOption = re.search(optionPattern, sym)
            
            if matchStock:  # this is a stock trade
                ticker = matchStock.group(0)
                opt = ''
                exp = ''
            
            elif matchOption:  # this is an option trade
                ticker = matchOption.group(1)
                opt = matchOption.group(3)
                
            else:  # skip if unidentified
                continue
            
            if float(amt) <= 0:  # trade is a BUY
                signedQty.append(qty)                    
            elif float(amt) > 0:  # trade is a SELL --> make quantity negative
                signedQty.append('-' + qty)
            
            # convert date into datetime object for easy processing
            dateobj = dt.datetime.strptime(date, '%m/%d/%Y').date()
            
            # update all lists (contain numeric strings, unless otherwise stated)
            dates.append(dateobj)  # datetime objects
            symbols.append(sym)  # alphabet strings
            amounts.append(amt)
            options.append(opt)  # alphabet strings (CALL/PUT)
            comms.append(comm)
            fees.append(fee)
            quantities.append(qty)
            # expired.append(exp)  # booleans
            tickers.append(ticker)  # alphabet strings
            prices.append(price)
            
    
    print("Transaction data ranges from {} to {}".format(firstdate, lastdate))            
    return dates, tickers, amounts, options, comms, fees, symbols, prices, signedQty