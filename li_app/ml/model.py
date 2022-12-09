import streamlit as st

import pandas as pd
from statsforecast import StatsForecast
from statsforecast.models import RandomWalkWithDrift

from collections import namedtuple
TSTrainingResults = namedtuple("TSTrainingResults", "model forecast insample")



@st.cache
def train_caching_wrapper(
    ts: pd.Series,
    forecast_interval: int = 7,
    ad_sensitivity: int = 90
    ):
    '''
    Wrapper method to allow for the caching of class methods.
    This wrapper has a very limited interface, but I do not plan on extending
    the forecast functionalities, or to use different libraries, so in the near
    future it won't need a refactoring.

    # TODO: add checks on input values (sensitivity should be between 0 and 100)

    statsforecast has a similar interface to statsmodels. So for convenience
    I do training, forecasting and insample forecasting here in the same function.
    '''

    train_data = ts.reset_index()
    train_data.columns = ['ds','y']
    train_data['unique_id'] = 1
    levels = [ad_sensitivity]

    models = [RandomWalkWithDrift()]
    model = StatsForecast(
        df=train_data, 
        models=models, 
        freq='D',
        n_jobs=-1,
    )
    forecast = model.forecast(h=forecast_interval, level=levels, fitted=True)
    insample = model.forecast_fitted_values()

    results = TSTrainingResults(
        model = model,
        forecast = forecast,
        insample = insample
    )
    return results