import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import boto3
from datetime import datetime
st.title('LinkedIn Job Postings for Data Science')

@st.cache
def load_unstructured(date):
    db = boto3.resource('dynamodb')
    table = db.Table('LinkedInDSJobs')

    def scanRecursive(dbTable, **kwargs):
        """
        NOTE: Anytime you are filtering by a specific equivalency attribute such as id, name 
        or date equal to ... etc., you should consider using a query not scan

        kwargs are any parameters you want to pass to the scan operation
        """
        response = dbTable.scan(**kwargs)
        if kwargs.get('Select')=="COUNT":
            return response.get('Count')
        data = response.get('Items')
        while 'LastEvaluatedKey' in response:
            response = kwargs.get('table').scan(ExclusiveStartKey=response['LastEvaluatedKey'], **kwargs)
            data.extend(response['Items'])
        return data

    data = scanRecursive(
        dbTable=table,
        Select='SPECIFIC_ATTRIBUTES',
        AttributesToGet=[
            'job_id','date','title','company'
        ])
    return data

data = load_unstructured(datetime.today())
df = pd.DataFrame(data)    
df['date'] = pd.to_datetime(df.date)

fig,ax = plt.subplots()
df.groupby('date').size().plot(ax=ax)
plt.ylabel('Number of jobs posted')
plt.xlabel('Date')
st.pyplot(fig)
st.dataframe(df)
