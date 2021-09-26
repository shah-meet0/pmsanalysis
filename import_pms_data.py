# -*- coding: utf-8 -*-
"""
Created on Sat Sep  5 07:45:35 2020
Module Allows for Opening Sebi Website and Scrapping Data

@author: Administrator
"""

from selenium import webdriver
import time
import pandas as pd
from time import sleep

driver_loc = r'C:\Users\Meet Shah\Desktop\Programs\chromedriver_win32\chromedriver.exe'


def get_all_data(filepath, driver_location=driver_loc):
    df = pd.DataFrame(columns=['Manager Name', 'Year', 'Month', 'AUM (crs)', 'Turnover Ratio', 'Return'])
    '''
    
    Parameters
    ----------
   
    driver_location : TYPE, optional
        DESCRIPTION. The default is driver_loc.(For samir's virtual machine')

    Returns new dataframe with all pms data(most recent 3 years), on desktop as alldata.csv
    -------
    Use only when necessary, returns all the data, runtime around 16-17 hours.

    '''
    url = 'https://www.sebi.gov.in/sebiweb/other/OtherAction.do?doPmr=yes'
    driver = webdriver.Chrome(driver_location)
    driver.get(url)

    i = 0
    for manager in range(2, 754):
        df.to_csv(filepath)
        try:
            current_manager = driver.find_element_by_xpath('//*[@id="2"]/div[1]/select/option[' + str(manager) + ']')
            current_manager_name = current_manager.text
            current_manager.click()
        except Exception:
            driver.get(url)
            current_manager = driver.find_element_by_xpath('//*[@id="2"]/div[1]/select/option[' + str(manager) + ']')
            current_manager_name = current_manager.text
            current_manager.click()
        for year in range(2, 5):
            try:
                current_year = driver.find_element_by_xpath('//*[@id="2"]/div[2]/select/option[' + str(year) + ']')
                current_year_name = current_year.text
                current_year.click()
            except Exception:
                driver.get(url)
                current_manager = driver.find_element_by_xpath(
                    '//*[@id="2"]/div[1]/select/option[' + str(manager) + ']')
                current_manager_name = current_manager.text
                current_manager.click()
                current_year = driver.find_element_by_xpath('//*[@id="2"]/div[2]/select/option[' + str(year) + ']')
                current_year_name = current_year.text
                current_year.click()
            for month in range(2, 14):
                sleep(2.5)
                try:
                    current_month = driver.find_element_by_xpath(
                        '//*[@id="2"]/div[3]/select/option[' + str(month) + ']')
                    current_month_name = current_month.text
                    current_month.click()
                    driver.find_element_by_xpath('//*[@id="2"]/div[4]/div/a').click()
                except Exception:
                    try:
                        driver.close()
                        driver = webdriver.Chrome(driver_location)
                    except Exception:
                        driver = webdriver.Chrome(driver_location)
                    driver.get(url)
                    current_manager = driver.find_element_by_xpath(
                        '//*[@id="2"]/div[1]/select/option[' + str(manager) + ']')
                    current_manager_name = current_manager.text
                    current_manager.click()
                    current_year = driver.find_element_by_xpath('//*[@id="2"]/div[2]/select/option[' + str(year) + ']')
                    current_year_name = current_year.text
                    current_year.click()
                    current_month = driver.find_element_by_xpath(
                        '//*[@id="2"]/div[3]/select/option[' + str(month) + ']')
                    current_month_name = current_month.text
                    current_month.click()
                    driver.find_element_by_xpath('//*[@id="2"]/div[4]/div/a').click()
                try:
                    p1 = float(driver.find_element_by_xpath(
                        '//*[@id="member-wrapper"]/section/div[4]/div/table/tbody/tr[4]/td[11]').text)
                    p2 = float(driver.find_element_by_xpath(
                        '//*[@id="member-wrapper"]/section/div[4]/div/table/tbody/tr[5]/td[11]').text)
                    p3 = float(driver.find_element_by_xpath(
                        '//*[@id="member-wrapper"]/section/div[4]/div/table/tbody/tr[6]/td[11]').text)
                    p4 = float(driver.find_element_by_xpath(
                        '//*[@id="member-wrapper"]/section/div[4]/div/table/tbody/tr[7]/td[11]').text)
                    p5 = float(driver.find_element_by_xpath(
                        '//*[@id="member-wrapper"]/section/div[4]/div/table/tbody/tr[8]/td[11]').text)
                    assets_under_management = p1 + p2 + p3 + p4 + p5
                    if assets_under_management > 0:
                        turnover_ratio = float(driver.find_element_by_xpath(
                            '//*[@id="member-wrapper"]/section/div[6]/div/table/tbody/tr/td[3]').text)
                        month_return = float(driver.find_element_by_xpath(
                            '//*[@id="member-wrapper"]/section/div[6]/div/table/tbody/tr/td[4]').text)
                        df.loc[i] = (
                        current_manager_name, current_year_name, current_month_name, assets_under_management,
                        turnover_ratio, month_return)
                        i = i + 1
                    else:
                        pass
                except Exception:
                    if int(current_year_name) != 2020 or month < 9:
                        print(current_manager_name, current_year_name, current_month_name, 'not available')
                    else:
                        pass

    df.to_csv(filepath)

    time.sleep(10)
    driver.close()
    return df


