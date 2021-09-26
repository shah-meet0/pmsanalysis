from selenium import webdriver
import time
import pandas as pd
from selenium.webdriver.support.ui import Select


class PmsImporter:

    def __init__(self, driver_loc):
        self.driver = webdriver.Chrome(driver_loc)
        self.website = 'https://www.sebi.gov.in/sebiweb/other/OtherAction.do?doPmr=yes'
        self.months = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6, 'July': 7, 'August': 8,
                     'September': 9, 'October': 10, 'November': 11, 'December': 12}

    def get_after_data(self):
        df = pd.DataFrame(columns=['Manager Name', 'Year', 'Month', 'AUM (crs)', 'Turnover Ratio', 'Return'])
        self.driver.get(self.website)
        self.quit()

    def get_manager_length(self):
        self.driver.get(self.website)
        select_box = Select(self.driver.find_element_by_xpath("//*[@id='2']/div[1]/select"))
        return len(select_box.options) - 1

    def new_get_entry(self, filepath, manager, year, month):
        df = pd.DataFrame(columns=['Manager Name', 'Year', 'Month', 'AUM (crs)', 'Turnover Ratio', 'Return'])

        self.driver.get(self.website)
        month_number = self.months[month]
        manager_select = Select(self.driver.find_element_by_xpath("//*[@id='2']/div[1]/select"))
        manager_select.select_by_index(manager)
        manager_name = manager_select.first_selected_option.text
        year_select = Select(self.driver.find_element_by_xpath('//*[@id="2"]/div[2]/select'))
        year_select.select_by_value(str(year))
        month_select = Select(self.driver.find_element_by_xpath('//*[@id="2"]/div[3]/select'))
        month_select.select_by_value(str(month_number))
        go_button = self.driver.find_element_by_xpath('//*[@id="2"]/div[4]/div/a')
        go_button.click()

    def get_new_data(self):
        aum = float(self.driver.find_element_by_xpath('//*[@id="newPMR2021"]/div[15]/div/table/tbody/tr[2]/th[13]').
                    text)




    def quit(self):
        self.driver.quit()
