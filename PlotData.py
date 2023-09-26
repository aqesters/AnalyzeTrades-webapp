#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 21:19:43 2023

@author: aesters
"""

# %% plot trading data
# - closedpos == 
# - filedir == 

import re
import matplotlib.pyplot as plt
import numpy as np 
from SumString import SumString
from matchsum import matchsum

def PlotData(closedpos, filedir):
    print("Plotting...")
    
    # isolate stock tickers and corresponding amounts
    tickers = []
    amounts = []
    trendpl = []
    closedates = []
    pltotal = 0
    i = 0
    stockPattern = r'^[A-Z]+$'
    optionPattern = r'^([A-Z]+)\s(\w+\s\w+\s\w+)\s.*\s(\w+)$'
    
    for trade in closedpos:    
        # if option, isolate stock ticker from this line
        ticker_raw = trade[2]
        matchStock = re.search(stockPattern, ticker_raw)
        matchOption = re.search(optionPattern, ticker_raw)
        if matchStock:
            ticker = ticker_raw
        elif matchOption:
            ticker = matchOption.group(1)  # isolate stock ticker 
        
        # append to tickers and amounts
        amount = trade[6][1:]  # exclude "$" at beginning       
        tickers.append(ticker)
        amounts.append(amount)     
        
        # collect first and last dates
        if i == 0:
            startdate = trade[0]
        enddate = trade[1]
        i += 1
        
        # update P/L list for trending plot
        pltotal += float(amount)
        trendpl.append(pltotal)
        closedate = trade[1]
        closedates.append(closedate)
    
    dt1 = startdate.strftime('%m/%d/%Y')
    dt2 = enddate.strftime('%m/%d/%Y')
    
    # BAR PLOT - setup 
    tickerSums = matchsum(tickers, amounts, sortkeys=False, sortvals=True)
    x, y = zip(*tickerSums)
    fig, ax = plt.subplots(figsize=(18,5))
    plt.bar(x,y)
    
    # BAR PLOT - configure grid/axes to make it more presentable
    ax.set_xticklabels(x, rotation='vertical')   
    
    tickstart = round(min(y)-500, -3)
    tickstop = round(max(y)+500, -3)
    markers = np.arange(tickstart, tickstop, 500)
    plt.yticks(markers)
    
    plt.grid(axis='y')
    plt.ylabel('Trading Profit/Loss ($)')
    plt.title('P/L by ticker ({} - {})'.format(dt1, dt2))
    plotname = filedir + 'TickerPL.png'
    plt.savefig(plotname)
    print('\nPlot saved to {}'.format(plotname))
    
    # P/L TREND PLOT - set up
    closedPL = matchsum(closedates, amounts, sortkeys=True, sortvals=False)
    x2, ytemp = zip(*closedPL)
    totalPL = 0
    y2 = []
    for PL in ytemp:
        totalPL += PL
        y2.append(totalPL)
    fig, ax = plt.subplots()
    plt.plot(x2,y2)
    
    # P/L TREND PLOT - make it presentable   
    plt.xticks(rotation=60)
    tickstart = round(min(y2)-500, -3)
    tickstop = round(max(y2)+500, -3)
    markers = np.arange(tickstart, tickstop, 500)
    plt.yticks(markers)
    
    plt.grid(axis='y')
    plt.ylabel('Total Profit/Loss ($)')
    
    plt.title('P/L over time ({} - {})'.format(dt1, dt2))
    plotname = filedir + 'TimePL.png'
    plt.savefig(plotname)
    print('\nPlot saved to {}'.format(plotname))
    
    amountsum = SumString(amounts)
    return dt1, dt2, amountsum  # return start and end dates 