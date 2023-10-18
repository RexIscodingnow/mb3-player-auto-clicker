"""
For Google Chrome brower (or Edge).
MixerBox URL: https://www.mbplayer.com/

Description: Window ver.
--  MixerBox Player Automated Click Player
    Using selenium to operate Previous, Next, Play/Pause Button.

這個是帶視窗介面
"""


import time
import keyboard
import tkinter as tk
import threading as td

from selenium import webdriver
from selenium.webdriver.common.by import By


"""
class="e1oiqyjt1": 播放清單標題
<iframe title=""></iframe>: 播放歌曲的標題

<li class="css-1wglmvy">: 歌曲位置 (第 1 個 ~ n 個)


操作面板
    <div class="">
                    1. css-qorinj  => 前一首
                    2. css-1mw6l2m => 播放 / 暫停
                    3. css-1n4h12s => 下一首
"""


url = "https://www.mbplayer.com/list/182229363"   # for testing

CHECK_URL = "https://www.mbplayer.com/list/"

WIDTH = 700
HEIGHT = 800
PROMPT_MSG = "輸入命令"
MANUAL_MSG = "command (輸入命令選項):\n" + \
             "1. 前一首 -----> P\t\n" + \
             "2. 播放/暫停 -> K\t\n" + \
             "3. 下一首 -----> N\t\n" + \
             "\n" + \
             "* 更改播放清單網址 --> M\t\n" + \
             "\n" + \
             "*執行* 按鈕 or Enter 鍵執行指令\n"
            #  "**退出應用程式 -->> E\n"


PLAYLIST_NAME = "播放清單: "
SONG_NAME = "歌曲:"


class Clicker:
    def __init__(self, url: str = "") -> None:
        self.url = url
        self.reset_times = 0
        self.driver = webdriver.Edge()


    def init_process(self):
        try:
            self.driver.get(self.url)
            time.sleep(3.5)

            first_song = self.driver.find_element(By.CLASS_NAME, "css-xixs5t")
            first_song.click()

            # self.reset_times = 0

        except:
            pass
            # msg = "1. 按下 R 重新開啟\n" + "2. 按下 M 更改網址"
            # main_window.info_song.set(msg)

            # # TODO: To send request or modify URL if recursive less than equal 3 times.
            # if self.reset_times >= 3:
            #     self.reset_times = 0
            #     return
            
            # else:
            #     while not keyboard.read_event() or main_window.cmd_entry.get(): pass

            #     self.reset_times += 1

            #     if keyboard.is_pressed("r") and main_window.cmd_entry.get() == " ":
            #         self.init_process()


    # ==================================================================
    # ==================================================================

    def get_listTitle(self) -> str:
        try:
            playlist = self.driver.find_element(By.CLASS_NAME, "e1oiqyjt1")
            return playlist.text
        except Exception as e:
            return "Error"

    def get_songTitle(self) -> str:
        try:
            cut_len = 20
            song_display = self.driver.find_element(By.TAG_NAME, "iframe")
            title = song_display.get_attribute("title")

            if len(title) >= cut_len:
                new_title = ""

                for i in range(len(title)):
                    new_title += title[i]
                    
                    if (i + 1) % cut_len == 0:
                        new_title += "\n"

                return new_title
            else:
                return title

        except Exception as e:
            return "Error"


    # ==================================================================
    # ==================================================================

    def previous(self):
        try:
            element = self.driver.find_element(By.CLASS_NAME, "css-qorinj")
            element.click()
        except:
            pass

    def play_pause(self):
        try:
            element = self.driver.find_element(By.CLASS_NAME, "css-1mw6l2m")
            element.click()
        except:
            pass

    def next_song(self):
        try:
            element = self.driver.find_element(By.CLASS_NAME, "css-1n4h12s")
            element.click()
        except:
            pass


    def changeURL(self, url: str):
        if CHECK_URL not in url:
            main_window.info_song.set("網址錯誤，要帶有:\n" + f"{CHECK_URL}\n\n" + "按下任意鍵繼續")
            time.sleep(1)
            while not keyboard.read_event(): pass
            return

        self.url = url
        self.init_process()

    def exit(self):
        global running

        running = False
        
        # 處理執行緒死鎖
        # 避免 read_key 加入到主執行緒
        if read_key.is_alive() and read_key is not td.current_thread():
            keyboard.unhook_all()
            read_key.join()

        self.driver.close()
        main_window.quit()


