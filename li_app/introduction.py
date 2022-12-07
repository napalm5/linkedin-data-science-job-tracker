import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import ingestion as io
import preprocess as pp

import boto3
from datetime import datetime


# Prepare data to be displayed
raw_data = io.loader_caching_wrapper(datetime.today().strftime('%m-%d-%Y'))

# Prepare raw job postings for DS applications
data = pp.pp_caching_wrapper(raw_data)

# Save state for reference between pages
st.session_state['raw_data'] = raw_data
st.session_state['data'] = data

# Introduction page
st.title('LinkedIn Job Postings for Data Science')
st.sidebar.markdown("# Introduction")

st.markdown(
    """
    Hi! This is an application to monitor the data science job market for a profile similar to mine.

    """
)
fig,ax = plt.subplots()
data.groupby('date').size().plot(ax=ax)
plt.xlabel('Number of jobs posted')
plt.ylabel('Date')
st.pyplot(fig)

st.markdown(
    """
    # What's behind this?
    You can find all the details in 

    Or you can directly take a [look at the code](https://gitlab.com/napalm5/linkedin-data-science-job-tracker)!
    
    """
)

