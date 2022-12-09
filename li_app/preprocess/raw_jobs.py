from abc import ABC, abstractmethod

import streamlit as st

import numpy as np
import pandas as pd

class PreprocessJobs(ABC):
    @abstractmethod
    def fit(self, data: pd.DataFrame):
        pass

    @abstractmethod
    def transform(self, raw_data: pd.DataFrame) -> pd.DataFrame:
        pass

    def fit_transform(self, raw_data: pd.DataFrame) -> pd.DataFrame:
        self.fit(raw_data)
        data = self.transform(raw_data)

        return data


@st.cache
def pp_caching_wrapper(raw_data,method='default'):
    '''
    Wrapper method to allow for the caching of class methods.
    This should probably be achieved through some sort of factory method,
    because this is not easily extensible to multiple PP methods.
    '''
    preprocessor = StandardPreprocessor()
    data = preprocessor.fit_transform(raw_data)

    return data




class StandardPreprocessor(PreprocessJobs):
    def __init__(self):
        self.countries = ['Italy', 'DACH', 'Germany', 'Austria', 'Switzerland'] #which countries to consider

    def fit(self, raw_data):
        pass
        
    def transform(self, raw_data):
        data = raw_data

        # Adapt format from DynamoDB output
        data = data.replace({'' : np.nan})

        # Only keep countries of interest
        data = data[data.location.isin(self.countries)]
        # Format dates
        data['date'] = pd.to_datetime(data.date)

        # Many jobs do not have a date, but since they are scraped in chronological order this is a good approximation 
        # data['date'] = data.date\
        #     .fillna(method='ffill')\
        #     .fillna(method='bfill')
        # But in the end analysis is better if I drop NAs
        data = data.dropna()

        return data

