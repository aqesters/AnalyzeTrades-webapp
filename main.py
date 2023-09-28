#!/usr/bin/env python
# -*- coding: utf-8 -*-

import altair as alt
import streamlit as st
import pandas as pd
import time
from ExtractData import ExtractData
from ProcessData import ProcessData
from SumString import SumString
from PlotData import PlotData
from Timeframe import Timeframe
from CreateJournal import CreateJournal

"""
# AnalyzeTrades v1.3

**For TD Ameritrade users**

*Author: Ari Esters*

*Last Modified: 25 Sept 2023*
"""
line = "-----------------------------------"
st.write(line)

# extract data
uploaded_file = st.file_uploader("Upload your transactions CSV file from your TD Ameritrade account :point_down:", type='csv')

if uploaded_file is not None:
    file_bytes = uploaded_file.getvalue().decode("utf-8")
    trades = ExtractData(file_bytes)

    # check if data exists
    if len(trades) == 0:
        st.error("Trading data does not exist. Transactions file may be empty.")
    
    # process data
    dates, tickers, amounts, options, comms, fees, symbols, prices, signedQty = ProcessData(trades)
    
    # user chooses timeframe
    all_days = (dates[-1] - dates[0]).days    # extract num days from datetime.timedelta obj
    st.write("\n" * 5)
    ndays = st.slider("Summarize trading performance over last __ days:", 1, all_days, 30)
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
    closedpos = CreateJournal(d, s, p, q, o, commsum, feesum)
    
    # Prep data for plotting
    date1, date2, amountsum, tickerNames, tickerPL, closeDates, trendingPL = PlotData(closedpos)
    tickerData = pd.concat([pd.DataFrame(tickerNames, columns=["Ticker"]), pd.DataFrame(tickerPL, columns=["P/L"])], axis=1)
    trendData = pd.concat([pd.DataFrame(closeDates, columns=["Close Date"]), pd.DataFrame(trendingPL, columns=["P/L"])], axis=1)

    ### Line chart for trending profit-loss data
    trendplot = alt.Chart(trendData).mark_line().encode(
        alt.X("Close Date:T"), 
        alt.Y("P/L:Q", axis=alt.Axis(format='$,.2f'))
    )
    
    # Create a selection for the nearest point
    nearest = alt.selection(type='single', nearest=True, on='mouseover', fields=['Close Date'], empty=False)
    
    # Add a transparent layer to capture mouseover events
    selectors = alt.Chart(trendData).mark_point().encode(
        x='Close Date:T',
        opacity=alt.value(0),
    ).add_selection(nearest)
    
    # Add the main line chart and enable tooltips for the nearest point
    points = trendplot.mark_point().encode(
        opacity=alt.condition(nearest, alt.value(1), alt.value(0)),
        tooltip=["Close Date:T", "P/L:Q"]  # Display x and y values in the tooltip
    )

    # Finally, combine the layers and plot line chart
    trendplot = trendplot + selectors + points
    st.altair_chart(trendplot, use_container_width=True, theme="streamlit")

    ### Bar chart for profit-loss by ticker
    tickplot = alt.Chart(tickerData).mark_bar().encode(
        alt.X("Ticker:N", sort="y"),
        alt.Y("P/L:Q", axis=alt.Axis(format='$,.2f'))
    )

    # Plot bar chart
    st.altair_chart(tickplot, use_container_width=True, theme="streamlit")
    
    # Summarize data
    grandsum = amountsum - commsum - feesum  
    st.write(line)
    st.write("## SUMMARY (", date1, " - ", date2, ")")
    st.write("Trade Profit-Loss (ignores P/L Open): ${:.2f}".format(amountsum))
    st.write("Total Commissions: ${:.2f}".format(commsum))
    st.write("Total Fees: ${:.2f}".format(feesum))
    st.write("Net Total: ${:.2f}".format(grandsum))
    st.write(line)
    st.write("Note: Only positions that were both opened and closed during this timeframe are counted.")
