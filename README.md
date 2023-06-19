# pmsanalysis
## [Website](https://pms-data.streamlit.app/)

## Purpose
The purpose of this project is to assimilate, analyse and present data on Portfolio Management Services in India. Portfolio Management Services are investment instruments
where the consumer has ownership of the securities in the portfolio, but the decisions are made partly or completely by a professional investment manager. This project
takes into account discretionary Portfolio Management Services, where all the decisions are made by the portfolio manager itself.

## Contents of Repository

* [Resources](./Resources): Folder contains all the data files which are used to present the data shown on the webApp. 
* [get_pms_data](./get_pms_data.py): Contains a class which uses Selenium to grab data from the [Securities and Exchange Board of India](https://www.sebi.gov.in/sebiweb/other/OtherAction.do?doPmr=yes), and then make it into a Pandas dataframe.
* [analyse_pms_data](./analyse_pms_data.py): Contains three classes:
  - PmsReformatter: Reformats the data obtained from get_pms_data to be better suited for further analysis.
  - PmsCleaner: Cleans the data obtained by removing managers with not enough entries, duplicated entries or managers who have stopped reporting data.
  - PmsAnalyser: Gets summary statistics for all managers, and saves it into a new dataframe. 
* [updatemonth.py](./updatemonth.py): Contains a routine to update the entire database each month when new data is reported.
* [risk_measures.py](./risk_measures.py): Contains functions to get summary statistics like annualized mean, volatility, skewness, kurtosis and other methods like the ordinary least squares. 
* [pmsstreamlit.py](./pmsstreamlit.py): Uses streamlit to construct a webapp to display the analysed data. 

