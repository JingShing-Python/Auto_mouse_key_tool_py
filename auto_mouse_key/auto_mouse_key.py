import keyboard
import pyautogui
import time

def process_command(command):
    action, *args = command.split()

    key_actions = ['key', 'hold', 'press', 'release']
    mouse_actions = ['move', 'click', 'scroll']
    click_types = ['left', 'right']
    scroll_directions = ['up', 'down']

    if action in key_actions:
        # keyboard action
        if action == 'key':
            keyboard.write(' '.join(args))
        elif action == 'press':
            key = ' '.join(args)
            keyboard.press(key)
            keyboard.release(key)
        elif action == 'hold':
            key = ' '.join(args)
            keyboard.press(key)
        elif action == 'release':
            key = ' '.join(args)
            keyboard.release(key)
    elif action in mouse_actions:
        # mouse action
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
    i = 0
    while i < len(instructions):
        instruction = instructions[i]
        if instruction == 'loop':
            print("AAA")
            loop_instructions = []
            i += 1
            while i < len(instructions) and instructions[i] != 'loop end':
                loop_instructions.append(instructions[i])
                i += 1
            loop_count = int(loop_instructions[0]) if len(loop_instructions) > 0 else 1
            print(loop_instructions)
            for _ in range(loop_count):
                for loop_instruction in loop_instructions[1:]:
                    process_command(loop_instruction)
        else:
            process_command(instruction)
        i += 1

if __name__ == '__main__':
    # input_command()
    load_file("test.txt")
