import pandas as pd
from datetime import datetime
from pandas.tseries.offsets import MonthEnd

class PmsCleaner:

    def __init__(self, filepath):
        self.df = pd.read_csv(filepath)

    @staticmethod
    def change_month_format(month_name: str):
        return datetime.strptime(month_name, "%B").month

    @staticmethod
    def change_date_format(date):
        return datetime.strftime(date, '%Y/%m/%d')

    def reformat_data_csv(self):
        self.df['Month'] = self.df['Month'].apply(PmsCleaner.change_month_format)
        self.df['Date'] = pd.to_datetime(100*self.df['Year']+self.df['Month'], format='%Y%m') + MonthEnd(1)
        self.df.set_index('Date', inplace=True)
        self.df.drop(columns=['Unnamed: 0', 'Year', 'Month'], inplace=True)
        self.df['Date'] = self.df['Date'].apply(PmsCleaner.change_date_format)
        self.df.sort_index()
        return self.df

    def print_csv(self, filepath):
        self.df.to_csv(filepath)
