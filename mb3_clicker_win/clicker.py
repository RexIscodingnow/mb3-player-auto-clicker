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


class Clicker:
    def __init__(self) -> None:
        self.url = ""
        self.driver = webdriver.Edge()


    def init_process(self, url) -> None:
        if not url:
            # raise URLError("URLError occurred: ")
            return

        try:
            self.url = url
            self.driver.get(url)
            time.sleep(5)   # Wait for the page to finish loading
            
            first_song = self.driver.find_element(By.CLASS_NAME, 'css-1x7tk1n')
            first_song.click()
            self.driver.minimize_window()

        except NoSuchElementException as e:
            print(e.msg)

        except ElementClickInterceptedException as e:
            print(e.msg)

        except TimeoutError as e:
            print(e)


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
            cut_len = 20
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
    """ unit test """
    # url = "https://www.mbplayer.com/list/182229363"
    url = "https://www.mbplayer.com/list/178091336"
    # url = "https://www.mbplayer.com/list/198715305"
    # url = "https://www.mbplayer.com/list/RDfNEcOxsScls"

    clicker = Clicker()
    clicker.init_process(url)

    cmd = ""

    while cmd != "cancel":
        cmd = input("command: ").lower().strip()

        match cmd:
            case 'p':
                clicker.play_pause()

            case 'k':
                clicker.previous_song()

            case 'n':
                clicker.next_song()

