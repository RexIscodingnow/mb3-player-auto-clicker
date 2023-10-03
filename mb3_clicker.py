"""
For Google Chrome brower.
MixerBox URL: https://www.mbplayer.com/

Description:
MixerBox Player Automated Click Player
Using selenium of Python module to operate Previous, Next, Play/Pause Button.

一些在製作動機的廢話:
    -- 因為本人蠻常使用 MixerBox 聽音樂，主要會在 PC 端使用網頁版，邊聽邊做事情，
       由於鍵盤有多媒體功能鰎 (fn + 播放器有的功能鰎) 不能作用到 MixerBox 網頁版，
       又加上 *懶得切到原網頁* 切換歌曲，所以寫了這個廢東西

結論: 科技帶來的便利性，來自於人類的懶惰

        -- by 某名人/偉人說過 (應該......)
"""


from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os


# 預設網址
url = "https://www.mbplayer.com/list/182229363"


# 網址檢查
CHECK_URL = "https://www.mbplayer.com/list/"


CMD_MSG = "cmd (輸入命令選項): 1. 前一首  2. 播放/暫停  3. 下一首  4. exit\n" + \
          "S. 顯示目前的播放清單網址  M. 更改播放清單網址\n" + \
          ": "
MSG = [
    f"網址: {url}\n",
    "輸入播放清單網址",
    "確認使用(Y/N)\n",
    ": "
]



driver = webdriver.Edge()


def initial():
    global url
    driver.get(url)
    driver.maximize_window()

    time.sleep(3.5)
    
    # class name: css-1wglmvy e1eiglht2
    firstSong_element = driver.find_element(By.CLASS_NAME, "css-xixs5t")
    firstSong_element.click()

    time.sleep(2)
    
    element = driver.find_element(By.CLASS_NAME, "css-1mw6l2m")
    element.click()


init = True

while True:
    if init:
        initial()
        init = False

    cmd = input(CMD_MSG)

    if "1" in cmd:
        # 前一首
        # class name: MuiBox-root css-qorinj
        element = driver.find_element(By.CLASS_NAME, "css-qorinj")
        element.click()

    if "2" in cmd:
        # 播放/暫停
        # class name: MuiBox-root css-1mw6l2m
        element = driver.find_element(By.CLASS_NAME, "css-1mw6l2m")
        element.click()

    if "3" in cmd:
        # 下一首
        # class name: MuiBox-root css-1n4h12s
        element = driver.find_element(By.CLASS_NAME, "css-1n4h12s")
        element.click()

    if "4" in cmd:
        print("點擊器 關閉囉!")
        break

    if "S".lower() in cmd.lower():
        print(MSG[0])

    if "M".lower() in cmd.lower():
        print(MSG[1])
        new_url = input(MSG[3])
        
        if new_url and CHECK_URL in new_url:
            use = input(MSG[2] + MSG[3])
            
            if "Y".lower() in use:
                # 播放視窗的關閉按鈕 (在右下播放視窗，角有一個 x 符號)
                # class name: css-fc2je9
                element = driver.find_element(By.CLASS_NAME, "css-fc2je9")
                element.click()
                url = new_url
                init = True
                time.sleep(0.5)

        else:
            print("錯誤網址")

    if "cls" in cmd.lower():
        # 清除視窗
        os.system("cls")



driver.close()