#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 22:31:34 2023

@author: aesters
"""
import re
import datetime as dt
import csv

# Creates trade journal (as CSV file) that shows close date, P/L %, and other 
# values for each closed position 

# Notes:
#   Only use date from timeframe selected by user (see Timeframe function)
#   Inputs should already be sorted by the dates (datetime objects)

def CreateJournal(dates, symbols, prices, signedQty, options, commsum, feesum, filedir):
    print("Creating trade journal...")
    startdate = dates[0]
    enddate = dates[-1]  
    
    # separate transactions into buy and sell orders
    buys = []
    sells = []  
    
    for i in range(len(signedQty)):      
        date = dates[i]
        sym = symbols[i]
        price = prices[i]
        sqty = signedQty[i]
        opt = options[i]
        # exp = expired[i]
        # if exp == True:
        #     price = 0  # expired options are worthless
        #     sqty = -1*sqty  # treat as a SELL
            
        transaction = [date, sym, price, sqty, opt]
        if float(sqty) > 0:  # this is a BUY order
            buys.append(transaction)
        elif float(sqty) < 0:  # this is a SELL order
            sells.append(transaction)
        else:
            continue
    
    # iterate thru buy orders and find corresponding sell orders
    trades = []
    openpos = []
    pl_sum = 0  # initialize total P/L
    for buy in buys:
        b_date = buy[0]
        b_sym = buy[1]
        if buy[2] == '' or buy[3] == '':  # skip meaningless line
            continue
        else:
            b_price = float(buy[2])
            b_qty = int(buy[3])
        b_opt = buy[4]
        
        j = 0  # reset index for SELLS
        remainder = b_qty  # number of shares remaining
        # using indices for this loop since SELL list is edited during loop
        while True:
            try:  # do this if index is still in range
                s_date = sells[j][0]
                s_sym = sells[j][1]
                if sells[j][2] == '' or sells[j][3] == '':  # skip meaningless line
                    j += 1
                    continue
                else: 
                    s_price = float(sells[j][2])
                    s_qty = abs(int(sells[j][3]))
            except IndexError:  # break if index out of range
                break
            
            if s_sym != b_sym:  # skip this case
                j += 1
                continue
            else:  # ticker matches
                remainder_prev = remainder
                remainder = remainder - s_qty 
                
                # if sells > buys
                if remainder < 0: 
                    qty = remainder_prev  # transaction is limited by shares owned
                    sells[j][3] = str(s_qty - remainder_prev)  # keep track of remaining shares to be sold 
                # if buys >= sells
                elif remainder >= 0:
                    qty = s_qty  # all shares sold
                    sells.pop(j)
                    
                # calculate P/L and P/L %
                if b_opt != '':  # this is an option trade
                    factor = 100
                else:  # not an option trade
                    factor = 1  
                
                pl_float = (s_price - b_price) * qty * factor
                pl_perc_float = (s_price - b_price)/b_price * 100
                pl_sum += pl_float  # keep track of total
                
                pl = "${:.2f}".format(pl_float)
                pl_perc = "{:.1f}%".format(pl_perc_float)
                
                # add data to list of closed trades
                trade = [b_date, s_date, s_sym, b_price, s_price, qty, pl, pl_perc]  
                trades.append(trade)          
                if remainder <= 0:
                    break  # ignore rest of SELLs for this BUY order
                
        # identify any unresolved positions that are still open
        if remainder > 0:            
            # check for expired options
            stockPattern = r'^[A-Z]+$'
            optionPattern = r'^([A-Z]+)\s(\w+\s\w+\s\w+)\s.*\s(\w+)$'
            matchStock = re.search(stockPattern, b_sym)
            matchOption = re.search(optionPattern, b_sym)          
            
            if matchStock:  # this is a stock trade
                ticker = matchStock.group(0)
                opt = ''
                exp = ''  
            elif matchOption:  # this is an option trade
                ticker = matchOption.group(1)
                expdate = matchOption.group(2)
                opt = matchOption.group(3)               
                
                # check if option is expired
                expdt = dt.datetime.strptime(expdate, '%b %d %Y').date()
                if expdt < enddate:  # option has expired
                    exp = True
                else:  # option not yet expired
                    exp = False
                
                if exp: # expired option --> position is worthless
                    s_price = 0
                    factor = 100
                    pl_float = (s_price - b_price) * remainder * factor
                    pl_perc_float = (s_price - b_price)/b_price * 100
                    pl_sum += pl_float
                   
                    # format and append to list
                    pl = "${:.2f}".format(pl_float)
                    pl_perc = "{:.1f}%".format(pl_perc_float)
                    trade = [b_date, expdt, b_sym, b_price, s_price, remainder, pl, pl_perc]
                    trades.append(trade)
                # otherwise, this must be an open position   
                else:  
                    pos = [b_date, '', b_sym, b_price, '', b_qty, '', '']
                    openpos.append(pos)
    
    # create filename, header, and summary lines
    date1 = startdate.strftime('%Y%m%d')
    date2 = enddate.strftime('%Y%m%d')
    filename = filedir + "TradeJournal_" + date1 + "_" + date2 + ".csv"
    header = ['Date Open', 'Date Close', 'Ticker', 'Price Open', 'Price Close', 'Quantity', 'P/L', 'P/L %']
    plline = ['', '', 'Net Profit-Loss', '', '', '', '${:.2f}'.format(pl_sum), '']
    commline = ['', '', 'Total Commissions', '', '', '', '${:.2f}'.format(commsum), '']
    feeline = ['', '', 'Total Fees', '', '', '', '${:.2f}'.format(feesum), '']
    grandsum = pl_sum - commsum - feesum
    totalline = ['', '', 'GRAND TOTAL', '', '', '', '${:.2f}'.format(grandsum), '']
    summary = [plline, commline, feeline, totalline]
    
    # write to .csv file
    with open(filename, 'w', newline='') as journal:
        writer = csv.writer(journal, delimiter=',')
        writer.writerow(header)
        # write open positions in reverse order (most recent first)
        for line in openpos[::-1]:
            writer.writerow(line)
        # write closed positions in reverse order (most recent first)
        for line in trades[::-1]:
            writer.writerow(line)
        # write summary lines
        for line in summary:
            writer.writerow(line)
            
    print("Trade journal complete! --> Saved as \'{}\'\n".format(filename))
    return trades