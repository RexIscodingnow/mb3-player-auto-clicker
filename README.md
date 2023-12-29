# mb3-player-auto-clicker

## For ~~Google Chrome~~ Edge brower.
## MixerBox URL: https://www.mbplayer.com/

### Description:
MixerBox Player ~~Automated~~ Clicker Player
Using selenium to operate Previous, Next, Play/Pause Button.

* 一些在製作動機的廢話:
    -- 因為本人蠻常使用 MixerBox 聽音樂，主要會在 PC 端使用網頁版，邊聽邊做事情，
       由於鍵盤有多媒體功能鰎 (fn + 播放器有的功能鰎) 不能作用到 MixerBox 網頁版，
       又加上 *懶得切到原網頁* 切換歌曲，所以寫了這個廢東西
<br/>
* 更: 也省去開瀏覽器，再開 MixerBox 網頁播放器的動作

結論: 科技帶來的便利性，來自於人類的懶惰
        -- by 某名人/偉人說過 (應該......)

# How to use it

Install the `Selenium`, if you haven't installed it.
```
pip install selenium
```


* Command prompt ver.
1. run
    ```
    python mb3_clicker.py
    ```

* GUI ver.
1. Install `keyboard`

```
pip install keyboard
```

2. Change the directory

    ```
    cd mb3_clicker_win
    ```

3. Run

    ```
    python mb3_clicker_window.py
    ```

# TODO
| TODO List | complete |
|------------------|------|
| 1. keyboard listener | ✔ |
| 2. GUI                | ✔ |
| 3. 打包成 .exe 執行檔 (probably todo) | ❌ |
