from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as pd

class Scrapepage:
    def __init__(self, url):
        self.url = url
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 20)
        self.alldata = []

    def scrape_data(self):
        try:
            # Wait for routes to load
            routescontainer = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "route_link")))

            for route in routescontainer:
                try:
                    routename = route.find_element(By.CLASS_NAME, "route").text
                    routelink = route.find_element(By.TAG_NAME, "a").get_attribute("href")
                    self.alldata.append({'routename': routename, 'routelink': routelink})
                except Exception as e:
                    print(f"An error occurred while extracting route data: {e}")
                    continue
        except Exception as e:
            print(f"Error while scraping data: {e}")

    def navigation_page(self):
        self.driver.get(self.url)

        for pn in range(1, 6):  # Adjust for the number of pages
            print(f"Scraping page {pn}")
            self.scrape_data()

            if pn < 5:
                try:
                    # Wait for pagination container to be present
                    pagination_container = self.wait.until(EC.presence_of_element_located(
                        (By.XPATH, '//*[@id="root"]/div/div[4]/div[12]')
                    ))
                    # Locate and click the next page button
                    next_page_button = pagination_container.find_element(
                        By.XPATH, f'.//div[contains(@class, "DC_117_pageTabs") and text()="{pn + 1}"]'
                    )
                    actions = ActionChains(self.driver)
                    actions.move_to_element(next_page_button).perform()
                    next_page_button.click()

                    # Wait for the page to change
                    self.wait.until(EC.text_to_be_present_in_element(
                        (By.XPATH, '//div[contains(@class, "DC_117_pageTabs DC_117_pageActive")]'),
                        str(pn + 1)
                    ))
                    print(f"Navigated to page {pn + 1}")
                    time.sleep(3)  # Ensure all elements are loaded
                except Exception as e:
                    print(f"Error navigating to page {pn + 1}: {e}")
                    break

    def save_to_csv(self, file_name="TSRTC_Routes.csv"):
        try:
            df = pd.DataFrame(self.alldata)
            df.to_csv(file_name, index=False)
            print(f"Data saved to {file_name}")
        except Exception as e:
            print(f"Error saving data to CSV: {e}")

    def close(self):
        self.driver.quit()


# Initialize and run
page = Scrapepage('https://www.redbus.in/online-booking/jksrtc')
page.navigation_page()
page.save_to_csv('C:/Users/sanji/Desktop/RedBusProject/RouteData/JKSRTC_Routes.csv')
page.close()
