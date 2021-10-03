import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


data = pd.read_csv('return analysis.csv')
data.drop(data.columns[0], axis= 1, inplace = True)
datafile = pd.read_csv('final pms data1.csv')
data['Ann_Ret'] = data['Ann_Ret']*100
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
st.write('All returns are in %')
list_of_options = []
managers = datafile['Manager Name'].unique()
for manager in managers:
    list_of_options.append(manager)
list_of_options.sort()    
option = st.sidebar.selectbox('Manager', ['All'] + list_of_options)
if option == 'All':
    st.write("Click on column header to sort by it")
    st.dataframe(data.style.background_gradient(cmap = 'Blues', axis= 0))
    st.write('All data has been obtained from the Securities and Exchange Board of India. There are sometimes mistakes done by them in data collection, which affects the statistics presented. I have removed some obvious outliers, but there still might be mistakes. Please keep this in mind when viewing say the highest annualized return.')
else:
    data = data[data['Manager']==option]
    datafile = datafile[datafile['Manager Name']==option]
    st.dataframe(data)
    st.dataframe(datafile)
    entry_1 = 1000 * (1+ (datafile['Return'].iloc[0])/100)
    wealth = [entry_1]
    length = datafile['Return'].size
    for i in range(1,length):
        wealth.append(wealth[-1] * (1+ (datafile['Return'].iloc[i])/100))
    datafile['Wealth'] = wealth
    fig, axs = plt.subplots()
    datafile.plot(x='Date', y = 'Wealth', ax = axs)
    d1 = datafile['Date'].iloc[0]
    d2 = datafile['Date'].iloc[-1]
    st.pyplot(fig)
    st.write('From ' + d1 + ' to '+ d2 + ', Rupees 1000 would become Rupees ' + "{:.2f}".format(wealth[-1]))