import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime


@st.cache
def read_files():
    analysed_data = pd.read_csv('./Resources/pms_data_analysed_sept_2021.csv')
    analysed_data.drop(columns='Unnamed: 0', inplace=True)
    analysed_data.set_index('Manager Name', inplace=True)
    full_data = pd.read_csv('./Resources/pms_data_cleaned_final_sept_2021.csv')
    # full_data['Date'] = pd.to_datetime(full_data['Date'], format ='%B %Y')
    # full_data.set_index('Date', inplace=True)
    nifty_returns = pd.read_csv('./Resources/Nifty_Returns_2018_2021.csv')
    return analysed_data, full_data, nifty_returns



(analysed_data, full_data, nifty_returns) = read_files()

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
    fig, axs = plt.subplots()
    plt.plot(manager_long['Date'], wealth)
    d1 = manager_long['Date'].iloc[0]
    d2 = manager_long['Date'].iloc[-1]
    st.pyplot(fig)
    st.write('From ' + d1 + ' to ' + d2 + ', Rupees 1000 would become Rupees ' + "{:.2f}".format(wealth[-1]))
