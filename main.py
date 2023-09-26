#!/usr/bin/env python
# -*- coding: utf-8 -*-

import altair as alt
import streamlit as st

import time
from ExtractData import ExtractData
from ProcessData import ProcessData
from SumString import SumString
from PlotData import PlotData
from Timeframe import Timeframe
from CreateJournal import CreateJournal

"""
# AnalyzeTrades v1.3

Author: Ari Esters

Last Modified: 25 Sept 2023
"""
    
# extract data
csvfile = st.file_uploader("Upload your transcations CSV file from your TD Ameritrade account :point_down:", type='csv')

if csvfile is not None:
    st.write(csvfile)
    if csvfile.type != 'csv': 
        st.write("This file is not a CSV file. Please upload a CSV file.")
    else:
        trades, filedir = ExtractData(csvfile)


'''
# check if data exists
if len(trades) == 0:
    print('\nERROR: Data does not exist. Transactions file may be empty.')
    return 0

# process data
dates, tickers, amounts, options, comms, fees, symbols, prices, signedQty = ProcessData(trades)

# Query and present data within retry mechanism
retry = 'Y'
while retry == 'Y':
    # user chooses timeframe
    start = Timeframe(dates)
    
    # isolate date from timeframe and plot
    d = dates[start:]
    #t = tickers[start:]
    #a = amounts[start:]
    o = options[start:]
    c = comms[start:]
    f = fees[start:]
    s = symbols[start:]
    p = prices[start:]
    q = signedQty[start:]
    
    # sum up commissions and fees
    commsum = SumString(c)
    feesum = SumString(f)

    # Write trade journal for all closed trades
    # STRUCTURE = [date open, date close, ticker, price open, price close, quantity, P/L, P/L %]
    closedpos = CreateJournal(d, s, p, q, o, commsum, feesum, filedir)
    
    # Plot data
    date1, date2, amountsum = PlotData(closedpos, filedir)
    
    # Summarize data
    grandsum = amountsum - commsum - feesum      
    print("\nSUMMARY (" + date1 + " - " + date2 + ")")
    print(line)
    print("Trade Profit-Loss (ignores P/L Open): ${:.2f}".format(amountsum))
    print("Total Commissions: ${:.2f}".format(commsum))
    print("Total Fees: ${:.2f}".format(feesum))
    print("Net Total: ${:.2f}".format(grandsum))
    print(line)
    print("Note: Only positions that were both opened and closed during this timeframe are counted.")
    
    # let user decide whether to retry
    validAns = False
    while validAns is False:
        print("\nPlots will be shown for this timeframe if you're done.")
        ans = input("---> Would you like to try a different timeframe? Enter here (Y/N): ")
        if (ans.upper() == 'Y') or (ans.upper() == 'YES'):
            validAns = True
            retry = 'Y'
            continue
        elif (ans.upper() == 'N') or (ans.upper() == 'NO'):
            validAns = True
            retry = 'N'
            print('Goodbye!')
            time.sleep(1)
        else:
            print('Answer not recognized. Please try again.')

'''
