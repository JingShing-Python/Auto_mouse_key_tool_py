[English](README.md) | 繁體中文
# Auto_mouse_key_tool_py
A tool that can simulate key and mouse action coding with python. It use simple syntax to move mouse and key in the text and find the image position.

## Instructions
## All syntax
* keyboard action
  * key string
  * key hold key_name
  * key release key_name
  > all key name can see in below
* mouse action
  * move
    * move relative(r) dx dy
    * move absolute(a) x y
    * move image(i) image_path
  * click
    * click left/right/middle
    * click left/right/middle N
    * click left/right/middle hold
    * click left/right/middle release
    * click left/right/middle hold release
  * scroll
    * scroll up/down
    * scroll up/down amount
* sleep
  * sleep N
* loop
  * loop N
  * loop end
* if
  * if image file_path
  * if mouse px py
  * endif
* exit

## Manual for syntax

* mouse action
  * move
  > this command can move mouse to specific position
    * move relative(r) dx dy
    > relative move
    * move absolute(a) x y
    > move to the absolute position
    * move image(i) image_path
    > move to the image detect on the screen. If not found it will do nothing
  * click
  > click the mouse button
    * click left/right/middle
    > click once
    * click left/right/middle N
    > click N times
    * click left/right/middle hold
    > pressed the button
    * click left/right/middle release
    * click left/right/middle hold release
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
* a, b, c, ...: individual letter keys

* 1, 2, 3, ...: number keys

* F1, F2, F3, ...: function keys

* space: spacebar

* enter: enter key

* tab: tab key

* shift: Shift key

* ctrl: Ctrl key

* alt: Alt key

* caps lock: Caps Lock key

* esc: Escape key

* backspace: backspace key

* delete: delete key

* home: Home key

* end: End key

* page up: Page Up key

* page down: Page Down key

* left arrow: left arrow key

* right arrow: right arrow key

* up arrow: up arrow key

* down arrow: down arrow key

## TODO
- [X] if else: to detect image and to do something
- [ ] count
- [ ] not bool
- [ ] record
- [ ] support excel
- [ ] gui
- [ ] generate instruction file
