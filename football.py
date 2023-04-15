from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
import logging
from selenium.webdriver.remote.remote_connection import LOGGER
from pathlib import Path
import os
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


LOGGER.setLevel(logging.CRITICAL)
#logger = logging.getLogger(__name__)
#logger.setLevel(logging.CRITICAL)
website = 'https://www.adamchoi.co.uk/overs/detailed'
path = 'C:/Program Files/chromedriver_win32/chromedriver.exe'
option= Options()
option.headless=True
option.add_argument('window-size=1920x1080')
driver=webdriver.Chrome(executable_path=path,options=option)
driver.get(website)



dropdown = Select(WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH,'//select[1]'))))
#dropdown = Select(driver.find_element_by_xpath('//select[1]'))
l=dropdown.options
country = []
for d in l:
    country.append(d.text)

def scrape(country):
    all_match_button = driver.find_element_by_xpath('//label[@analytics-event="All matches"]')
    all_match_button.click()
    print('scraping')
    dropdown.select_by_visible_text(country)
    dropdown2 = Select(WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH,'//*[@id="league"]'))))
    #dropdown2 = Select(driver.find_element_by_xpath('//*[@id="league"]'))
    lg=dropdown2.options
    leagues = []
    for d in lg:
        leagues.append(d.text)
    #time.sleep(3)

    for league in leagues:
        dropdown2.select_by_visible_text(league)
        #time.sleep(0.5)
        dropdown3 = Select(WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH,'//*[@id="season"]'))))
        #dropdown3 = Select(driver.find_element_by_xpath('//*[@id="season"]'))
        ss=dropdown3.options
        seasons=[]
        for s in ss:
            seasons.append(s.text)

        for season in seasons:
            dropdown3.select_by_visible_text(season)
            time.sleep(2)

            print(f'{country},{league},{season}')

            matches = driver.find_elements_by_tag_name('tr')

            date=[]
            home=[]
            score=[]
            away=[]
            i=0
            for match in matches:
                i += 1
                date.append(match.find_element_by_xpath('./td[1]').text)
                home.append(match.find_element_by_xpath('./td[2]').text)
                score.append(match.find_element_by_xpath('./td[3]').text)
                away.append(match.find_element_by_xpath('./td[4]').text)
                print(i)
            
            
            fname = f"./Data/{country}_{league}_{season.replace('/','-')}"+".csv"
            print(fname)
            #ofpath.parent.mkdir(parents=True,exist_ok=True)
            df=pd.DataFrame({'date':date,'home':home,'score':score,'away':away})
            print(df)
            time.sleep(3)
            df.to_csv(fname,index=False)


for c in country:
    scrape(c)

driver.quit()



