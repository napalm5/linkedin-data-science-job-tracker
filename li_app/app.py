import streamlit as st
import pandas as pd
import numpy as np

import ingestion as io
import preprocess as pp

import boto3
from datetime import datetime
st.title('LinkedIn Job Postings for Data Science')

loader = io.DynamoDBLoader(
    table = 'LinkedInDSJobs',
    attributes = ['job_id','date','title']
)
raw_data = loader.get(datetime.today())

# Prepare raw job postings for DS applications
preprocessor = pp.StandardPreprocessor()
data = preprocessor.fit_transform(data)


## Divide plots into pages
fig,ax = plt.subplots()
data.groupby('date').size().plot(ax=ax)
plt.xlabel('Number of jobs posted')
plt.ylabel('Date')
st.pyplot(fig)

