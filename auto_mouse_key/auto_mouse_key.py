import keyboard
import pyautogui
import time

def process_command(command):
    action, *args = command.split()

    key_actions = ['key']
    mouse_actions = ['move', 'click']
    click_types = ['right', 'left']

    if action in key_actions:
        # keyboard action
        # key string
        keyboard.write(' '.join(args))
    elif action in mouse_actions:
        # mouse action
        # move relative(r) dx dy
        # move absolute(a) x y
        # move image(i) image_path
        # click right
        # click left
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
            click_type = args[0]
            if click_type in click_types:
                pyautogui.click(button=click_type)
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
