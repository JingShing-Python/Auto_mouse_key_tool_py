import keyboard
import pyautogui
import time

def process_command(command):
    parts = command.split()
    if len(parts) < 2:
        return

    action = parts[0]
    parameters = ' '.join(parts[1:])

    if action == 'key':
        # key is mean keyboard
        # it will simulate keyboard to key in
        # key string
        keyboard.write(parameters)
    elif action == 'mouse':
        if parameters.startswith('move'):
            # mouse move relative dx dy
            # mouse move absolute x y
            # mouse move image image_path
            _, move_type, *values = parameters.split()
            if move_type == 'relative':
                x, y = map(int, values)
                current_x, current_y = pyautogui.position()
                target_x = current_x + x
                target_y = current_y + y
                pyautogui.moveTo(target_x, target_y)
            elif move_type == 'absolute':
                x, y = map(int, values)
                pyautogui.moveTo(x, y)
            elif move_type == 'image':
                _, image_path = parameters.split()
                center = pyautogui.locateCenterOnScreen(image_path)
                if center:
                    x, y = center
                    pyautogui.moveTo(x, y)
        elif 'click' in parameters:
            if 'right' in parameters:
                pyautogui.click(button='right')
            elif 'left'in parameters:
                pyautogui.click(button='left')
    elif action == 'sleep':
        time.sleep(int(parameters.split()[-1]))

def input_command():
    while True:
        command = input('Enter command: ')
        if command == 'exit':
            break
        process_command(command)

def read_instructions(file_path):
    instructions = []
    with open(file_path, 'r') as file:
        for line in file:
            instructions.append(line.strip())
    print(instructions)
    return instructions

def load_file(file_path):
    instructions = read_instructions(file_path)
    for i in instructions:
        process_command(i)

if __name__ == '__main__':
    input_command()
