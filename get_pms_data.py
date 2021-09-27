import selenium.common.exceptions
from selenium import webdriver
import time
import pandas as pd
from selenium.webdriver.support.ui import Select

'''
Module uses Selenium to scrap data from Securities and Exchanged Board of India website. 
Potential application would be to concurrently run several classes, and then merge the output.
'''


class PmsImporter:

    def __init__(self, driver_loc):
        self.driver = webdriver.Chrome(driver_loc)
        self.website = 'https://www.sebi.gov.in/sebiweb/other/OtherAction.do?doPmr=yes'
        self.months = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6, 'July': 7, 'August': 8,
                       'September': 9, 'October': 10, 'November': 11, 'December': 12}

    class NoRecordFoundException(Exception):
        pass

    def get_all_data(self, years, filepath):
        '''

        :param years: An array containing the years for which the data is to be scrapped
        :param filepath: Location where the obtained data will be stored.
        :return: Dataframe containing the obtained data

        NOTE: Very unstable with regards to internet connectivity, and also takes time.
        Error handlers will show what data might be missing from final product.
        '''
        entries = []
        num_managers = self.get_manager_length()
        for manager in range(2, num_managers + 1):
            for year in years:
                for month in range(1, 13):
                    try:
                        manager_select = Select(self.driver.find_element_by_xpath("//*[@id='2']/div[1]/select"))
                        manager_select.select_by_index(manager)
                        manager_name = manager_select.first_selected_option.text

                        year_select = Select(self.driver.find_element_by_xpath('//*[@id="2"]/div[2]/select'))
                        year_select.select_by_value(str(year))

                        month_select = Select(self.driver.find_element_by_xpath('//*[@id="2"]/div[3]/select'))
                        month_select.select_by_value(str(month))
                        month_name = month_select.first_selected_option.text

                        go_button = self.driver.find_element_by_xpath('//*[@id="2"]/div[4]/div/a')
                        go_button.click()
                        data_tuple = self.get_data(year, month)
                        if data_tuple[0] == 0:
                            break
                        new_entry = [manager_name, int(year), month_name, *data_tuple]
                        entries.append(new_entry)

                    except self.NoRecordFoundException as e:
                        print(manager_name, str(year), month_name, e)
                        if month > 6:
                            print('Skipping rest of year')
                            break

                    except selenium.common.exceptions.NoSuchElementException:
                        print(str(manager), str(year), str(month), 'failed to load or does not have all data.')
                        self.driver.refresh()
                        self.driver.get(self.website)

                    except Exception:
                        # Sometimes page won't load because of buggy website, this handler will print out
                        # when you might need to manually add a couple of entries.
                        self.driver.refresh()
                        self.driver.get(self.website)
                        print(str(manager), str(month), 'had to be refreshed')

        df = pd.DataFrame(data=entries, columns=['Manager Name', 'Year', 'Month', 'AUM (crs)',
                                                 'Turnover Ratio', 'Return'])
        df.to_csv(filepath)
        time.sleep(10)
        self.quit()
        return df

    def get_data_for_month(self, month, year):
        entries = []
        num_managers = self.get_manager_length()
        for manager in range(2, num_managers + 1):
            try:
                manager_select = Select(self.driver.find_element_by_xpath("//*[@id='2']/div[1]/select"))
                manager_select.select_by_index(manager)
                manager_name = manager_select.first_selected_option.text

                year_select = Select(self.driver.find_element_by_xpath('//*[@id="2"]/div[2]/select'))
                year_select.select_by_value(str(year))

                month_select = Select(self.driver.find_element_by_xpath('//*[@id="2"]/div[3]/select'))
                month_select.select_by_value(str(month))
                month_name = month_select.first_selected_option.text

                go_button = self.driver.find_element_by_xpath('//*[@id="2"]/div[4]/div/a')
                go_button.click()
                data_tuple = self.get_data(year, month)
                new_entry = [manager_name, int(year), month_name, *data_tuple]
                entries.append(new_entry)

            except self.NoRecordFoundException as e:
                print(manager_name, str(year), month_name, e)

            except selenium.common.exceptions.NoSuchElementException:
                print(str(manager), str(year), str(month), 'failed to load or does not have all data.')
                self.driver.refresh()
                self.driver.get(self.website)

            except Exception:
                # Sometimes page won't load because of buggy website, this handler will print out
                # when you might need to manually add a couple of entries.
                self.driver.refresh()
                self.driver.get(self.website)
                print(str(manager), str(month), 'had to be refreshed')
        df = pd.DataFrame(data=entries, columns=['Manager Name', 'Year', 'Month', 'AUM (crs)',
                                                 'Turnover Ratio', 'Return'])
        time.sleep(10)
        self.quit()
        return df

    def get_data_for_year(self, manager: int, year):
        entries = []
        for month in range(1, 13):
            try:
                manager_select = Select(self.driver.find_element_by_xpath("//*[@id='2']/div[1]/select"))
                manager_select.select_by_index(manager)
                manager_name = manager_select.first_selected_option.text

                year_select = Select(self.driver.find_element_by_xpath('//*[@id="2"]/div[2]/select'))
                year_select.select_by_value(str(year))

                month_select = Select(self.driver.find_element_by_xpath('//*[@id="2"]/div[3]/select'))
                month_select.select_by_value(str(month))
                month_name = month_select.first_selected_option.text

                go_button = self.driver.find_element_by_xpath('//*[@id="2"]/div[4]/div/a')
                go_button.click()
                data_tuple = self.get_data(year, month)
                new_entry = [manager_name, int(year), month_name, *data_tuple]
                entries.append(new_entry)

            except self.NoRecordFoundException as e:
                print(manager_name, str(year), month_name, e)

            except selenium.common.exceptions.NoSuchElementException:
                print(str(manager), str(year), str(month), 'failed to load or does not have all data.')
                self.driver.refresh()
                self.driver.get(self.website)

            except Exception:
                # Sometimes page won't load because of buggy website, this handler will print out
                # when you might need to manually add a couple of entries.
                self.driver.refresh()
                self.driver.get(self.website)
                print(str(manager), str(month), 'had to be refreshed')
        df = pd.DataFrame(data=entries, columns=['Manager Name', 'Year', 'Month', 'AUM (crs)',
                                                 'Turnover Ratio', 'Return'])
        time.sleep(10)
        self.quit()
        return df

    def get_manager_length(self):
        self.driver.get(self.website)
        select_box = Select(self.driver.find_element_by_xpath("//*[@id='2']/div[1]/select"))
        return len(select_box.options)

    def manager_id_maker(self, filepath):
        num_managers = self.get_manager_length()
        manager_select = Select(self.driver.find_element_by_xpath("//*[@id='2']/div[1]/select"))
        entries = []
        options = manager_select.options
        for i in range(2, num_managers+1):
            # entries.append([manager_select.select_by_index(i), i])
            entries.append([options[i-1].text, i])
        df = pd.DataFrame(data=entries, columns= ['Manager Name', 'Manager ID'])
        df.set_index('Manager ID', inplace= True)
        df.to_csv(filepath)
        return df

    def get_entry(self, manager: int, year, month: str, **kwargs):
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
        try:
            data_tuple = self.get_data(year, month_number)
            entry = [[manager_name, year, month, *data_tuple]]
            df = pd.DataFrame(data=entry,
                              columns=['Manager Name', 'Year', 'Month', 'AUM (crs)', 'Turnover Ratio', 'Return'])
            for key, value in kwargs.items():
                if key == 'filepath':
                    df.to_csv(value, mode='a', header=False)
            return df
        except Exception as e:
            print(manager_name, year, month, e)

    def get_data(self, year, month):
        nrf = 'No Records Found.'
        if self.driver.find_element_by_xpath('//*[@id="member-wrapper"]/section/div[3]').text == nrf:
            raise self.NoRecordFoundException(nrf)

        if isinstance(month, str):
            month = self.months[month]
        if isinstance(year, str):
            year = int(year)
        if (year == 2020 and month > 8) or year > 2020:
            return self.get_new_data()
        else:
            return self.get_old_data()

    def get_new_data(self):
        assets_under_management = float(self.driver.find_element_by_xpath('//*[@id="newPMR2021"]/div['
                                                                          '13]/div/table/tbody/tr[2]/td[8]').text)
        month_return = float(self.driver.find_element_by_xpath('//*[@id="newPMR2021"]/div[21]/div/table/tbody/'
                                                               'tr[1]/td[3]').text)
        turnover_ratio = float(self.driver.find_element_by_xpath('//*[@id="newPMR2021"]/div[19]/div/table/tbody/tr[3]'
                                                                 '/td[3]').text)
        return assets_under_management, turnover_ratio, month_return

    def get_old_data(self):
        ind_resident = float(self.driver.find_element_by_xpath(
            '//*[@id="member-wrapper"]/section/div[4]/div/table/tbody/tr[4]/td[11]').text)
        ind_non_resident = float(self.driver.find_element_by_xpath(
            '//*[@id="member-wrapper"]/section/div[4]/div/table/tbody/tr[5]/td[11]').text)
        corp_resident = float(self.driver.find_element_by_xpath(
            '//*[@id="member-wrapper"]/section/div[4]/div/table/tbody/tr[6]/td[11]').text)
        corp_non_resident = float(self.driver.find_element_by_xpath(
            '//*[@id="member-wrapper"]/section/div[4]/div/table/tbody/tr[7]/td[11]').text)
        corp_fii = float(self.driver.find_element_by_xpath(
            '//*[@id="member-wrapper"]/section/div[4]/div/table/tbody/tr[8]/td[11]').text)

        assets_under_management = ind_resident + ind_non_resident + corp_resident + corp_non_resident + corp_fii
        turnover_ratio = float(self.driver.find_element_by_xpath(
            '//*[@id="member-wrapper"]/section/div[6]/div/table/tbody/tr/td[3]').text)
        month_return = float(self.driver.find_element_by_xpath(
                            '//*[@id="member-wrapper"]/section/div[6]/div/table/tbody/tr/td[4]').text)
        return assets_under_management, turnover_ratio, month_return

    def quit(self):
        self.driver.quit()


