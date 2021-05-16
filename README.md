# google-scraping

* google map 驅動程式\
若不確定該安裝哪個版本，在終端機中輸入

        pip install webdriver_manager
import後利用ChromeDriverManager().install()每次根據電腦來抓驅動程式

        driver = webdriver.Chrome(ChromeDriverManager().install(), options=self.options)


