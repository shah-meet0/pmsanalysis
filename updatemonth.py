# This script can be used to update the data base. Will require changes in streamlit code
# Can make streamlit auto update, but for now doing it manually so backups are preserved in case
# Sebi changes some stuff.
# uses only obtained data

import pandas as pd
import get_pms_data as gpd
import analyse_pms_data as apd


def get_manager_list_and_last_month(filepath_to_current_data):
    current_data = pd.read_csv(filepath_to_current_data)
    manager_list = current_data['Manager'].unique()
    current_data['Date'] = pd.to_datetime(current_data['Date'], format='%B %Y')
    current_data.set_index('Date', inplace=True)
    current_data.sort_index(inplace=True)
    last_month = current_data.last_valid_index.month
    return manager_list, last_month


def get_data_for_month(manager_list, month, year, driver_loc, filepath_to_save):
    updater = gpd.PmsImporter(driver_loc)
    updated_month_df = updater.get_data_for_month_with_list(manager_list, month, year)
    updated_month_df.to_csv(filepath_to_save)
    return updated_month_df


def format_manager_data(location_of_new_data, filepath_to_save):
    reformatter = apd.PmsReformater(location_of_new_data)
    reformatter.reformat_data_csv()
    reformatter.print_csv(filepath_to_save)
    return reformatter.df


def add_to_orig_data(filepath_to_current_data, reformatted_df):
    pass


def analyse_new_data(filepath_to_merged_data):
    pass

def update_routine():
    # backup is a local folder
    pass


