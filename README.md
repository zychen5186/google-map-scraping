# google-scraping

hsun_main.py -> url放搜尋某範圍裡某種類（e.g.公園）的連結，輸出為範圍內的地標名稱及地址
main.py ->url放某地標的連結，輸出為名稱、評分、平價數、地址、營業時間、熱門時段、評價（未完成）

以下紀錄一些實作時遇到的問題：
1.find_element後面參數的空格都要改成"."
2.Message: no such element: Unable to locate element:
    (1)常常是因為沒有讓頁面跳到該element出現的畫面，所以抓不到element。
    (2)或者find的時候該element還沒load出來，可用WebDriverWait來確保已載入完成
3.用driver.execute_script操縱畫面沒反應，可能是參數內的目標element抓錯，但有時候看不出來只能多試幾個element看看。
4.get element的時候輸入的標籤參數，可以該標籤的空格為分隔，輸入部分標籤，若沒有空格的話不能把標籤截斷。

* google map 驅動程式\
若不確定該安裝哪個版本，在終端機中輸入

        pip install webdriver_manager
        
import後作為webdriver.Chrome()的參數，ChromeDriverManager().install()每次根據電腦來抓驅動程式

        driver = webdriver.Chrome(ChromeDriverManager().install(), options=self.options)

