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
    "網址:",
    "輸入播放清單網址",
    "確認使用(Y/N)\n",
    ": "
]


driver = webdriver.Edge()


def initial(url: str):
    # global url
    driver.get(url)

    time.sleep(3.5)

    # class name: css-1wglmvy e1eiglht2
    firstSong_element = driver.find_element(By.CLASS_NAME, 'css-1x7tk1n')
    firstSong_element.click()


initial(url)

while True:
    cmd = input(CMD_MSG).strip()

    if cmd == "1":
        # 前一首
        # class name: MuiBox-root css-qorinj
        # element = driver.find_element(By.CLASS_NAME, "css-qorinj")
        element = driver.find_element(By.XPATH, "//*[@id=\"__next\"]/div[1]/div/div/div[2]/div[1]")
        element.click()

    if cmd == "2":
        # 播放/暫停
        # class name: MuiBox-root css-1mw6l2m
        # element = driver.find_element(By.CLASS_NAME, "css-1mw6l2m")
        element = driver.find_element(By.XPATH, "//*[@id=\"__next\"]/div[1]/div/div/div[2]/div[2]")
        element.click()

    if cmd == "3":
        # 下一首
        # class name: MuiBox-root css-1n4h12s
        # element = driver.find_element(By.CLASS_NAME, "css-1n4h12s")
        element = driver.find_element(By.XPATH, "//*[@id=\"__next\"]/div[1]/div/div/div[2]/div[3]")
        element.click()

    if cmd == "4":
        print("點擊器 關閉囉!")
        break

    if cmd.lower() == "s":
        print(f"{MSG[0]} {url}")

    if cmd.lower() == "m":
        print(MSG[1])
        new_url = input(MSG[3]).strip()
        
        if not new_url or CHECK_URL not in new_url:
            print("錯誤網址")
            continue

        while True:
            op = input(MSG[2] + MSG[3]).lower().strip()
            if op == "y":
                # 播放視窗的關閉按鈕 (在右下播放視窗，右下角有一個 x 符號)
                # class name: css-fc2je9
                url = new_url
                element = driver.find_element(By.CLASS_NAME, "css-fc2je9")
                element.click()
                time.sleep(0.5)
                initial(new_url)
                break

            elif op == 'n':
                print("不改動播放清單")
                break

    if "cls" in cmd.lower():
        # 清除視窗
        os.system("cls")


driver.close()