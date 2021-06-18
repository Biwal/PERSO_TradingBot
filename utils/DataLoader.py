import pandas as pd


class DataLoader:
    def __init__(self, filepath: str = "data/coin_Tether.csv") -> None:
        self._filepath = filepath
        self._raw_dataset = pd.read_csv(
            self._filepath, encoding="utf-8", index_col=3, parse_dates=True
        )

    def get_full_dataset(self) -> pd.DataFrame:
        dataset = self._process_raw_data()
        return dataset

    def get_train_test_dataset(self) -> pd.DataFrame:
        dataset = self._process_raw_data()

        train = dataset.query('("2020-10-01" > index >= "2016-12-23")').copy()
        test = dataset.query('("2022-01-01" > index >= "2020-10-01")').copy()
        print(train.head())
        return train, test

    def _process_raw_data(self) -> pd.DataFrame:
        dataset = self._raw_dataset.copy()
        # Suppression des lignes avec une valeure nulle
        # => Uniquement lignes de novembre et décembre 2020.
        dataset.dropna(axis=0, inplace=True)
        print(dataset.columns)
        dataset.drop(columns=['SNo','Name','Symbol','Marketcap'], inplace=True)

        for x in dataset.columns:
            dataset[x] = dataset[x].astype("Float32")
        return dataset