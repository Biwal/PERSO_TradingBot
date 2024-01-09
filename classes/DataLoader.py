import pandas as pd

class DataLoader:
    def __init__(self, filepath: str = 'data/eurusd_hour.csv') -> None:
        self._filepath = filepath
        self._dataset_raw = pd.read_csv(filepath_or_buffer=filepath, encoding='utf-8', parse_dates=['Date'])
        
    @property
    def dataset_raw(self):
        return self._dataset_raw
    
    @property
    def dataset_train_test(self):
        train = self._dataset_raw.query('("2005-01-01" <= Date < "2015-01-01")').copy()
        test = self._dataset_raw.query('("2015-01-01" <= Date < "2021-01-01")').copy()
        return train, test