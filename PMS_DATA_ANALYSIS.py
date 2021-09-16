# -*- coding: utf-8 -*-
"""
Created on Fri Sep 11 07:59:47 2020

@author: Administrator
"""


import pandas as pd
import matplotlib.pyplot as plt
import risk_kit as rk

filename_1='C:\\users\\administrator\\onedrive\\vm\\final pms data1.csv'
filename_2 ='C:\\users\\administrator\\onedrive\\vm\\return analysis.csv'
df_pms_data=pd.read_csv(filename_1,parse_dates=['Date'],infer_datetime_format=True,index_col='Date')
print(df_pms_data.dtypes)
print(df_pms_data.head())

managers=df_pms_data['Manager Name'].unique()
df_return_analysis=pd.DataFrame(columns=['Manager','Entries','Ann_Ret','Ann_Vol','Sharpe_Ratio','Drawdown','Skewness','Kurtosis'])
i=0
for manager in managers:
    df_pms_manager=df_pms_data[df_pms_data['Manager Name']==manager]
    print(df_pms_manager.head())
    r=df_pms_manager['Return']/100
    entries=df_pms_manager.shape[0]
    periods_per_year=12
    riskfree_rate=0.07
    ann_r = rk.annualize_rets(r,periods_per_year)
    ann_vol = rk.annualize_vol(r, periods_per_year)
    ann_sr = rk.sharpe_ratio(r, riskfree_rate, periods_per_year)
    skew=rk.skewness(r)
    kurt=rk.kurtosis(r)
    dd = r.aggregate(lambda r: rk.drawdown(r).Drawdown.min())
    df_return_analysis.loc[i]=(manager,entries,ann_r,ann_vol,ann_sr,dd,skew, kurt)
    i=i+1
df_return_analysis.to_csv(filename_2)
print(df_return_analysis.head())  

