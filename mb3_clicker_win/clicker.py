"""
Todo list
    
TODO: Add 3 exception handlers to Clicker.init_process().

"""


import time
from urllib.parse import urlparse
from urllib.error import URLError
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    WebDriverException,
    ElementClickInterceptedException,
    NoSuchAttributeException,
    NoSuchElementException,
    TimeoutException
)


WAIT_LOADING_TIME = 5

PREFIX_URL = "https://www.mbplayer.com/list/"
PARSED_PREFIX_URL = urlparse(PREFIX_URL)


class InvalidURLError(ValueError):
    """
    Raised when the URL format is invalid or does not match the required pattern.
    """
    pass


class Clicker:
    def __init__(self) -> None:
        self.url = ""
        self.driver = webdriver.Edge()


    def init_process(self, url: str) -> None:
        if not url:
            raise ValueError("The `url` must not be empty.")

        try:
            parse_result = urlparse(url)
            if (PARSED_PREFIX_URL.netloc != parse_result.netloc) or \
                (PARSED_PREFIX_URL.path not in parse_result.path):
                raise InvalidURLError(f"Invalid URL: expected the `url` to match the '{PREFIX_URL}' pattern.")

            self.driver.get(url)
            time.sleep(WAIT_LOADING_TIME)   # Wait for the page to finish loading

            first_song = self.driver.find_element(By.CLASS_NAME, 'css-1x7tk1n')
            first_song.click()

            # Wait for `first_song.click()` to complete before minimizing the browser window
            time.sleep(2)
            self.minimize_window()

        except NoSuchElementException as e:
            print(e.msg)

        except ElementClickInterceptedException as e:
            print(e.msg)

        except TimeoutError as e:
            print(e)


    def minimize_window(self) -> None:
        self.driver.minimize_window()

    # ==================================================================
    # ==================================================================

    def get_playlist_title(self) -> str:
        try:
            playlist_title = self.driver.find_element(By.CLASS_NAME, "e1oiqyjt1")
            return playlist_title.text

        except NoSuchElementException as e:
            print(e)
            return "The playlist title is not found"


    def get_song_title(self) -> str:
        try:
            cut_len = 30
            new_title = ""
            song_display = self.driver.find_element(By.TAG_NAME, "iframe")
            title = song_display.get_attribute("title")

            for i in range(len(title)):
                new_title += title[i]                    
                if (i + 1) % cut_len == 0:
                    new_title += "\n"

            return new_title

        except NoSuchElementException as e:
            print(e)
            return "The song title is not found"

        except NoSuchAttributeException as e:
            print(e)
            return "The song title is not found"

    # ==================================================================
    # ==================================================================

    def previous_song(self) -> None:
        """
        click previous track button
        """
        try:
            # element = self.driver.find_element(By.CLASS_NAME, "css-qorinj")
            element = self.driver.find_element(By.XPATH, "//*[@id=\"__next\"]/div[1]/div/div/div[2]/div[1]")
            element.click()

        except NoSuchElementException as e:
            raise WebDriverException("Some errors have occurred in the operation here.\n(Operation interface of Song Player --> Play)")


    def play_pause(self) -> None:
        """
        click play / pause control button
        """
        try:
            # element = self.driver.find_element(By.CLASS_NAME, "css-1mw6l2m")
            element = self.driver.find_element(By.XPATH, "//*[@id=\"__next\"]/div[1]/div/div/div[2]/div[2]")
            element.click()

        except NoSuchElementException as e:
            raise WebDriverException("Some errors have occurred in the operation here.\n(Operation interface of Song Player --> Pause)")


    def next_song(self) -> None:
        """
        click next track button
        """
        try:
            # element = self.driver.find_element(By.CLASS_NAME, "css-1n4h12s")
            element = self.driver.find_element(By.XPATH, "//*[@id=\"__next\"]/div[1]/div/div/div[2]/div[3]")
            element.click()

        except NoSuchElementException as e:
            raise WebDriverException("Some errors have occurred in the operation here.\n(Operation interface of Song Player --> Next)")


    def switch_playlist(self, url: str) -> None:
        """
        To switch to another playlist using the `url`
        """


if __name__ == '__main__':
    """ unit test
    another cmd ver.
    """
    import threading as td

    def _msg_update(old_song_name, old_title, clicker: Clicker, event: td.Event):
        while not event.is_set():
            title = clicker.get_playlist_title()
            song_name = clicker.get_song_title()

            if old_title != title:
                old_title = title
                print(f"\n{title}\n", end='\r', flush=True)
            if old_song_name != song_name:
                old_song_name = song_name
                print(f"\n{song_name}\n", end='\r', flush=True)

    # url = "https://www.mbplayer.com/list/182229363"
    url = "https://www.mbplayer.com/list/178091336"
    # url = "https://www.mbplayer.com/list/198715305"
    # url = "https://www.mbplayer.com/list/RDfNEcOxsScls"

    print("opening clicker ...")

    clicker = Clicker()
    clicker.init_process(url)

    print("try `help` to show all command")

    _event = td.Event()
    _msg_update_td = td.Thread(target=_msg_update,  args=("", "", clicker, _event))
    _msg_update_td.start()

    while True:
        title = clicker.get_playlist_title()
        song = clicker.get_song_title()
        print(title)
        print(song)

        cmd = input("command: ").lower().strip()

        match cmd:
            case 'p':
                clicker.play_pause()

            case 'k':
                clicker.previous_song()

            case 'n':
                clicker.next_song()

            case 'help':
                print("p\t\tPlay / Pause the song\n"
                      "k\t\tPrevious song\n"
                      "n\t\tNext song\n"
                      "min-win\t\tMinimize browser window\n"
                      "help\t\tShow all commands describe\n"
                      "exit\t\tExit the clicker\n\n")

            case 'min-win':
                clicker.minimize_window()
                print("minimize browser window\n")

            case 'exit':
                print("stop process...")

                if _msg_update_td.is_alive():
                    _event.set()
                    _msg_update_td.join()
                break

            case _:
                print("try `help` to show all command\n")

