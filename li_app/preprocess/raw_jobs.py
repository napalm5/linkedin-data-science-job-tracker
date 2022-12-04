from abc import ABC, abstractmethod

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

class StandardPreprocessor(PreprocessJobs):
    def __init__(self):
        pass

    def fit(self, raw_data):
        pass
        
    def transform(self, raw_data):
        # Format dates
        data = raw_data
        data['date'] = pd.to_datetime(data.date)
        data['date'] = data.date\
            .fillna(method='ffill')\
            .fillna(method='bfill')

        return data

