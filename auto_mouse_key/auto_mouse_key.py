import keyboard
import pyautogui
import time

def process_command(command):
    action, *args = command.split()

    key_actions = ['key', 'hold', 'release']
    mouse_actions = ['move', 'click', 'scroll']
    click_types = ['left', 'right']
    scroll_directions = ['up', 'down']

    if action in key_actions:
        # keyboard action
        # key string
        if action == 'key':
            keyboard.write(' '.join(args))
        elif action == 'hold':
            key = args[0]
            keyboard.press(key)
        elif action == 'release':
            key = args[0]
            keyboard.release(key)
    elif action in mouse_actions:
        # mouse action

        # move
        # move relative(r) dx dy
        # move absolute(a) x y
        # move image(i) image_path

        # click
        # click left/right/middle
        # click left/right/middle N
        # click left/right/middle hold
        # click left/right/middle release
        # click left/right/middle hold release

        # scroll
        # scroll up/down
        # scroll up/down amount
        if action == 'move':
            move_type, *values = args
            if move_type == 'relative' or move_type == 'r':
                x, y = map(int, values)
                current_x, current_y = pyautogui.position()
                target_x = current_x + x
                target_y = current_y + y
                pyautogui.moveTo(target_x, target_y)
            elif move_type == 'absolute' or move_type == 'a':
                x, y = map(int, values)
                pyautogui.moveTo(x, y)
            elif move_type == 'image' or move_type == 'i':
                image_path = ' '.join(values)
                center = pyautogui.locateCenterOnScreen(image_path)
                if center:
                    x, y = center
                    pyautogui.moveTo(x, y)
        elif action == 'click':
            if 'hold' in args:
                pyautogui.mouseDown()
                if 'release' in args:
                    time.sleep(0.1)
                    pyautogui.mouseUp()
            elif 'release' in args:
                pyautogui.mouseUp()
            else:
                click_type = args[0]
                if click_type in click_types:
                    count = int(args[1]) if len(args) > 1 else 1
                    for _ in range(count):
                        pyautogui.click(button=click_type)
        elif action == 'scroll':
            scroll_direction = args[0]
            if scroll_direction in scroll_directions:
                amount = int(args[1]) if len(args) > 1 else 1
                if scroll_direction == 'up':
                    pyautogui.scroll(amount)
                elif scroll_direction == 'down':
                    pyautogui.scroll(-amount)
    elif action == 'sleep':
        time.sleep(int(args[-1]))

def input_command():
    while True:
        command = input('Enter command: ')
        if command == 'exit':
            break
        process_command(command)

def read_instructions(file_path):
    with open(file_path, 'r') as file:
        instructions = [line.strip() for line in file]
    return instructions

def load_file(file_path):
    instructions = read_instructions(file_path)
    for instruction in instructions:
        process_command(instruction)

if __name__ == '__main__':
    input_command()
