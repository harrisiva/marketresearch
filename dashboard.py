import streamlit as st
import pandas as pd
import numpy as np


df = pd.read_csv("data.csv").reset_index(drop=True)

# Add addition columns to the dataframe to simplify business use case
df['contacted'] = False # This column is to be convereted to a check box to provide user feature

st.title("Canadian Jiu-Jitsu Academies")
st.header("Dataframe of Canadian Jiu-Jitsu Academies")

st.data_editor(
    df,
    column_config={
        "contacted": st.column_config.CheckboxColumn(
            "Contacted?",
            default=False,
        )
    },
    disabled=True,
    hide_index=True,
)

st.caption("This dataframe was put together by using python's inbuilt request library to request HTML responses from Smoothcomp, a SaaS firm, and concat the collected data using Google Maps free API. The data is to be used for performing market research related to contacting BJJ academies for merchandise deals.")

st.divider()
df.dropna(inplace=True)


st.header("Map of Canadian Jiu-Jitsu Academies")
st.map(df,
    size=100,
    latitude='lat',
    longitude='lng')