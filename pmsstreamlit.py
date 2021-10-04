import datetime

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import analyse_pms_data as apd
from pandas.tseries.offsets import MonthEnd
import matplotlib.dates as mdates
from datetime import date


@st.cache
def read_analysed_data():
    analysed_data = pd.read_csv('./Resources/pms_data_analysed_sept_2021.csv')
    analysed_data.drop(columns='Unnamed: 0', inplace=True)
    analysed_data.set_index('Manager Name', inplace=True)
    analysed_data.sort_index(inplace=True)
    list_of_managers = [manager_name for manager_name in analysed_data.index.unique()]
    return analysed_data, list_of_managers


@st.cache
def read_monthly_data():
    monthly_data = pd.read_csv('./Resources/pms_data_cleaned_final_sept_2021.csv')
    indexed_monthly_data = monthly_data.copy()
    indexed_monthly_data['Date'] = pd.to_datetime(indexed_monthly_data['Date'], format='%B %Y') + MonthEnd(1)
    indexed_monthly_data.set_index('Date', inplace=True, drop=False)
    missing_dates_df = apd.PmsCleaner.make_missing_dates_df(indexed_monthly_data)
    return monthly_data, indexed_monthly_data, missing_dates_df


@st.cache
def parse_nifty_returns():
    nifty_returns = pd.read_csv('./Resources/Nifty_Returns_2018_2021.csv')
    nifty_returns['Date'] = pd.to_datetime(nifty_returns['Date'], format='%B %Y') + MonthEnd(1)
    nifty_returns.set_index('Date', inplace=True)
    return nifty_returns['Index Return']


@st.cache
def estimate_missing_dates(manager_df, missing_dates_for_manager, index_return, beta):
    missing_dates_returns = index_return.loc[missing_dates_for_manager]
    estimated_returns = missing_dates_returns * beta
    manager_dated = manager_df.copy()
    manager_dated['Date'] = pd.to_datetime(manager_dated['Date'], format='%B %Y') + MonthEnd(1)
    manager_dated.set_index('Date', inplace=True)
    known_returns = manager_dated['Return']
    final_returns = pd.concat([known_returns, estimated_returns])
    final_returns.sort_index(inplace=True)
    return final_returns

def on_manager_selection(manager_selected, _analysed_data, _monthly_data, index_returns):
    manager_brief = _analysed_data.loc[manager_selected]
    manager_long = _monthly_data[_monthly_data['Manager Name'] == manager_selected]
    manager_long.reset_index(inplace=True, drop=True)
    st.table(manager_brief)
    manager_beta = manager_brief['Estimated Beta']
    missing_dates = missing_dates_df.loc[manager]['Missing Dates']
    est_returns = estimate_missing_dates(manager_long, missing_dates, index_returns, manager_beta)
    joint_wealth_df = make_wealth_indexes(index_returns, est_returns)
    fig_r = plt.figure(1)
    plt.plot(est_returns.index, est_returns*100, label='Manager Returns')
    plt.plot(index_returns*100, label='Index Returns')
    plt.gca().set_xlim(est_returns.first_valid_index(), date(2021, 9, 30))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %y'))
    for label in plt.gca().xaxis.get_ticklabels()[1:-1:2]:
        label.set_visible(False)
    plt.gca().set_ylabel('Return %')
    plt.legend()

    fig_w = plt.figure(2)
    start_date = joint_wealth_df.first_valid_index()
    end_date = joint_wealth_df.last_valid_index()
    plt.plot(joint_wealth_df.index, joint_wealth_df['Manager Wealth'], label='Manager Wealth Evolution')
    plt.plot(joint_wealth_df.index, joint_wealth_df['Index Wealth'], label='Index Wealth Evolution')
    plt.gca().set_xlim(start_date, date(2021,9,30))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %y'))
    for label in plt.gca().xaxis.get_ticklabels()[1:-1:2]:
        label.set_visible(False)
    plt.gca().set_ylabel('Wealth')
    plt.legend()

    end_wealth_index = round(joint_wealth_df.loc[end_date]['Index Wealth'],2)
    end_wealth_pms = round(joint_wealth_df.loc[end_date]['Manager Wealth'],2)
    start_date_formatted = datetime.datetime.strftime(start_date, '%b %Y')
    end_date_formatted = datetime.datetime.strftime(end_date, '%b %Y')

    st.pyplot(fig_r)
    st.pyplot(fig_w)
    st.write(f'From {start_date_formatted} to {end_date_formatted}:')
    st.write(f'Manager would have taken Rupees 1000 to Rupees {end_wealth_pms}')
    st.write(f'While Nifty 500 would have taken Rupees 1000 to Rupees {end_wealth_index}')
    st.dataframe(manager_long)


@st.cache
def make_wealth_indexes(index_returns, est_returns):
    entries = []
    index_wealth = 1000
    pms_wealth = 1000
    for index, ret in est_returns.iteritems():
        index_wealth *= (index_returns[index] + 1)
        pms_wealth *= (ret + 1)
        entries.append([index, index_wealth, pms_wealth])
    joint_wealth = pd.DataFrame(data=entries, columns=['Date', 'Index Wealth', 'Manager Wealth'])
    joint_wealth.set_index('Date', inplace=True)
    joint_wealth.sort_index(inplace=True)
    return joint_wealth


(analysed_data, list_of_managers) = read_analysed_data()
(monthly_data, indexed_monthly_data, missing_dates_df) = read_monthly_data()
index_returns = parse_nifty_returns()

# st.markdown(
#     """
#     <style>
#     .reportview-container {
#         background: white
#     }
#    .sidebar .sidebar-content {
#         background: grey
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )
st.title("Portfolio Management Service Analysis")
st.write("By Meet Shah")

manager = st.sidebar.selectbox('Manager', ['All'] + list_of_managers)
if manager == 'All':
    st.write("Click on column header to sort by it")
    st.dataframe(analysed_data.style.background_gradient(cmap='Blues', axis=0).format(precision=3))
    fig, (ax1, ax2) = plt.subplots(1, 2)

    ax1.hist(analysed_data['Annualized Return'] * 100, color='Red')
    ax1.set_title('Annualized Return (%)')
    ax1.set_xlim((-50, 51))
    ax1.set_ylabel('Frequency')

    ax2.hist(analysed_data['Annualized Volatility'] * 100)
    ax2.set_title('Annualized Volatility (%)')

    fig.set_facecolor('#91878a')

    st.pyplot(fig)
    st.write('All data has been obtained from the Securities and Exchange Board of India. '
             'There are sometimes mistakes done by them in data collection, which affects the statistics presented.'
             'I have removed some obvious outliers, but there still might be mistakes. Please keep this in mind when '
             'viewing say the highest annualized return.')
else:
    on_manager_selection(manager, analysed_data, monthly_data, index_returns)
