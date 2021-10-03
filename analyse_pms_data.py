import pandas as pd
from datetime import datetime
from pandas.tseries.offsets import MonthEnd
import risk_measures as rm


# TODO: needs documentation

class PmsAnalyser:

    def __init__(self, filepath):
        """
        Requires a csv which has been cleaned and formatted already using PmsCleaner and PmsReformater

        For instance: pms_data_cleaned_final_sept_2021.csv

        available on github.com/shah-meet0

        :param filepath: filepath to appropriate csv
        """

        self.df = pd.read_csv(filepath)
        self.df['Date'] = pd.to_datetime(self.df['Date'], format='%B %Y') + MonthEnd(1)
        self.df.set_index('Date', inplace=True, drop=False)
        PmsReformater.change_date_format(self.df, '%Y-%m-%d', '%B %Y')

    def get_beta_estimates(self, filepath_to_index_returns, risk_free_rate=0.0624):
        """
        For an example for what index_returns should look like, see Nifty_Returns_2018_2021.csv

        on github.com/shah-meet0

        :param filepath_to_index_returns: filepath to index_returns csv
        :param risk_free_rate: risk_free_rate estimate (annualized), and not in percent
        :return: dictionary containing manager name and estimated CAPM beta
        """
        monthly_risk_free_rate = (1 + risk_free_rate) ** (1/12) - 1
        index_returns = pd.read_csv(filepath_to_index_returns)
        index_returns['Date'] = pd.to_datetime(index_returns['Date']) + MonthEnd(1)
        index_returns.set_index('Date', inplace=True)
        managers = self.df['Manager Name'].unique()
        betas = {}
        for manager in managers:
            manager_df = self.get_index_returns_for_dates(manager, index_returns)
            beta_calc = rm.get_beta_estimate(manager_df['Return'], manager_df['Index Return'], monthly_risk_free_rate)
            betas[manager] = beta_calc[0][0][0]
            print(betas)
        return betas

    def get_index_returns_for_dates(self, manager, index_returns):
        manager_df = self.df[self.df['Manager Name'] == manager]
        manager_df = manager_df.drop(columns=['Date'])
        manager_df = pd.merge(manager_df, index_returns, how='outer', left_index=True,
                              right_index=True)
        manager_df.dropna(inplace=True)
        return manager_df


class PmsCleaner:

    def __init__(self, filepath, date_format='%B %Y'):
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

    @staticmethod
    def find_missing_dates(df: pd.DataFrame):
        starting_date = df.first_valid_index()
        ending_date = df.last_valid_index()
        dates = pd.date_range(starting_date, ending_date, freq='M')
        missing_dates = []
        for date in dates:
            if date not in df.index:
                missing_dates.append(datetime.strftime(date, '%Y-%m-%d'))
        return missing_dates

    def make_missing_dates_dict(self):
        managers = self.df['Manager Name'].unique()
        missing_dates_dict = {}
        for manager in managers:
            manager_df = self.df[self.df['Manager Name'] == manager]
            missing_dates = PmsCleaner.find_missing_dates(manager_df)
            missing_dates_dict[manager] = missing_dates
        return missing_dates_dict

    def print_csv(self, filepath):
        self.df.sort_index(inplace=True)
        self.df.set_index('Date', inplace=True)
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
        self.df['Date'] = pd.to_datetime(100 * self.df['Year'] + self.df['Month'], format='%Y%m') + MonthEnd(1)
        self.df.set_index('Date', inplace=True, drop=False)
        self.df.drop(columns=['Unnamed: 0', 'Year', 'Month'], inplace=True)
        self.df = self.df.sort_index()
        PmsReformater.change_date_format(self.df, from_format, to_format)
        return self.df

    def print_csv(self, filepath):
        self.df.sort_index(inplace=True)
        self.df.set_index('Date', inplace=True)
        self.df.to_csv(filepath)
