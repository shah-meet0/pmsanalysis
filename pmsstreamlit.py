import datetime

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import analyse_pms_data as apd
from pandas.tseries.offsets import MonthEnd
import matplotlib.dates as mdates
from datetime import date
plt.rcParams['axes.facecolor'] = '#F0F0F5'
plt.rcParams['figure.facecolor'] = '#F0F0F5'
st.set_page_config(page_title='PMS Analysis')


@st.cache
def read_analysed_data():
    analysed_data = pd.read_csv('./Resources/pms_data_analysed_sept_2021.csv')
    analysed_data.drop(columns='Unnamed: 0', inplace=True)
    analysed_data.set_index('Manager Name', inplace=True)
    analysed_data.sort_index(inplace=True)
    analysed_data = analysed_data.rename(columns={'Annualized Return': 'Ann_Ret', 'Annualized Volatility': 'Ann_Vol',
                                   'Estimated Beta': 'Est_Beta'})
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
    st.title(manager_selected)
    manager_brief = _analysed_data.loc[manager_selected]
    manager_brief = manager_brief.rename({'Ann_Ret': 'Annualized Return', 'Ann_Vol': 'Annualized Volatility',
                                  'Est_Beta': 'Estimated Beta'})
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
    st.write(f'Manager would have taken Rupees 1000 to Rupees {end_wealth_pms}.')
    st.write(f'While Nifty 500 would have taken Rupees 1000 to Rupees {end_wealth_index}.')
    st.dataframe(manager_long)

    st.write(f'WARNING: Wealth evolution and Returns both have forecasts from Sep 2020 to Mar 2021.')
    st.write(f'This forecast is not taken into account in the statistics calculated, but does affect'
             f' graphs and wealth evolution')


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

# *****************************Start of App***************************** #


manager = st.sidebar.selectbox('Manager', ['All'] + list_of_managers)
if manager == 'All':

    data_source_flag = st.sidebar.checkbox(label='Give Data Source.')
    data_processing_flag = st.sidebar.checkbox(label='More Info on Data Processing.')
    data_validity_flag = st.sidebar.checkbox(label='More Info on Data Validity.')
    hide_data_flag = st.sidebar.checkbox(label='Hide Data.')
    contact_me_flag = st.sidebar.checkbox(label='About Me.')

    if data_source_flag:
        st.title('Data Source')
        st.write('Notes:')
        st.write('All data has been obtained from the Securities and Exchange Board of India')
        st.write('https://sebi.gov.in/sebiweb/other/OtherAction.do?doPmr=yes')
        st.write('Only discretionary services were taken into account')

    if data_processing_flag:
        st.title('Data Processing')
        st.write('All data has been processed in Python.')
        st.write('Where needed, risk free rate was taken as 6.24%, the 10 year government bond yield at time of writing')
        st.write('SEBI lists over 900 portfolio management services. Some of these are duplicated entries.')
        st.write('Most of the managers have not reported data in 2021, this app only considers those which have.')
        st.write('Managers with over 20% return for more than 4 months have been removed. '
                 'These were generally incorrect entries.')
        st.write('SEBI stopped reporting returns from September 2020 to March 2021. Returns for these times have '
                 'been estimated using CAPM')
        st.write('Processing functions and data are openly available at')
        st.write('https://github.com/shah-meet0/pmsanalysis')

    if data_validity_flag:
        st.title('Data Validity')
        st.write('SEBI most likely has some incorrect data. For instance, India Bulls Asset Management was '
                 'reported to have nearly 8% return every month in 2018, which is not what their website reports.')
        st.write('As such take some data (especially those with higher annualized return) with a grain of salt')
        st.write('Also, floating point errors cause some imprecision in wealth calculation.')

    if contact_me_flag:
        st.title('About Me')
        st.write('Hi! I am Meet Shah!')
        st.write('I am an Econometrics and Mathematical Economics Student at LSE.')
        st.write('To contact me with suggestions or desired features, please use the following email address:')
        st.write('meetsamshah@gmail.com')

    if not hide_data_flag:
        st.title("Portfolio Management Services")
        st.write('An investment instrument in India')
        st.write("Click on column header to sort by it")
        st.dataframe(analysed_data.style.background_gradient(cmap='gist_gray', axis=0).format(precision=3))
        fig, (ax1, ax2) = plt.subplots(1, 2)

        ax1.hist(analysed_data['Ann_Ret'] * 100, color='Red')
        ax1.set_title('Annualized Return (%)')
        ax1.set_xlim((-50, 51))
        ax1.set_ylabel('Frequency')

        ax2.hist(analysed_data['Ann_Vol'] * 100)
        ax2.set_title('Annualized Volatility (%)')

        fig.set_facecolor('#F0F0F5')

        st.pyplot(fig)

else:
    on_manager_selection(manager, analysed_data, monthly_data, index_returns)
