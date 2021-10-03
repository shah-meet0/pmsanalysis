import pandas as pd
from datetime import datetime
from pandas.tseries.offsets import MonthEnd


# Needs documentation
class PmsCleaner:

    def __init__(self, filepath):
        self.df = pd.read_csv(filepath)
        self.df['Date'] = pd.to_datetime(self.df['Date'], format='%Y-%m-%d')
        self.df.set_index('Date', inplace= True)

    def get_relevant_managers(self, year, entries):
        managers = self.df['Manager Name'].unique()
        for manager in managers:
            manager_entries = self.df[self.df['Manager Name'] == manager]
            if manager_entries.shape[0] < entries or manager_entries.last_valid_index().year < year:
                self.df = self.df[self.df['Manager Name'] != manager]

    def remove_abnormal_returns(self, return_threshold, sensitivity):
        abnormal_returns = self.df[abs(self.df['Return']) >= return_threshold]
        abnormal_managers = abnormal_returns['Manager Name'].unique()
        for manager in abnormal_managers:
            number_entries = len(abnormal_returns[abnormal_returns['Manager Name'] == manager])
            if number_entries > sensitivity:
                self.df = self.df[self.df['Manager Name'] != manager]

    def find_missing_dates(self, start_year, start_month, end_year, end_month):
        pass

    def attach_index_return(self, index_returns_path):
        pd.read_csv(index_returns_path)
        pass

    def print_csv(self, filepath):
        self.df.to_csv(filepath)


class PmsReformater:

    def __init__(self, filepath):
        self.df = pd.read_csv(filepath)

    @staticmethod
    def change_month_format(month_name: str):
        return datetime.strptime(month_name, "%B").month

    @staticmethod
    def change_date_format(date):
        return datetime.strftime(date, '%Y-%m-%d')

    def change_data_format(self, date_format):
        self.df['Date'] = pd.to_datetime(self.df['Date'], format=date_format)
        self.df['Date'] = self.df['Date'].apply(PmsCleaner.change_date_format)

    def reformat_data_csv(self):
        self.df['Month'] = self.df['Month'].apply(PmsCleaner.change_month_format)
        self.df['Date'] = pd.to_datetime(100*self.df['Year']+self.df['Month'], format='%Y%m') + MonthEnd(1)
        self.df['Date'] = self.df['Date'].apply(PmsCleaner.change_date_format)
        self.df.set_index('Date', inplace=True)
        self.df.drop(columns=['Unnamed: 0', 'Year', 'Month'], inplace=True)
        self.df = self.df.sort_index()
        return self.df

    def print_csv(self, filepath):
        self.df.to_csv(filepath)
