import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import ingestion as io
import preprocess as pp

import boto3
from datetime import datetime


# Prepare data to be displayed
loader = io.DynamoDBLoader(
    table = 'LinkedInDSJobs',
    attributes = ['job_id','date','title','location']
)
raw_data = loader.get(datetime.today().strftime('%Y-%m-%d'))

# Prepare raw job postings for DS applications
preprocessor = pp.StandardPreprocessor()
data = preprocessor.fit_transform(raw_data)

# Introduction page
st.title('LinkedIn Job Postings for Data Science')
st.sidebar.markdown("# Introduction")

fig,ax = plt.subplots()
data.groupby('date').size().plot(ax=ax)
plt.xlabel('Number of jobs posted')
plt.ylabel('Date')
st.pyplot(fig)


