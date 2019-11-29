# -*- coding: utf-8 -*-
"""
Created on Wed Aug 21 13:13:13 2019

@author: DPulido
"""
#import selenium
from selenium import webdriver
import pandas as pd
import numpy as np
import time 
import datetime as dt
from datetime import datetime
import config

driver = webdriver.Chrome()
time.sleep(2)

# Open the website
driver.get('https://dro.orange-business.com/authentification?target=https://m2mexpress.sp.orange-business.com/mac/customer/home.do&codeContexte=malima_osp_en')
 
id_box = driver.find_element_by_name('user')
pass_box = driver.find_element_by_name('pwd')

id_box.send_keys(config.username)
pass_box.send_keys(config.password)

# Click login
login_button = driver.find_element_by_id('submit-button')
login_button.click()

time.sleep(2)

driver.get('https://m2mexpress.sp.orange-business.com/mac/customer/fleet/fleet.do')

totalpages=driver.find_element_by_id('pagingTotalPages')
totalpages=int(totalpages.text)
print (totalpages)

dfT= pd.DataFrame(columns=['line', 'state', 'date'])

totalpages=3 #he limitado a 3 paginas el scraping ya que en total son 379

for page in range(totalpages):
    print(page)

    driver.get('https://m2mexpress.sp.orange-business.com/mac/customer/fleet/fleet.do?pageIndex='+str(page)+'&selectedSubIds=')
    
    lines = driver.find_elements_by_xpath("""//*[@id="subData"]/tbody/tr/td[2]/a""")
    date = driver.find_elements_by_xpath("""//*[@id="subData"]/tbody/tr/td[5]/a""")
    status = driver.find_elements_by_xpath("""//*[@id="subData"]/tbody/tr/td[4]/a""")
    
    capitalizer = lambda x: x.text
    linelist = list(map(capitalizer, lines)); linelist
    datelist = list(map(capitalizer, date)); datelist
    statuslist = list(map(capitalizer, status)); statuslist

    df=pd.DataFrame({'line':linelist,'state':statuslist,'date':datelist})

    dfT=pd.concat([dfT, df], ignore_index=True)
dfT['line']=dfT['line'].str.slice(3, 15)

print (dfT)
export_csv = dfT.to_csv (r'C:\Users\David\Desktop\export_dataframe.csv', index = None, header=True)

