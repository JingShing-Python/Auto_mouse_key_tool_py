import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import threading
import time
import pyautogui
import keyboard

instructions = []
file_path = ""
is_running = False

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

def load_instructions(old_file_path=None):
    global instructions
    global file_path
    if old_file_path == None:
        file_path = filedialog.askopenfilename(filetypes=[('Text Files', '*.txt')])
    else:
        file_path = old_file_path
    if file_path:
        with open(file_path, 'r') as file:
            instructions = [line.strip() for line in file]
        update_listbox()

def save_instructions():
    global instructions
    file_path = filedialog.asksaveasfilename(filetypes=[('Text Files', '*.txt')])
    if file_path:
        with open(file_path, 'w') as file:
            file.write('\n'.join(instructions))
        messagebox.showinfo('Save', 'Instructions saved successfully.')

def update_listbox():
    listbox.delete(0, tk.END)
    for instruction in instructions:
        listbox.insert(tk.END, instruction)

def add_instruction():
    instruction = input_entry.get()
    if instruction:
        selected_index = listbox.curselection()
        if selected_index:
            index = selected_index[0] + 1
            instructions.insert(index, instruction)
        else:
            instructions.append(instruction)
        update_listbox()
        input_entry.delete(0, tk.END)

def edit_instruction():
    selected_index = listbox.curselection()
    if selected_index:
        index = selected_index[0]
        instruction = input_entry.get()
        if instruction:
            instructions[index] = instruction
            update_listbox()
            input_entry.delete(0, tk.END)

def delete_instruction():
    selected_index = listbox.curselection()
    if selected_index:
        index = selected_index[0]
        del instructions[index]
        update_listbox()

def refresh_instructions():
    global file_path
    load_instructions(file_path)
    update_listbox()

def play_instructions():
    global is_running
    if not is_running:
        is_running = True
        play_button.config(state=tk.DISABLED)
        stop_button.config(state=tk.NORMAL)
        thread = threading.Thread(target=run_instructions)
        thread.start()

def stop_instructions():
    global is_running
    is_running = False
    play_button.config(state=tk.NORMAL)
    stop_button.config(state=tk.DISABLED)

def run_instructions():
    global is_running
    i = 0
    while i < len(instructions) and is_running:
        instruction = instructions[i]
        if instruction == 'exit':
            break
        elif 'loop' in instruction and not 'end' in instruction:
            if instruction.split()[-1] != 'end':
                loop_count = int(instruction.split()[-1]) if len(instruction.split()) > 0 else 1
            
            loop_instructions = []
            i += 1
            while i < len(instructions) and instructions[i] != 'loop end' and is_running:
                loop_instructions.append(instructions[i])
                i += 1
            if loop_count == -1:
                while is_running:
                    if keyboard.is_pressed('esc'):
                        break
                    for loop_instruction in loop_instructions[0:]:
                        process_command(loop_instruction)
            else:
                for _ in range(loop_count):
                    if not is_running:
                        break
                    for loop_instruction in loop_instructions[0:]:
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
                        while nested_if_count > nested_endif_count and is_running:
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
                        while nested_if_count > nested_endif_count and is_running:
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

    is_running = False
    play_button.config(state=tk.NORMAL)
    stop_button.config(state=tk.DISABLED)

# GUI initialization
root = tk.Tk()
root.title('Instruction Manager')

# Frame for the left side containing the listbox
listbox_frame = tk.Frame(root, width=300, padx=10, pady=10)
listbox_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Listbox with scrollbar
listbox_scrollbar = tk.Scrollbar(listbox_frame)
listbox_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

listbox = tk.Listbox(listbox_frame, yscrollcommand=listbox_scrollbar.set)
listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

listbox_scrollbar.config(command=listbox.yview)

# Frame for the right side containing the input and buttons
input_frame = tk.Frame(root, padx=10, pady=10)
input_frame.pack(side=tk.RIGHT, fill=tk.BOTH)

# Input entry
input_entry = tk.Entry(input_frame)
input_entry.pack(side=tk.LEFT, padx=5)

# Add button
add_button = tk.Button(input_frame, text='Add', command=add_instruction)
add_button.pack(side=tk.LEFT, padx=5)

# Edit button
edit_button = tk.Button(input_frame, text='Edit', command=edit_instruction)
edit_button.pack(side=tk.LEFT, padx=5)

# Delete button
delete_button = tk.Button(input_frame, text='Delete', command=delete_instruction)
delete_button.pack(side=tk.LEFT, padx=5)

# Refresh button
refresh_button = tk.Button(input_frame, text='Refresh', command=refresh_instructions)
refresh_button.pack(side=tk.LEFT, padx=5)

# Button frame for play and stop buttons
button_frame = tk.Frame(root, padx=10, pady=10)
button_frame.pack(side=tk.BOTTOM)

# Play button
play_button = tk.Button(button_frame, text='Play',command=play_instructions)
play_button.pack(side=tk.LEFT, padx=5)

# Stop button
stop_button = tk.Button(button_frame, text='Stop', command=stop_instructions, state=tk.DISABLED)
stop_button.pack(side=tk.LEFT, padx=5)

# Load button
load_button = tk.Button(root, text='Load', command=load_instructions)
load_button.pack(side=tk.TOP, padx=10, pady=5)

# Save button
save_button = tk.Button(root, text='Save', command=save_instructions)
save_button.pack(side=tk.TOP, padx=10, pady=5)

root.mainloop()
