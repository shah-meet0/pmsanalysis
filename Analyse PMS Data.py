# -*- coding: utf-8 -*-
"""
Created on Fri Sep  4 07:09:56 2020

@author: Administrator
"""


import pandas as pd
import datetime
from pandas.tseries.offsets import MonthEnd

pd.set_option('display.max_columns', 15)
pd.set_option('display.max_rows', 300)

def change_month_format(month_name):
    month_num = datetime.datetime.strptime(month_name, "%B").month
    return month_num

def read_data_file(filename):
    df_data=pd.read_csv(filename)
    df_data['Month']=df_data['Month'].apply(change_month_format) 
    df_data['Date'] = pd.to_datetime(100*df_data.Year + df_data.Month ,format = '%Y%m') + MonthEnd(1)
    df_data.set_index('Date',inplace=True)
    df_data.drop(columns=['Unnamed: 0.1', 'Unnamed: 0','Year','Month'],inplace=True)
    df_data=df_data.sort_index()
    return df_data

def clean_managers (df_data, year):
    managers=df_data['Manager Name'].unique()

    for manager in managers:
        df_pms_manager=df_data[df_data['Manager Name']==manager]
        if df_pms_manager.last_valid_index().year < year or df_pms_manager.shape[0] < 13:        
            df_data = df_data[df_data['Manager Name'] != manager]
    
    return df_data
            




filename='C:\\users\\administrator\\onedrive\\vm\\final pms data.csv'
filename1='C:\\users\\administrator\\onedrive\\vm\\final pms data1.csv'
#df_pms_data=read_data_file(filename)
#df_pms_data= clean_managers(df_pms_data, 2020)

df_pms_data =pd.read_csv(filename1)
df_pms_data.set_index('Date', inplace = True)

indexes=df_pms_data.index.unique()
df_mean_returns=pd.DataFrame(columns=['Return Date','Mean Return'])

for i,idx in enumerate(indexes):
    df_pms_date=df_pms_data[df_pms_data.index==idx]
    mean_return=df_pms_date['Return'].mean()
    df_mean_returns.loc[i]=(idx,mean_return)
df_mean_returns.set_index('Return Date',inplace=True)
    
managers = df_pms_data['Manager Name'].unique()

for manager in managers:
    df_pms_manager=df_pms_data[df_pms_data['Manager Name']==manager]
    if df_pms_manager.shape[0] != 31:
        
        manager_indexes=df_pms_manager.index.unique()
       
        flag=0
        for idx in indexes:
             if idx in manager_indexes:
                 previous_aum=df_pms_manager.loc[idx,'AUM (crs)']
                 previous_turnover=df_pms_manager.loc[idx,'Turnover Ratio']
             if flag==0:
                 if idx in manager_indexes:
                     flag=1
                     continue
             else:
                 if idx not in manager_indexes:
                     
                     mean_return=df_mean_returns.loc[idx,'Mean Return']
                     
                     previous_aum=previous_aum*((100+mean_return)/100)
                     df_pms_append=pd.DataFrame(columns=['Date','Manager Name','AUM (crs)','Turnover Ratio','Return'])
                     df_pms_append.loc[0]=(idx,manager,previous_aum,previous_turnover,mean_return)
                     df_pms_append.set_index('Date',inplace=True)
                     print(df_pms_append.head())
                     df_pms_data = pd.concat([df_pms_data, df_pms_append])

df_pms_data.to_csv(filename1)                    
                     
