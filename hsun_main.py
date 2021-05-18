from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager#會自動幫忙抓符合電腦版本的chrome驅動程式
from openpyxl import Workbook
import re

import time
import os

class WebDriver:

    location_data = {}

    def __init__(self):
        self.PATH = "chromedriver"
        self.options = Options()
        # self.options.binary_location = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"
        self.options.add_argument("--headless")#加此參數driver會在背景執行，不會另開一個視窗
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options = self.options)

        self.location_data["name"] = []
        self.location_data["location"] = []

    def get_scale(self):
        print("獲取比例尺")
        try:
            scale = int(self.driver.find_element_by_id('widget-scale-label').text.split()[0])
            print(scale)
        except Exception as e:
            print(e)
            pass     
        return(scale)
      
    # def get_location_data(self,ws,count):
    #     print("獲取地點資訊")
    #     try:
    #         buttons = self.driver.find_elements_by_class_name("place-result-container-place-link")
    #         for i in range(len(buttons)):
    #             buttons[i].click()
    #             WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="pane"]/div/div[1]/div/div/div[4]/div[1]')))
            
    #     except Exception as e:
    #         print(e)
    #         pass                 
    
    def get_location_data(self,ws,count):
        print("獲取地點資訊")
        try:
            names = self.driver.find_elements_by_class_name("place-result-container-place-link")
            addresses = self.driver.find_elements_by_class_name("mapsConsumerUiSubviewSectionGm2Placesummary__text-content.gm2-body-2")

        except Exception as e:
            print(e)
            pass
        
        try:
            name_list = [a.get_attribute("aria-label") for a in names]
            print(name_list)
            address = [a.text for a in addresses]
            print(address)
            address_list = []
            for i in range(len(address)):
                if(len(re.split(" · |\n| · $\n| · $$\n", address[i])) < 4):
                    address_list.append("")
                else:
                    #print(re.split(" · |\n| · $\n| · $$\n", address[i]))
                    address_list.append(re.split(" · |\n| · $\n| · $$\n|$$", address[i])[3])
                    #不知為何沒辦法把 · $$\n當分界符號，後續如果有遇到其他分隔符號再自行添加
                    #暫時放棄...
            
            print(address_list)
            print(len(name_list),len(address))
            for a,b in zip(name_list, address_list):
                count += 1
                ws.append([count,a,b])
                self.location_data["name"].append(a)
                self.location_data["location"].append(b)
        except Exception as e:
            print(e)
            pass



    def scroll_the_page(self):
        print("滾動到底部")
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="pane"]/div/div[1]/div/div/div[4]/div[1]')))

            pause_time = 2
            max_count = 5
            x = 0
            while(x<max_count):
                
                try:
                    scrollable_div = self.driver.find_element_by_xpath('//*[@id="pane"]/div/div[1]/div/div/div[4]/div[1]')#一個卡很久的地方...要定位到正確的element，scroll的時候才會成功，用class_name很可能會定位到錯的element，如果script沒寫錯，很有可能是element沒定位對，總之多試幾個element才會知道哪個是對的。
                    self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scrollable_div)
                except Exception as e:
                    print(e)
                    pass
                time.sleep(pause_time)
                x=x+1
        
        except Exception as e:
            print(e)
            self.driver.quit()
        
    def click_next_page(self):
        print("下一頁")
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "mapsConsumerUiSubviewSectionGm2Pagination__section-pagination-button-next")))
            button = self.driver.find_element_by_id("mapsConsumerUiSubviewSectionGm2Pagination__section-pagination-button-next")
            button.click()
        except Exception as e:
            print(e)
            pass
        

    def scrape(self, url):
        count = 0
        wb = Workbook()
        ws = wb.active
        ws.append(["編號","名稱","地址"])
        try:
            self.driver.get(url)
            print("SUCCEEDED")
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'widget-scale-label')))
            scale = self.get_scale()
            new_scale = scale
        except Exception as e:
            print("ERROR OCCURED")
            print(e)
            #self.driver.quit()
            #continue
        while(scale == new_scale):
            self.scroll_the_page()
            self.get_location_data(ws,count)
            self.click_next_page()
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'widget-scale-label')))
            time.sleep(5)
            new_scale = self.get_scale()
            
        

        self.driver.quit()
        wb.save('google_map_scraping.xlsx')
        return(self.location_data)

url = "https://www.google.com.tw/maps/search/%E5%B7%A5%E5%BB%A0/@24.9981291,121.5503798,14z/data=!3m1!4b1?hl=zh-TW&authuser=0"
x = WebDriver()
x.scrape(url)