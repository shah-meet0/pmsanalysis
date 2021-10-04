import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime


@st.cache
def read_data_files():
    analysed_data = pd.read_csv('./Resources/pms_data_analysed_sept_2021.csv')
    analysed_data.drop(columns='Unnamed: 0', inplace=True)
    analysed_data.set_index('Manager Name', inplace=True)
    full_data = pd.read_csv('./Resources/pms_data_cleaned_final_sept_2021.csv')
    # full_data['Date'] = pd.to_datetime(full_data['Date'], format ='%B %Y')
    # full_data.set_index('Date', inplace=True)

    return analysed_data, full_data


@st.cache
def parse_nifty_returns():
    nifty_returns = pd.read_csv('./Resources/Nifty_Returns_2018_2021.csv')
    index_returns = nifty_returns['Index Return']
    wealth_evolution = [1000]
    for index, return_value in index_returns.iteritems():
        wealth_evolution.append(wealth_evolution[-1] * (1 + return_value))
    wealth_evolution = wealth_evolution[1:-2]
    return index_returns, wealth_evolution


(analysed_data, full_data) = read_data_files()
(index_returns, index_wealth) = parse_nifty_returns()

st.markdown(
    """
    <style>
    .reportview-container {
        background: white
    }
   .sidebar .sidebar-content {
        background: grey
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.title("Portfolio Management Service Analysis")
st.write("By Meet Shah")
list_of_managers = [manager for manager in analysed_data.index.unique()]
list_of_managers.sort()
manager = st.sidebar.selectbox('Manager', ['All'] + list_of_managers)
if manager == 'All':
    st.write("Click on column header to sort by it")
    st.dataframe(analysed_data.style.background_gradient(cmap='Blues', axis=0).format(precision=3))
    st.write('All data has been obtained from the Securities and Exchange Board of India. '
             'There are sometimes mistakes done by them in data collection, which affects the statistics presented.'
             'I have removed some obvious outliers, but there still might be mistakes. Please keep this in mind when '
             'viewing say the highest annualized return.')
else:
    manager_brief = analysed_data.loc[manager]
    manager_long = full_data[full_data['Manager Name'] == manager]
    manager_long.reset_index(inplace=True, drop=True)
    st.dataframe(manager_brief)
    st.dataframe(manager_long)
    entry_1 = 1000 * (1 + (manager_long['Return'].iloc[0]))
    wealth = [entry_1]
    length = manager_long.shape[0]
    for i in range(1, length):
        wealth.append(wealth[-1] * (1 + (manager_long['Return'].iloc[i])))
    fig = plt.figure(1)
    plt.plot(wealth, label='Manager Wealth')
    plt.plot(index_wealth, label='Index Wealth')
    plt.xlabel('Date')
    plt.ylabel('Wealth')
    plt.legend()
    st.pyplot(fig)
    fig2 = plt.figure(2)
    plt.plot(manager_long['Return'],label ='Manager Return')
    plt.plot(index_returns, label = 'Index Return')
    plt.legend()
    d1 = manager_long['Date'].iloc[0]
    d2 = manager_long['Date'].iloc[-1]
    st.pyplot(fig2)
    st.write('From ' + d1 + ' to ' + d2 + ', Rupees 1000 would become Rupees ' + "{:.2f}".format(wealth[-1]))
