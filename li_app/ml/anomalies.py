import streamlit as st

import pandas as pd

@st.cache
def find_anomalies(
    ts: pd.Series,
    insample: pd.DataFrame):
    '''
    Take insample forecasts at the given level, and flag values in the time 
    series that exceed the level.

    Since all of the complexity is handled during the model training,
    there is no need to create a class structure for this operation.

    '''
    # TODO: instead taking first element, use sensitivity variable
    high_thresh_column = [c for c in insample.columns if 'hi-' in c][-1] #column name changes depending on the model
    is_anomaly = ts > insample.set_index('ds')[high_thresh_column]

    # TODO: if today is an anomaly, send a mail

    return is_anomaly