def get_all_for_month(month, driver_location=driver_loc):
    df = pd.DataFrame(columns=['Manager Name', 'Year', 'Month', 'AUM (crs)', 'Turnover Ratio', 'Return'])
    '''
    
    Parameters
    ----------
    month : TYPE, required
        Type in Month name wanted, first letter Capital. STRING ONLY
    dataframe : TYPE, optional
        DESCRIPTION. The default is df.
    driver_location : TYPE, optional
        DESCRIPTION. The default is driver_loc.

    Returns csv with all relevant managers on desktop as latest month .csv
    -------
    Use to get data for latest months, defaults to latest year, change year = within the code to get for some other year

    '''
    month_numbers = {'January': 2, 'February': 3, 'March': 4, 'April': 5, 'May': 6, 'June': 7, 'July': 8, 'August': 9,
                     'September': 10, 'October': 11, 'November': 12, 'December': 13}
    month_number = month_numbers[month]
    year = 2
    url = 'https://www.sebi.gov.in/sebiweb/other/OtherAction.do?doPmr=yes'
    driver = webdriver.Chrome(driver_location)
    driver.get(url)

    i = 0
    for manager in range(2, 754):
        df.to_csv('C:/Users/Administrator/Desktop/latest' + month + '.csv')
        try:
            current_manager = driver.find_element_by_xpath('//*[@id="2"]/div[1]/select/option[' + str(manager) + ']')
            current_manager_name = current_manager.text
            current_manager.click()
            current_year = driver.find_element_by_xpath('//*[@id="2"]/div[2]/select/option[' + str(year) + ']')
            current_year_name = current_year.text
            current_year.click()
            current_month = driver.find_element_by_xpath('//*[@id="2"]/div[3]/select/option[' + str(month_number) + ']')
            current_month_name = current_month.text
            current_month.click()
            driver.find_element_by_xpath('//*[@id="2"]/div[4]/div/a').click()
        except Exception:
            driver.get(url)
            current_manager = driver.find_element_by_xpath('//*[@id="2"]/div[1]/select/option[' + str(manager) + ']')
            current_manager_name = current_manager.text
            current_manager.click()
            current_year = driver.find_element_by_xpath('//*[@id="2"]/div[2]/select/option[' + str(year) + ']')
            current_year_name = current_year.text
            current_year.click()
            current_month = driver.find_element_by_xpath('//*[@id="2"]/div[3]/select/option[' + str(month_number) + ']')
            current_month_name = current_month.text
            current_month.click()
            driver.find_element_by_xpath('//*[@id="2"]/div[4]/div/a').click()

        try:
            p1 = float(driver.find_element_by_xpath(
                '//*[@id="member-wrapper"]/section/div[4]/div/table/tbody/tr[4]/td[11]').text)
            p2 = float(driver.find_element_by_xpath(
                '//*[@id="member-wrapper"]/section/div[4]/div/table/tbody/tr[5]/td[11]').text)
            p3 = float(driver.find_element_by_xpath(
                '//*[@id="member-wrapper"]/section/div[4]/div/table/tbody/tr[6]/td[11]').text)
            p4 = float(driver.find_element_by_xpath(
                '//*[@id="member-wrapper"]/section/div[4]/div/table/tbody/tr[7]/td[11]').text)
            p5 = float(driver.find_element_by_xpath(
                '//*[@id="member-wrapper"]/section/div[4]/div/table/tbody/tr[8]/td[11]').text)
            assets_under_management = p1 + p2 + p3 + p4 + p5
            if assets_under_management > 0:
                turnover_ratio = float(driver.find_element_by_xpath(
                    '//*[@id="member-wrapper"]/section/div[6]/div/table/tbody/tr/td[3]').text)
                month_return = float(driver.find_element_by_xpath(
                    '//*[@id="member-wrapper"]/section/div[6]/div/table/tbody/tr/td[4]').text)
                df.loc[i] = (
                current_manager_name, current_year_name, current_month_name, assets_under_management, turnover_ratio,
                month_return)
                i = i + 1
            else:
                pass
        except Exception:
            pass
    driver.close()
    df.to_csv('C:/Users/Administrator/Desktop/latest' + month + '.csv')
    return df


