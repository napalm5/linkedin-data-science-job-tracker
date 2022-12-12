import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import ingestion as io
import preprocess as pp
import ml as ml

import boto3
from datetime import datetime


# Prepare data to be displayed
raw_data = io.loader_caching_wrapper(date=datetime.today().strftime('%m-%d-%Y'))

# Prepare raw job postings for DS applications
data = pp.pp_caching_wrapper(raw_data)
ts = data.groupby('date').size()

# Model the job posting time series
forecast_results = ml.train_caching_wrapper(ts)

# Save variables for reuse between pages
st.session_state['raw_data'] = raw_data
st.session_state['data'] = data
st.session_state['ts'] = ts
st.session_state['forecast_results'] = forecast_results


# Introduction page
st.title('LinkedIn Job Postings for Data Science')
st.sidebar.markdown("# Introduction")

st.markdown(
    """
    Hi! This is an application to monitor the latest trands in the data science job market, for profiles similar to mine.

    Here you can see a plot of the number of job offers posted every day for the past few weeks.
    An anomaly detection algorithm runs in the backend and raises an alarm whenever the number of job offers starts to spike. The anomalies are marked by a vertical red line on the plot.

    Be sure to reach out to me before the next peak! 😉  

    Please be aware that this project has just started and it's a work in progress, so be sure to come back in a couple of weeks to see a better analysis. 
    
    In particular, I am currently fixing some issues in the scraping process, so the time series you are seeing are at the moment might not be reliable. 

    """
)

# Run anomaly detection algorithm and plot results
is_anomaly = ml.find_anomalies(ts, forecast_results.insample)

# TODO: put this in a function, or class of functions
fig,ax = plt.subplots()
ax.scatter(ts.index,ts.values) # Main time series
#ax.fill_between(ts.index,ts.values,alpha=0.5)
ts.plot(ax=ax,linewidth=0.2,linestyle='-')# Interpolation
for i in ts.index[is_anomaly]:# Anomalies
    ax.axvline(i, color='r', linestyle='--') 
plt.ylabel('Number of jobs posted')
plt.xlabel('Date')
plt.xticks(rotation=45)
st.pyplot(fig)

'''
# What's behind this?
'''
st.image('./assets/stack.png')
'''
The data analysis process is described in the [Methodology](Methodology) section.

The technical architecture is described in  [Technical description](Technical_description) section.

Or you can take a [look at the code for yourself](https://gitlab.com/napalm5/linkedin-data-science-job-tracker)!
'''

