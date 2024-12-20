from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as pd

class RebusScrap:
    def __init__(self):
        self.driver=webdriver.Chrome()
        self.wait=WebDriverWait(self.driver,30)
        self.alldata=[]
    def button(self):
        try:
            WebDriverWait(self.driver,30).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,"div[class='button']")))
            b=self.driver.find_elements(By.CSS_SELECTOR,"div[class='button']")   
            for i in range(len(b)-1,-1,-1):
                b[i].click()
        except Exception as e:
            print(e)
    def Scroll(self):
        scroll_limit=1000
        for _ in range(scroll_limit):
            self.driver.execute_script('scrollBy(0,100)')
    
    def ScrapeBus_details(self,fromlocation,tolocation,links):
        try:
            self.wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME,"bus-item")))
            try:
                buscontainer=self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME,"bus-item")))
                if not buscontainer:
                    self.alldata.append({'From':fromlocation,'To':tolocation,'Bus_Name':'NA','Bus_Type':'NA','Bus_Dept':'NA','Bus_Arrival':'NA','Duration':'NA','Rating':'NA','Price':'NA','Seats':'NA'})
                else:
                    for bus in buscontainer:
                        busname=bus.find_element(By.CLASS_NAME,'travels').text
                        bustype=bus.find_element(By.CLASS_NAME,'bus-type').text
                        busdept=bus.find_element(By.CLASS_NAME,'dp-time').text
                        busarrival=bus.find_element(By.CLASS_NAME,'bp-time').text
                        busdur=bus.find_element(By.CLASS_NAME,'dur').text
                        rating=bus.find_element(By.XPATH, "//div[@class='rating-sec lh-24']").text
                        price=bus.find_element(By.CLASS_NAME,'fare').text
                        seats=bus.find_element(By.CLASS_NAME,'seat-left').text
                        self.alldata.append({'From':fromlocation,'To':tolocation,'Link':links,'Bus_Name':busname,'Bus_Type':bustype,'Bus_Dept':busdept,'Bus_Arrival':busarrival,'Duration':busdur,'Rating':rating,'Price':price,'Seats':seats})
            except Exception as e:
                print(f"No buses found or error occurred for route {fromlocation} to {tolocation}: {e}")
        except Exception as e:
            print(f"No buses found or error occurred for route {from_location} to {to_location}: {e}")
    def Savedata(self,file='BusDetail.csv'):
        df=pd.DataFrame(self.alldata)
        print(df)
        df.to_csv(f"{file}")

urls=['https://www.redbus.in/bus-tickets/delhi-to-srinagar',
'https://www.redbus.in/bus-tickets/jammu-to-katra',
'https://www.redbus.in/bus-tickets/katra-to-jammu'



]
scrape=RebusScrap()
try:
    for i in urls:
        parts = i.split("/")[-1].split("-to-")
        from_location = parts[0].replace("-", " ").title()
        to_location = parts[1].replace("-", " ").title()
        print(i)
        scrape.driver.get(i)
        scrape.button()
        scrape.Scroll()
        scrape.ScrapeBus_details(from_location,to_location,i)
    scrape.Savedata('JKSRTC_Bus.csv')
except Exception as e:
    print(e)