def get_entry(manager, year, month, driver_location=driver_loc):
    df = pd.DataFrame(columns=['Manager Name', 'Year', 'Month', 'AUM (crs)', 'Turnover Ratio', 'Return'])
    ''' Gets one entry and puts it on desktop as manager_year_month.csv
        Input Manager Name as manager ID(using xpath on sebipms), do the same for year.
        Month: First letter capital, STRING ONLY, full name. '''
    month_numbers = {'January': 2, 'February': 3, 'March': 4, 'April': 5, 'May': 6, 'June': 7, 'July': 8, 'August': 9,
                     'September': 10, 'October': 11, 'November': 12, 'December': 13}
    month_number = month_numbers[month]
    driver = webdriver.Chrome(driver_location)
    driver.get('https://www.sebi.gov.in/sebiweb/other/OtherAction.do?doPmr=yes')
    current_manager = driver.find_element_by_xpath('//*[@id="2"]/div[1]/select/option[' + str(manager) + ']')
    current_manager_name = current_manager.text
    current_manager.click()
    current_year = driver.find_element_by_xpath('//*[@id="2"]/div[2]/select/option[' + str(year) + ']')
    current_year_name = current_year.text
    current_year.click()
    current_month = driver.find_element_by_xpath('//*[@id="2"]/div[3]/select/option[' + str(month_number) + ']')
    current_month_name = current_month.text
    current_month.click()
    driver.find_element_by_xpath('//*[@id="2"]/div[4]/div/a').click()
    try:
        p1 = float(
            driver.find_element_by_xpath('//*[@id="member-wrapper"]/section/div[4]/div/table/tbody/tr[4]/td[11]').text)
        p2 = float(
            driver.find_element_by_xpath('//*[@id="member-wrapper"]/section/div[4]/div/table/tbody/tr[5]/td[11]').text)
        p3 = float(
            driver.find_element_by_xpath('//*[@id="member-wrapper"]/section/div[4]/div/table/tbody/tr[6]/td[11]').text)
        p4 = float(
            driver.find_element_by_xpath('//*[@id="member-wrapper"]/section/div[4]/div/table/tbody/tr[7]/td[11]').text)
        p5 = float(
            driver.find_element_by_xpath('//*[@id="member-wrapper"]/section/div[4]/div/table/tbody/tr[8]/td[11]').text)
        assets_under_management = p1 + p2 + p3 + p4 + p5
        if assets_under_management > 0:
            turnover_ratio = float(
                driver.find_element_by_xpath('//*[@id="member-wrapper"]/section/div[6]/div/table/tbody/tr/td[3]').text)
            month_return = float(
                driver.find_element_by_xpath('//*[@id="member-wrapper"]/section/div[6]/div/table/tbody/tr/td[4]').text)
            df.loc[0] = (
            current_manager_name, current_year_name, current_month_name, assets_under_management, turnover_ratio,
            month_return)
        else:
            pass
    except Exception:
        print('This entry is not available')
    driver.close()
    # df.to_csv('C:/Users/Administrator/Desktop/' +current_manager_name + current_year_name + current_month_name + '.csv' )
    return df