class MainWindow(tk.Tk):
    def __init__(self) -> None:
        super().__init__()

        self.title("測試 mb3_clicker")
        self.config(background="black")
        screen_mid_x = (self.winfo_screenwidth() - WIDTH) // 2
        screen_mid_y = (self.winfo_screenheight() - HEIGHT) // 2
        self.geometry(f"{WIDTH}x{HEIGHT}+{screen_mid_x}+{screen_mid_y}")
        self.resizable(False, False)

        self.__flag = False
        self.info_song = tk.StringVar()

        # ==================================================
        # ==================================================

        self.info_playList = tk.Label(
            font=("Arial", 18),
            textvariable=self.info_song,
            width=35,
            height=8
        )
        self.cmd_entry = tk.Entry(
            font=("Arial", 20),
            width=30
        )
        self.exec_btn = tk.Button(
            text="執行",
            font=("Arial", 20),
            command=self.command
        )
        self.manual = tk.Label(
            background = "skyblue",
            font = ("Arial", 20),
            text=MANUAL_MSG,
            width=25
        )

        self.__set_weiget(self.info_playList, 90, 50, self.info_song, PLAYLIST_NAME + '\n' + SONG_NAME)
        self.__set_weiget(self.cmd_entry, 110, 300)
        self.__set_weiget(self.exec_btn, WIDTH // 2 - 50, 370)
        self.__set_weiget(self.manual, WIDTH // 5, HEIGHT // 2 + 60)

    def __set_weiget(self,
                     widget: tk.Widget,
                     x: int = 0,
                     y: int = 0,
                     strVar: tk.StringVar = None,
                     value: str = "",
                     ) -> None:
        
        widget.place(x=x, y=y)

        if strVar:
            strVar.set(value)

    def update_info(self):
        origin = self.info_song.get()
        info = PLAYLIST_NAME + f" {clicker.get_listTitle()}\n" + SONG_NAME + f"\n{clicker.get_songTitle()}"
        if origin != info and self.__flag == False:
            self.info_song.set(info)


    def command(self):
        cmd = self.cmd_entry.get()
        self.cmd_entry.delete(0, "end")
        
        if self.__flag == True:
            clicker.changeURL(cmd.strip())
            self.__flag = False

        if cmd.lower() == "p" and self.__flag == False:
            clicker.previous()
        elif cmd.lower() == "k" and self.__flag == False:
            clicker.play_pause()
        elif cmd.lower() == "n" and self.__flag == False:
            clicker.next_song()
        elif cmd.lower() == "m" and self.__flag == False:
            self.__flag = True
            self.info_song.set("輸入網址")
        
        # if cmd.lower() == "e" and self.flag == False:
        #     clicker.exit()


def read_keyboard():
    global running

    while running:
        main_window.update_info()

        if keyboard.is_pressed("enter") and main_window.cmd_entry.get():
            main_window.command()


if __name__ == "__main__":
    main_window = MainWindow()
    clicker = Clicker(url)

    clicker.init_process()
    info = PLAYLIST_NAME + f"{clicker.get_listTitle()}\n" + SONG_NAME + f"\n{clicker.get_songTitle()}"
    main_window.info_song.set(info)

    running = True
    read_key = td.Thread(target=read_keyboard, name="read keyboard")

    main_window.protocol("WM_DELETE_WINDOW", clicker.exit)

    read_key.start()
    main_window.mainloop()