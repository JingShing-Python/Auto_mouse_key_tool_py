import keyboard
import pyautogui
import time

def process_command(command):
    print(command)
    parts = command.split()
    if len(parts) > 0:
        action, *args = parts
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
    else:
        print("Invalid command: No action specified.")

def input_command():
    loop_instructions = []
    i = 0
    instructions = []
    while True:
        instruction = instructions[i]
        if instruction == 'exit':
            break
        elif 'loop' in instruction:
            if instruction.split()[-1] != 'end':
                loop_count = int(instruction.split()[-1]) if len(instruction.split()) > 0 else 1
            loop_instructions = []
            i += 1
            while i < len(instructions) and instructions[i] != 'loop end':
                loop_instructions.append(instructions[i])
                i += 1
            for _ in range(loop_count):
                for loop_instruction in loop_instructions:
                    process_command(loop_instruction)
        elif 'if' in instruction and 'endif' not in instruction:
            if_parts = instruction.split()
            if len(if_parts) >= 3:
                condition_type = if_parts[1]
                condition_value = ' '.join(if_parts[2:])
                if condition_type == 'image':
                    if pyautogui.locateOnScreen(condition_value):
                        nested_if_count = 1
                        nested_endif_count = 0
                        i += 1
                        while nested_if_count > nested_endif_count:
                            nested_instruction = instructions[i]
                            if 'endif' in nested_instruction:
                                nested_endif_count += 1
                            elif 'if' in nested_instruction:
                                nested_if_count += 1
                            process_command(nested_instruction)
                            i += 1
                    else:
                        i = skip_else_block(instructions, i)
                elif condition_type == 'mouse':
                    mouse_x, mouse_y = map(int, condition_value.split(','))
                    current_x, current_y = pyautogui.position()
                    if current_x == mouse_x and current_y == mouse_y:
                        nested_if_count = 1
                        nested_endif_count = 0
                        i += 1
                        while nested_if_count > nested_endif_count:
                            nested_instruction = instructions[i]
                            if 'endif' in nested_instruction:
                                nested_endif_count += 1
                            elif 'if' in nested_instruction:
                                nested_if_count += 1
                            process_command(nested_instruction)
                            i += 1
                    else:
                        i = skip_else_block(instructions, i)
                else:
                    print(f"Invalid condition type in if statement: {condition_type}")
                    i += 1
            else:
                print(f"Invalid if statement: {instruction}")
                i += 1
        else:
            process_command(instruction)
            i += 1


def read_instructions(file_path):
    with open(file_path, 'r') as file:
        instructions = [line.strip() for line in file]
    return instructions

def load_file(file_path):
    instructions = read_instructions(file_path)
    i = 0
    while i < len(instructions):
        instruction = instructions[i]
        if instruction == 'exit':
            break
        elif 'loop' in instruction:
            if instruction.split()[-1] != 'end':
                loop_count = int(instruction.split()[-1]) if len(instruction.split()) > 0 else 1
            
            loop_instructions = []
            i += 1
            while i < len(instructions) and instructions[i] != 'loop end':
                loop_instructions.append(instructions[i])
                i += 1
            print(loop_instructions)
            for _ in range(loop_count):
                for loop_instruction in loop_instructions[0:]:
                    print(loop_instruction)
                    process_command(loop_instruction)
        elif 'if' in instruction and not 'endif' in instruction:
            if_parts = instruction.split()
            if len(if_parts) >= 3:
                condition_type = if_parts[1]
                condition_value = ' '.join(if_parts[2:])
                if condition_type == 'image':
                    if pyautogui.locateOnScreen(condition_value):
                        nested_if_count = 1
                        nested_endif_count = 0
                        i += 1
                        while nested_if_count > nested_endif_count:
                            nested_instruction = instructions[i]
                            if 'endif' in nested_instruction:
                                nested_endif_count += 1
                            elif 'if' in nested_instruction:
                                nested_if_count += 1
                            process_command(nested_instruction)
                            i += 1
                    else:
                        i = skip_else_block(instructions, i)
                elif condition_type == 'mouse':
                    mouse_x, mouse_y = map(int, condition_value.split(','))
                    current_x, current_y = pyautogui.position()
                    if current_x == mouse_x and current_y == mouse_y:
                        nested_if_count = 1
                        nested_endif_count = 0
                        i += 1
                        while nested_if_count > nested_endif_count:
                            nested_instruction = instructions[i]
                            if 'endif' in nested_instruction:
                                nested_endif_count += 1
                            elif 'if' in nested_instruction:
                                nested_if_count += 1
                            process_command(nested_instruction)
                            i += 1
                    else:
                        i = skip_else_block(instructions, i)
                else:
                    print(f"Invalid condition type in if statement: {condition_type}")
                    i += 1
            else:
                print(f"Invalid if statement: {instruction}")
                i += 1
        else:
            process_command(instruction)
            i += 1

def skip_else_block(instructions, start_index):
    nested_if_count = 0
    nested_endif_count = 1
    i = start_index + 1
    while nested_if_count > nested_endif_count:
        nested_instruction = instructions[i]
        if 'endif' in nested_instruction:
            nested_endif_count += 1
        elif 'if' in nested_instruction:
            nested_if_count += 1
        i += 1
    return i

if __name__ == '__main__':
    # input_command()
    load_file("test.txt")