def get_year(manager, year, driver_location=driver_loc):
    '''
    

    Parameters
    ----------
    manager : int
        Manager ID code
        
    year : int
        2- latest year, ++ for next years (For eg, in 2020, 2018 = 4)
   
    dataframe : TYPE, optional
        DESCRIPTION. The default is df.
    
    driver_location : string, optional
        DESCRIPTION. The default is driver_loc. Enter location of chrome driver

    Returns
    -------
    CSV on desktop with all data for a particular year for  a particular manager

    '''
    df = pd.DataFrame(columns=['Manager Name', 'Year', 'Month', 'AUM (crs)', 'Turnover Ratio', 'Return'])
    i = 0
    driver = webdriver.Chrome(driver_location)
    driver.get('https://www.sebi.gov.in/sebiweb/other/OtherAction.do?doPmr=yes')
    current_manager = driver.find_element_by_xpath('//*[@id="2"]/div[1]/select/option[' + str(manager) + ']')
    current_manager_name = current_manager.text
    current_manager.click()
    current_year = driver.find_element_by_xpath('//*[@id="2"]/div[2]/select/option[' + str(year) + ']')
    current_year_name = current_year.text
    current_year.click()
    for month in range(2, 14):
        current_month = driver.find_element_by_xpath('//*[@id="2"]/div[3]/select/option[' + str(month) + ']')
        current_month_name = current_month.text
        current_month.click()
        driver.find_element_by_xpath('//*[@id="2"]/div[4]/div/a').click()
        try:
            p1 = float(driver.find_element_by_xpath(
                '//*[@id="member-wrapper"]/section/div[4]/div/table/tbody/tr[4]/td[11]').text)
            p2 = float(driver.find_element_by_xpath(
                '//*[@id="member-wrapper"]/section/div[4]/div/table/tbody/tr[5]/td[11]').text)
            p3 = float(driver.find_element_by_xpath(
                '//*[@id="member-wrapper"]/section/div[4]/div/table/tbody/tr[6]/td[11]').text)
            p4 = float(driver.find_element_by_xpath(
                '//*[@id="member-wrapper"]/section/div[4]/div/table/tbody/tr[7]/td[11]').text)
            p5 = float(driver.find_element_by_xpath(
                '//*[@id="member-wrapper"]/section/div[4]/div/table/tbody/tr[8]/td[11]').text)
            assets_under_management = p1 + p2 + p3 + p4 + p5
            if assets_under_management > 0:
                turnover_ratio = float(driver.find_element_by_xpath(
                    '//*[@id="member-wrapper"]/section/div[6]/div/table/tbody/tr/td[3]').text)
                month_return = float(driver.find_element_by_xpath(
                    '//*[@id="member-wrapper"]/section/div[6]/div/table/tbody/tr/td[4]').text)
                df.loc[i] = (
                current_manager_name, current_year_name, current_month_name, assets_under_management, turnover_ratio,
                month_return)
                i = i + 1
            else:
                pass
        except Exception:
            print(current_month_name + 'not available for ' + current_manager_name)
    driver.close()
    # df.to_csv('C:/Users/Administrator/Desktop/' +current_manager_name + current_year_name + '.csv')
    return df


def manager_id_maker(driver_location=driver_loc):
    '''
    

    Parameters
    ----------
    driver_location : TYPE, optional
        DESCRIPTION. The default is driver_loc.

    Returns
    -------
    csv with all managers and their id on desktop

    '''
    dataframe = pd.DataFrame(columns=['Manager Name', 'Manager ID'])
    i = 0
    manager_id = 2
    over = False
    driver = webdriver.Chrome(driver_location)
    driver.get('https://www.sebi.gov.in/sebiweb/other/OtherAction.do?doPmr=yes')
    while over != True:
        try:
            current_manager = driver.find_element_by_xpath('//*[@id="2"]/div[1]/select/option[' + str(manager_id) + ']')
            current_manager_name = current_manager.text
            dataframe.loc[i] = (current_manager_name, manager_id)
            i = i + 1
            manager_id = int(manager_id) + 1
        except Exception:
            over = True
    driver.close()
    dataframe.set_index('Manager ID', inplace=True)
    dataframe.to_csv('C:/Users/Administrator/Desktop/ManagerList.csv')
    return None


filepath = r'C:\Users\Meet Shah\Desktop\Programs\alldata.csv'
get_all_data(filepath)

