import pandas as pd
from datetime import datetime
from pandas.tseries.offsets import MonthEnd


# Needs documentation
class PmsCleaner:

    def __init__(self, filepath, date_format):
        self.df = pd.read_csv(filepath)
        self.df['Date'] = pd.to_datetime(self.df['Date'], format=date_format) + MonthEnd(1)
        self.df.set_index('Date', inplace=True, drop=False)
        PmsReformater.change_date_format(self.df, '%Y-%m-%d', '%B %Y')


    def remove_irrelevant_managers(self, year, entries):
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

    def drop_duplicates(self):
        managers = self.df['Manager Name'].unique()
        for manager in managers:
            manager_df = self.df[self.df['Manager Name'] == manager]
            duplicated_dates = manager_df[manager_df.duplicated()]
            if len(duplicated_dates) > 0:
                manager_df.drop_duplicates(['Date'], inplace=True)
                print(1)
                self.df = self.df[self.df['Manager Name'] != manager]
                self.df = pd.concat([self.df, manager_df], axis=0)


    def find_missing_dates(self, start_year, start_month, end_year, end_month):
        pass

    def get_index_returns_for_dates(self, manager, index_returns):
        manager_df = self.df[self.df['Manager Name'] == manager]
        print(manager_df.head(5))
        index_returns.drop(columns=['Date'], inplace=True)
        manager_df.drop(columns=['Date'], inplace=True)
        manager_df = pd.merge(manager_df, index_returns['Index Return'], how= 'outer', left_index=True, right_index=True)
        print(manager_df)

    def print_csv(self, filepath):
        self.df.sort_index(inplace=True)
        self.df.set_index('Date', inplace=True)
        print(self.df.head(5))
        self.df.to_csv(filepath)


class PmsReformater:

    def __init__(self, filepath):
        self.df = pd.read_csv(filepath)

    @staticmethod
    def change_month_format(month_name: str):
        return datetime.strptime(month_name, "%B").month

    @staticmethod
    def change_date_format(df, from_format, to_format):
        df['Date'] = pd.to_datetime(df['Date'], format=from_format)
        df['Date'] = df['Date'].apply(lambda date: datetime.strftime(date, to_format))

    def reformat_data_csv(self, from_format, to_format):
        self.df['Month'] = self.df['Month'].apply(PmsReformater.change_month_format)
        self.df['Date'] = pd.to_datetime(100*self.df['Year']+self.df['Month'], format='%Y%m') + MonthEnd(1)
        self.df.set_index('Date', inplace=True, drop =False)
        self.df.drop(columns=['Unnamed: 0', 'Year', 'Month'], inplace=True)
        self.df = self.df.sort_index()
        PmsReformater.change_date_format(self.df, from_format, to_format)
        return self.df

    def print_csv(self, filepath):
        self.df.to_csv(filepath)
