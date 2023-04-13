import pandas as pd
import numpy as np
import os



class Record:
    def __init__(self,
                 class_: str,
                 date: str,
                 content: str,
                 is_correct: bool):
        self._class = class_
        if not isinstance(date, pd.Timestamp):
            date = pd.to_datetime(date)
        self._date = date
        self._content = content
        self._is_correct = is_correct

    def to_dict(self):
        """
        Transform a record as a dict.
        :return: a dict saved the information of a record
        """
        return {'Class': [self._class],
                'Date': [self._date],
                'Content': [self._content],
                'IsCorrect': [self._is_correct]}


    def save(self, path):
        """
        Save a new record to history data.
        :param path: history data path
        :return: None
        """
        columns = ['Class', 'Date', 'Content', 'IsCorrect']
        if os.path.exists(path):
            history_data = pd.read_csv(path)
        new_record = pd.DataFrame(data=self.to_dict())
        if os.path.exists(path):
            history_data = pd.concat([history_data, new_record],
                                     ignore_index=False)
            history_data.to_csv(path, index=False)
        else:
            new_record.to_csv(path, index=False)
        print(f'A new record has been saved to {path}.')

    @staticmethod
    def sort_by_wrong_time(data: pd.DataFrame) -> pd.DataFrame:
        """
        Sort history data by how many wrong time it has.
        :param data: history data as DataFrame
        :return: None
        """
        groups = data.groupby('Content', as_index=False)
        grouped_data = pd.DataFrame(columns=['Content', 'WrongTime'])
        for i, group in enumerate(groups):
            name, df = group
            grouped_data.loc[i, 'Content'] = name
            grouped_data.loc[i, 'WrongTime'] = len(df)
        sorted_data = grouped_data.sort_values(by='WrongTime', ascending=True)[::-1]
        sorted_data = sorted_data.reset_index()
        return sorted_data

    @staticmethod
    def get_callback_records(data: pd.DataFrame,
                             call_back: int) -> pd.DataFrame:
        """
        Get records user wants to review from history data.
        :param data: history data as DataFrame
        :param call_back: call back range
        :return: records user wants to review
        """
        assert 'Date' in data.columns
        ed = data['Date'].max()
        st = ed + pd.Timedelta(f'-{call_back}D')
        return data[(data['Date'] >= st) & (data['Date'] <= ed)]

    @staticmethod
    def get_contents(data: pd.DataFrame) -> list:
        """
        Get sentences or words from records.
        :param data: history data as DataFrame
        :return: sentences or words as Series or DataFrame
        """
        assert 'Content' in data.columns
        return data.loc[:, 'Content'].values
