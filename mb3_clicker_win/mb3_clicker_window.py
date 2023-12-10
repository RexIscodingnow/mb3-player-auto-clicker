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
from selenium.common.exceptions import WebDriverException


"""
class="e1oiqyjt1": 播放清單標題
<iframe title=""></iframe>: 播放歌曲的標題

<li class="css-1wglmvy">: 歌曲位置 (第 1 個 ~ n 個)


操作面板
    <div class="">
                    1. css-qorinj  => 前一首
                    2. css-1mw6l2m => 播放 / 暫停
                    3. css-1n4h12s => 下一首

常用歌單: https://www.mbplayer.com/list/182229363
古典樂: https://www.mbplayer.com/list/178091336
"""


is_clicked = False
url = "https://www.mbplayer.com/list/182229363"   # for testing
# url = "https://www.mbplayer.com/list/178091336"

CHECK_URL = "https://www.mbplayer.com/list/"

WIDTH = 700
HEIGHT = 800
PROMPT_MSG = "輸入命令"
MANUAL_MSG = "命令選項 (可大小寫):\t\t\n" + \
             "\n" + \
             "1. 前一首 ----------> P\t\n" + \
             "2. 播放/暫停 -------> K\t\n" + \
             "3. 下一首 ----------> N\t\n" + \
             "\t4. 更改播放清單網址 --> M\t\n" + \
             "\n" + \
             "最小化開啟的瀏覽器 --> J\n" + \
             "執行按鈕 or Enter 鍵執行指令\n"
            #  "\n" + \
            #  "**退出應用程式 -->> E\n"


PLAYLIST_NAME = "播放清單:"
SONG_NAME = "正在播放:"


class Clicker:
    def __init__(self, url: str = "") -> None:
        self.url = url
        self.reset_times = 0   # recursion times
        self.driver = webdriver.Edge()


    def init_process(self):
        try:
            if not self.url:
                return

            self.driver.get(self.url)
            
            time.sleep(5)

            first_song = self.driver.find_element(By.CLASS_NAME, "css-xixs5t")
            first_song.click()

            self.reset_times = 0

        except:
            # self.connect_error()
            # pass
            raise WebDriverException("An error occurred when trying to open the playlist.\nPlease Check the PlayList URL!")


    def connect_error(self, event: td.Event):        
        # FIXME: 斷網處理
        if self.reset_times >= 3:
            msg = "以達上限次數 (3)\n\n按下任意鍵離開"
            main_window.info_song.set(msg)
            
            self.reset_times = 0
            
            time.sleep(0.5)
            while not keyboard.read_event() or not main_window.is_pressed: pass
            return
        
        else:
            self.reset_times += 1
            print(self.reset_times)
            
            msg = "1. 輸入 R 重新載入原網址\n" + "2. 輸入 M 更改網址\n" + "或關掉重開一遍"
            main_window.info_song.set(msg)

            time.sleep(0.5)

            cmd = ""

            while not event.is_set():
                if cmd in ['r', 'm']:
                    if main_window.is_pressed or keyboard.is_pressed("enter"):
                        main_window.cmd_entry.delete(0, "end")
                        break

                cmd = main_window.cmd_entry.get().lower()

            if cmd == 'r':
                main_window.info_song.set("重新載入原網址\n請等待 2 秒")

                time.sleep(2)

                try:
                    self.init_process()
                    self.reset_times = 0

                except WebDriverException as we:
                    self.connect_error(err_event)
            
            # FIXME: modify url
            elif cmd == 'm':
                main_window.info_song.set("輸入網址")

                time.sleep(1)

                url = ""
                
                # while not keyboard.is_pressed("enter") or not main_window.is_pressed:
                while not event.is_set():
                    if main_window.is_pressed or keyboard.is_pressed("enter"):
                        break
                    
                    url = main_window.cmd_entry.get()

                main_window.cmd_entry.delete(0, "end")

                try:
                    self.changeURL(url)
                
                except WebDriverException as we:
                    self.connect_error(error_handle)


    # ==================================================================
    # ==================================================================
 
    def get_listTitle(self) -> str:
        try:
            playlist = self.driver.find_element(By.CLASS_NAME, "e1oiqyjt1")
            return playlist.text
        except:
            return "Error"

    def get_songTitle(self) -> str:
        try:
            cut_len = 20
            new_title = ""
            song_display = self.driver.find_element(By.TAG_NAME, "iframe")
            title = song_display.get_attribute("title")
            
            for i in range(len(title)):
                new_title += title[i]                    
                if (i + 1) % cut_len == 0:
                    new_title += "\n"

            return new_title
        except:
            return "Error"


    # ==================================================================
    # ==================================================================

    def previous(self):
        try:
            element = self.driver.find_element(By.CLASS_NAME, "css-qorinj")
            element.click()
        except:
            raise WebDriverException("Some errors have occurred in the operation here.\n(Operation interface of Song Player --> Play)")
            # raise WebDriverException()

    def play_pause(self):
        try:
            element = self.driver.find_element(By.CLASS_NAME, "css-1mw6l2m")
            element.click()
        except:
            raise WebDriverException("Some errors have occurred in the operation here.\n(Operation interface of Song Player --> Pause)")
            # raise WebDriverException()

    def next_song(self):
        try:
            element = self.driver.find_element(By.CLASS_NAME, "css-1n4h12s")
            element.click()
        except:
            raise WebDriverException("Some errors have occurred in the operation here.\n(Operation interface of Song Player --> Next)")
            # raise WebDriverException()


    def changeURL(self, url: str):
        if CHECK_URL not in url:
            main_window.info_song.set("網址錯誤，要帶有:\n" + f"{CHECK_URL}\n\n" + "按下任意鍵繼續")
            
            time.sleep(1)
            while not keyboard.read_event() or not main_window.is_pressed: pass
            return
        
        element = self.driver.find_element(By.CLASS_NAME, "css-fc2je9")
        element.click()

        try:
            self.url = url
            self.init_process()
            self.reset_times = 0

        except WebDriverException as we:
            raise WebDriverException("An error occurred when change new URL (another Playlist)")


