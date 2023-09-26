from collections import namedtuple
import altair as alt
import pandas as pd
import streamlit as st

"""
# AnalyzeTrades v1.3

Author: Ari Esters
Last Modified: 25 Sept 2023
"""

with st.echo(code_location='below'):
    n_days = st.slider("Analyze data over last __ days:", 1, 365, 30)

    Point = namedtuple('Point', 'x y')
    data = []

    points_per_turn = total_points / num_turns

    #st.altair_chart(alt.Chart(pd.DataFrame(data), height=500, width=500)
     #   .mark_circle(color='#0068c9', opacity=0.5)
      #  .encode(x='x:Q', y='y:Q'))
