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
uploaded_file = st.file_uploader("Upload your transcations CSV file from your TD Ameritrade account :point_down:", type='csv')

if uploaded_file is not None:
    file_bytes = uploaded_file.getvalue().decode("utf-8")
    trades = ExtractData(file_bytes)
    st.write(len(trades))
    st.write(trades)

    # check if data exists
    if len(trades) == 0:
        st.error("Trading data does not exist. Transactions file may be empty.")
    
    # process data
    dates, tickers, amounts, options, comms, fees, symbols, prices, signedQty = ProcessData(trades)
    
    # user chooses timeframe
    all_days = dates[-1] - dates[0]
    ndays = st.slider(1, int(all_days), 30)
    start = Timeframe(dates, ndays)
    
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
    #date1, date2, amountsum = PlotData(closedpos, filedir)
    
    # Summarize data
    grandsum = amountsum - commsum - feesum  
    line = "-----------------------------------"
    st.write("SUMMARY (", date1, " - ", date2, ")")
    st.write(line)
    st.write("Trade Profit-Loss (ignores P/L Open): ${:.2f}".format(amountsum))
    st.write("Total Commissions: ${:.2f}".format(commsum))
    st.write("Total Fees: ${:.2f}".format(feesum))
    st.write("Net Total: ${:.2f}".format(grandsum))
    st.write(line)
    st.write("Note: Only positions that were both opened and closed during this timeframe are counted.")
