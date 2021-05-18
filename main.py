from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager#會自動幫忙抓符合電腦版本的chrome驅動程式

import time
import os

class WebDriver:

    location_data = {}

    def __init__(self):
        self.PATH = "chromedriver"
        self.options = Options()
        # self.options.binary_location = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"
        self.options.add_argument("--headless")#加此參數driver會在背景執行，不會另開一個視窗
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=self.options)

        self.location_data["rating"] = 0
        self.location_data["reviews_count"] = 0
        self.location_data["location"] = "NA"
        self.location_data["contact"] = "NA"
        self.location_data["Time"] = {"星期一":"NA", "星期二":"NA", "星期三":"NA", "星期四":"NA", "星期五":"NA", "星期六":"NA", "星期日":"NA"}
        self.location_data["Reviews"] = []
        self.location_data["Popular Times"] = {"星期一":[], "星期二":[], "星期三":[], "星期四":[], "星期五":[], "星期六":[], "星期日":[]}

    def click_open_close_time(self):
        #原先營業時間表未展開，webdriver沒辦法找到裡面的資訊，用此func點開
        if(len(list(self.driver.find_elements_by_class_name("mapsConsumerUiSubviewSectionOpenhours__section-open-hours-button-right.section-open-hours-button.mapsConsumerUiSubviewSectionOpenhours__expand-more")))!=0):
            element = self.driver.find_element_by_class_name("mapsConsumerUiSubviewSectionOpenhours__section-open-hours-button-right.section-open-hours-button.mapsConsumerUiSubviewSectionOpenhours__expand-more")
            self.driver.implicitly_wait(5)
            ActionChains(self.driver).move_to_element(element).click(element).perform()

    def click_all_reviews_button(self):

        try:
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "mapsConsumerUiSubviewSectionGm2Button__button.mapsConsumerUiSubviewSectionGm2Button__button-text")))
            element = self.driver.find_elements_by_class_name("mapsConsumerUiSubviewSectionGm2Button__button.mapsConsumerUiSubviewSectionGm2Button__button-text")#這個class明明只屬於“更多評論”,但不知道為什麼直接用find_element第一個都會找到“提出修改意見".....處理超久找不到解答，只好一次取整個list再取"更多評論"的index
            print(element[1].text)
            element[1].click()
        except Exception as e:
            print(e)
            self.driver.quit()
            return False

        return True

    def get_location_data(self):

        try:
            avg_rating = self.driver.find_element_by_class_name("section-star-array")
            total_reviews = self.driver.find_element_by_class_name("widget-pane-link")
            address = self.driver.find_element_by_css_selector("[data-item-id='address']")
            phone_number = self.driver.find_element_by_css_selector('[data-tooltip="複製電話號碼"]')
        except:
            pass
        #若aria-hideden attribute為false（如電話號碼）, 沒辦法直接用.text來獲得文字內容, 可用is_displayed()確認
        try:
            self.location_data["rating"] = float((avg_rating.get_attribute("aria-label")).split()[0])
            self.location_data["reviews_count"] = int((total_reviews.text).split()[0].replace(",",""))
            self.location_data["location"] = address.text
            self.location_data["contact"] = phone_number.get_attribute("aria-label").strip("電話號碼: ")#待解：跟location一樣都是用css_selector找，但contact用.text抓不到電話號碼，只能抓aria-label
        except Exception as e:
            print(e)
            pass


    def get_location_open_close_time(self):

        try:
            days = self.driver.find_elements_by_class_name("mapsConsumerUiSubviewSectionOpenhoursOpenhoursrow__row-header")
            times = self.driver.find_elements_by_class_name("mapsConsumerUiSubviewSectionOpenhoursOpenhoursrow__row-data")
            day = [a.text for a in days]
            
            open_close_time = [a.text.replace("\n",", ") for a in times]
            
            for i, j in zip(day, open_close_time):
                self.location_data["Time"][i] = j
        
        except Exception as e:
            print(e)
            pass

    def get_popular_times(self):
        try:
            a = self.driver.find_elements_by_class_name("section-popular-times-graph")
            #google map預設顯示星期一，但HTML源碼中是從星期日開始寫，find_elements會照順序擷取
            dic = {0:"星期日", 1:"星期一", 2:"星期二", 3:"星期三", 4:"星期四", 5:"星期五", 6:"星期六"}
            l = {"星期日":[], "星期一":[], "星期二":[], "星期三":[], "星期四":[], "星期五":[], "星期六":[]}
            count = 0

            for i in a:
                b = i.find_elements_by_class_name("section-popular-times-bar")
                for j in b:
                    x = j.get_attribute("aria-label")
                    l[dic[count]].append(x)
                count = count + 1

            for i, j in l.items():
                self.location_data["Popular Times"][i] = j
        
        except Exception as e:
            print(e)
            pass

    def scroll_the_page(self):
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "section-layout-root")))

            pause_time = 2
            max_count = 5
            x = 0
            while(x<max_count):
                scrollable_div = self.driver.find_element_by_css_selector('div.section-layout.section-scrollbox.mapsConsumerUiCommonScrollable__scrollable-y.mapsConsumerUiCommonScrollable__scrollable-show')
                try:
                    self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scrollable_div)
                except:
                    pass
                time.sleep(pause_time)
                x=x+1
        
        except Exception as e:
            print(e)
            self.driver.quit()

    def expand_all_reviews(self):
        try:
            element = self.driver.find_elements_by_class_name("mapsConsumerUiSubviewSectionReview__section-expand-review")
            for i in element:
                i.click()
        
        except Exception as e:
            print(e)
            pass

    def get_reviews_data(self):
        try:
            review_names = self.driver.find_elements_by_class_name("section-review-title")
            review_text = self.driver.find_elements_by_class_name("section-review-review-content")
            review_dates = self.driver.find_elements_by_css_selector("[class='section-review-publish-date']")
            review_stars = self.driver.find_elements_by_css_selector("[class='section-review-stars']")

            review_stars_final = []

            for i in review_stars:
                review_stars_final.append(i.get_attribute("aria-label"))

            review_names_list = [a.text for a in review_names]
            review_text_list = [a.text for a in review_text]
            review_dates_list = [a.text for a in review_dates]
            review_stars_list = [a for a in review_stars_final]

            for (a,b,c,d) in zip(review_names_list, review_text_list, review_dates_list, review_stars_list):
                self.location_data["Reviews"].append({"name":a, "review":b, "date":c, "rating":d})

        except Exception as e:
            print(e)
            pass

    def scrape(self, url):
        try:
            
            self.driver.get(url)
        
            print("SUCCEEDED")
        except Exception as e:
            print("ERROR OCCURED")
            print(e)
            self.driver.quit()
            #continue
        time.sleep(10)
        self.click_open_close_time()
        print("1")
        self.get_location_data()
        print("2")
        self.get_location_open_close_time()
        print("3")
        self.get_popular_times()
        self.click_all_reviews_button()
        time.sleep(10)
        self.scroll_the_page()
        print("4")
        self.expand_all_reviews()
        print("5")
        self.get_reviews_data()
        print("6")
        self.driver.quit()

        return(self.location_data)

url = "https://www.google.com.tw/maps/place/%E5%A3%BD%E5%8F%B8%E7%88%B8/@25.0196117,121.5470822,16z/data=!4m14!1m8!3m7!1s0x0:0x3e0b9289c979b221!2z5p-R5qmYU2hpbm4gLSDptKjolKU!8m2!3d25.0231373!4d121.5544957!9m1!1b1!3m4!1s0x3442aa30ef55d3a9:0xac5581fca078b0dd!8m2!3d25.0221477!4d121.553631?hl=zh-TW&authuser=0"
x = WebDriver()
print(x.scrape(url))