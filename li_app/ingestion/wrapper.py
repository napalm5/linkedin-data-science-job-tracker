import streamlit as st

from ingestion.dynamodb import DynamoDBLoader

from datetime import datetime

@st.cache
def loader_caching_wrapper(date: str,source='dynamodb'):
    '''
    Wrapper method to allow for the caching of class methods.
    This should probably be achieved through some sort of factory method,
    because this does not provide an easily extendable interface.

    By setting "date" as an argument, I make sure that the app downloads
    new date once every day/week/..,, depending on what is passed
    '''
    loader = DynamoDBLoader(
        table = 'LinkedInDSJobs',
        attributes = ['job_id','date','title','location']
    )
    raw_data = loader.get()
    return raw_data