class Window(tk.Tk):
    def __init__(self) -> None:
        super().__init__()

        self.title("MB3_clicker")
        self.config(background="black")
        screen_mid_x = (self.winfo_screenwidth() - WIDTH) // 2
        screen_mid_y = (self.winfo_screenheight() - HEIGHT) // 2
        self.geometry(f"{WIDTH}x{HEIGHT}+{screen_mid_x}+{screen_mid_y}")
        self.resizable(False, False)

        self.__flag = False
        self.is_pressed = False
        self.info_song = tk.StringVar()   # 歌曲資訊

        # ==================================================
        # ==================================================

        self.info_playList = tk.Label(
            font=("Arial", 18),
            textvariable=self.info_song,
            width=35,
            height=8
        )
        self.cmd_entry = tk.Entry(
            font=("標楷體", 25),
            width=22
        )
        self.exec_btn = tk.Button(
            text="執行",
            font=("標楷體", 22),
            command=self.command,
            width=6,
            height=1
        )
        self.manual = tk.Label(
            background = "skyblue",
            font = ("標楷體", 20),
            text=MANUAL_MSG,
            width=35,
            height=10
        )

        self.__set_weiget(self.info_playList, 100, 50, self.info_song, PLAYLIST_NAME + '\n' + SONG_NAME)
        self.__set_weiget(self.cmd_entry, 150, 300)
        self.__set_weiget(self.exec_btn, WIDTH // 2 - 65, 370)
        self.__set_weiget(self.manual, WIDTH // 7, HEIGHT // 2 + 60)

    @property
    def flag(self):
        return self.__flag
    
    @flag.setter
    def flag(self, flag):
        self.__flag = flag

    # =========================================================
    # =========================================================
    # =========================================================

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


    def clicked(self, event):
        self.is_pressed = True
        # print("pressed it")

    def released(self, event):
        self.is_pressed = False
        # print("released it")

    def update_info(self):
        origin = self.info_song.get()
        info = f"{PLAYLIST_NAME} {clicker.get_listTitle()}\n {SONG_NAME}\n{clicker.get_songTitle()}"
        
        if origin != info and self.__flag == False:
            self.info_song.set(info)


    def command(self):
        cmd = self.cmd_entry.get().strip()
        self.cmd_entry.delete(0, "end")
        
        try:
            if self.__flag == True:
                clicker.changeURL(cmd)
                self.__flag = False

            if cmd.lower() == "p" and self.__flag == False:
                clicker.previous()
            elif cmd.lower() == "k" and self.__flag == False:
                clicker.play_pause()
            elif cmd.lower() == "n" and self.__flag == False:
                clicker.next_song()
            elif cmd.lower() == "j" and self.__flag == False:
                clicker.driver.minimize_window()
            elif cmd.lower() == "m" and self.__flag == False:
                self.__flag = True
                self.info_song.set("輸入網址\n若不要改請按 ESC 鍵退出")
            
            # if cmd.lower() == "e" and self.flag == False:
            #     clicker.exit()

        except WebDriverException as we:
            # print(e)
            
            # FIXME: 創建 & 卡頓
            error_handle = td.Thread(target=clicker.connect_error, args=(err_event,), name="error handle")
            error_handle.start()
            error_handle.join()

            # time.sleep(0.1)

            # # restart read_key() for new thread
            # event.clear()
            # print(event.is_set())


def read_keyboard(stop_event: td.Event):
    while not stop_event.is_set():
        main_window.update_info()

        if keyboard.is_pressed("enter") and main_window.cmd_entry.get():
            main_window.command()

        if keyboard.is_pressed("esc") and main_window.flag:
            main_window.flag = False


def exit_exec(keyboard_event: td.Event, err_event: td.Event):
    keyboard_event.set()
    
    if error_handle.is_alive():
        if err_event.is_set():
            err_event.set()

        error_handle.join()

    # 處理執行緒死鎖
    # 避免 read_key 加入到主執行緒
    if read_key.is_alive() and read_key is not td.current_thread():
        keyboard.unhook_all()
        read_key.join()

    main_window.quit()
    clicker.driver.close()


if __name__ == "__main__":
    main_window = Window()
    clicker = Clicker(url)

    err_event = td.Event()
    keyboard_event = td.Event()
    error_handle = td.Thread(target=clicker.connect_error, args=(err_event,), name="error handle")
    # main_window.tk.call("wm", "iconphoto", main_window._w, tk.PhotoImage(file="mouse.png"))
    
    try:
        clicker.init_process()
    
    except WebDriverException as we:
        error_handle.start()

    finally:
        read_key = td.Thread(target=read_keyboard, args=(keyboard_event,), name="read keyboard")
        read_key.start()

        main_window.exec_btn.bind("<Button-1>", main_window.clicked)
        main_window.exec_btn.bind("<ButtonRelease-1>", main_window.released)
        
        # 
        main_window.protocol("WM_DELETE_WINDOW", lambda: exit_exec(keyboard_event, err_event))
        main_window.update_info()
        main_window.mainloop()