[English](README.md) | 繁體中文
# 自動按鍵工具
一個可以模擬鍵盤和滑鼠操作的工具，用 python 製作。

## 說明
## 語法
* 鍵盤操作
  * key 字串
  * press key_name
  * hold key_name
  * release key_name
  > 所有可用的 key_name 可於下方查表
* 滑鼠操作
  * 移動
    * move relative(r) dx dy
    * move absolute(a) x y
    * move image(i) image_path
  * 點擊
    * click left/right/middle
    * click left/right/middle N
    * click left/right/middle hold
    * click left/right/middle release
    * click left/right/middle hold release
  * 滾動
    * scroll up/down
    * scroll up/down amount
* 休眠
  * sleep N
* 迴圈
  * loop N
  * loop end
* if狀態
  * if image file_path
  * if mouse px py
  * endif
* 退出
  * exit

## 語法手冊
* 鍵盤操作
  * key 字串
  > 模擬鍵盤輸入此字串
  * press key_name
  > 按鍵盤按鍵一次
  * hold key_name
  > 按住鍵盤按鍵
  * release key_name
  > 鬆開鍵盤按鍵
  > 
  > 所有可用的 key_name 可於下方查表
* 滑鼠操作
  * move
  > 這個指令可以移動滑鼠鼠標
    * move relative(r) dx dy
    > 相對座標移動
    * move absolute(a) x y
    > 移動到絕對座標
    * move image(i) image_path
    > 移動到屏幕上偵測的給定圖片中心，如果沒找到圖片，則不會移動
  * click
  > 點擊滑鼠按鍵
    * click left/right/middle
    > 點擊一次
    * click left/right/middle N
    > 點擊 N 次
    * click left/right/middle hold
    > 按住按鍵
    * click left/right/middle release
    > 鬆開按鍵
    * click left/right/middle hold release
    > 按住再鬆開
  * scroll
  > use mouse scroll
    * scroll up/down
    > scroll onece
    * scroll up/down amount
    > scroll the certain amount
* sleep
> this method is for waiting the instruction. To slow down your script.
  * sleep N
  > wait for N seconds
* loop
> loop is a specific syntax. It has no effect but it can be mixed with other features.
  * loop N
  > loop N times. if N == -1 it will be infinite loop. It can be break with esc.
  * loop end
  > after a loop need to put loop end to declare a stop for loop.
* if
  * if image file_path
  > detect if on the screen detect the image file. It will be true and run the code below.
  * if mouse px py
  > detect if mouse in px py.
  * endif
  > after a if statement need to put endif to declare a stop for statement.
* exit
> stop the script

## all key_name available

* a, b, c, ...: 單個字母鍵

* 1, 2, 3, ...: 數字鍵

* F1, F2, F3, ...: 功能鍵

* space: 空格鍵

* enter: 回車鍵

* tab: 制表鍵

* shift: Shift鍵

* ctrl: Ctrl鍵

* alt: Alt鍵

* caps lock: 大寫鎖定鍵

* esc: Escape鍵

* backspace: 倒退鍵

* delete: 刪除鍵

* home: Home鍵

* end: End鍵

* page up: Page Up鍵

* page down: Page Down鍵

* left arrow: 左方向鍵

* right arrow: 右方向鍵

* up arrow: 上方向鍵

* down arrow: 下方向鍵

## TODO
- [X] if else: to detect image and to do something
- [ ] count
- [ ] not bool
- [ ] record
- [ ] support excel
- [ ] gui
- [ ] generate instruction file
