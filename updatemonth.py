# This script can be used to update the data base. Will require changes in streamlit code
# Can make streamlit auto update, but for now doing it manually so backups are preserved in case
# Sebi changes some stuff.
# uses only obtained data.

import pandas as pd
import get_pms_data as gpd
import analyse_pms_data as apd
from pandas.tseries.offsets import MonthEnd


def get_manager_list_and_last_month(filepath_to_current_data):
    current_data = pd.read_csv(filepath_to_current_data)
    manager_list = current_data['Manager Name'].unique()
    current_data['Date'] = pd.to_datetime(current_data['Date'], format='%B %Y') + MonthEnd(1)
    current_data.set_index('Date', inplace=True)
    current_data.sort_index(inplace=True)
    last_month = current_data.last_valid_index().month
    return manager_list, last_month


def get_data_for_month(manager_list, month, year, driver_loc, filepath_to_save):
    updater = gpd.PmsImporter(driver_loc)
    updated_month_df = updater.get_data_for_month_with_list(manager_list, month, year)
    updated_month_df.to_csv(filepath_to_save)
    return updated_month_df


def format_manager_data(location_of_new_data):
    reformatter = apd.PmsReformater(location_of_new_data)
    reformatter.reformat_data_csv()
    reformatter.df.drop('Date', inplace=True)
    return reformatter.df


def add_to_orig_data(filepath_to_current_data, reformatted_df):
    current_data = pd.read_csv(filepath_to_current_data)
    current_data['Date'] = pd.to_datetime(current_data['Date'], format='%B %Y') + MonthEnd(1)
    current_data.set_index('Date', inplace=True)
    final_df = pd.merge(current_data, reformatted_df, left_index=True, right_index=True, how='outer')
    return final_df


def analyse_new_data(filepath_to_merged_data, filepath_to_index_returns):
    analyser = apd.PmsAnalyser(filepath_to_merged_data)
    return analyser.get_analysed_df(filepath_to_index_returns)


def update_routine(filepath_to_current_data, filepath_to_index_returns, driver_loc, year, month=None, infer_month=False):
    manager_list, last_month = get_manager_list_and_last_month(filepath_to_current_data)
    if infer_month:
        month = last_month + 1
    filepath_to_save = f'./Updates/raw_data_{year}_{month}.csv'
    get_data_for_month(manager_list, month, year, driver_loc, filepath_to_save)
    reformatted_data = format_manager_data(filepath_to_save)
    merged_df = add_to_orig_data(filepath_to_current_data, reformatted_data)
    filepath_to_final_data = f'./Updates/combined_data_{year}_{month}.csv'
    merged_df.to_csv(filepath_to_final_data)
    final_analysed_df = analyse_new_data(filepath_to_final_data, filepath_to_index_returns)
    filepath_to_analysed_final_data = f'./Updates/analysed_data_{year}_{month}.csv'
    final_analysed_df.to_csv(filepath_to_analysed_final_data)


