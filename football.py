from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
import pandas as pd
website = 'https://www.adamchoi.co.uk/overs/detailed'
path = 'G:/Program Files/chromedriver_win32/chromedriver.exe'
driver=webdriver.Chrome(executable_path=path)
driver.get(website)

all_match_button = driver.find_element_by_xpath('//label[@analytics-event="All matches"]')
all_match_button.click()


dropdown = Select(driver.find_element_by_xpath('//select[1]'))
dropdown.select_by_visible_text('Spain')

time.sleep(3)
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
driver.quit()

df=pd.DataFrame({'date':date,'home':home,'score':score,'away':away})
df.to_csv('football.csv',index=False)