import os
import time
from datetime import datetime
from datetime import date
import re
import random
import ctypes

kernel32 = ctypes.windll.kernel32
kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)


class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def find_number(file_name):
    with open(file_name) as f:
        for line in f:
            s = re.search(r'\d+', line)
            if s:
                return line


def delete_line(file_name):
    with open(file_name, 'r') as fin:
        data = fin.read().splitlines(True)
    with open(file_name, 'w') as fout:
        fout.writelines(data[1:])


def prepend_line(file_name, line):
    """ Insert given string as a new line at the beginning of a file """
    # define name of temporary dummy file
    dummy_file = file_name + '.bak'
    # open original file in read mode and dummy file in write mode
    with open(file_name, 'r') as read_obj, open(dummy_file, 'w') as write_obj:
        # Write given line to the dummy file
        write_obj.write(line + '\n')
        # Read lines from original file one by one and append them to the dummy file
        for line in read_obj:
            write_obj.write(line)
    # remove original file
    os.remove(file_name)
    # Rename dummy file as the original file
    os.rename(dummy_file, file_name)


def println(message, name):
    save_path = 'C:\\thoughts'
    file_name = "thoughts.txt"
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    complete_name = os.path.join(save_path, file_name)
    # total = find_number(complete_name) + number
    words = find_number(complete_name).split()
    total = int(words[-1]) + 1
    with open(complete_name) as f:
        lines = f.read()
        first = lines.split('\n', 1)[0]
    if first != f"total thoughts recorded : {total}":
        delete_line(complete_name)
        prepend_line(complete_name, f"total thoughts recorded : {total}")
    text_file = open(complete_name, "a")
    text_to_write = f'thought #{total}' \
                    f'\n{date.today().strftime("%B %d, %Y")}' \
                    f' | ' \
                    f'{datetime.now().strftime("%H:%M:%S")}' \
                    f'\n{message}' \
                    f'\n{name}' \
                    f'\n\n '
    text_file.write(text_to_write)
    text_file.close()
    print(f"thought #{total} recorded")


if __name__ == '__main__':
    keep_on = True
    thoughts = 0
    messages = [
        "calling all thoughts !",
        "thinking...",
        "head empty , no thoughts",
        "what was i doing ?",
        "trying my best to remember...",
    ]
    welcome = random.choice(messages)
    print("welcome to the thought recorder")
    print(f"{Colors.HEADER}{welcome}{Colors.END}\n")
    while keep_on:
        if thoughts > 0:
            user = input(f"{Colors.CYAN}record another thought ? [Y/N]{Colors.END} ")
        else:
            user = input(f"{Colors.CYAN}record thought ? [Y/N]{Colors.END} ")
        if user != "y":
            keep_on = False
        else:
            thoughts += 1
            println(input(f"{Colors.GREEN}thought :{Colors.END} "), input(f"{Colors.GREEN}author :{Colors.END} "))
    print(f"{Colors.HEADER}thanks for using the thought recorder :){Colors.END}")
    print(f"thoughts recorded : {Colors.BOLD}{thoughts}{Colors.END}")
    time.sleep(3)
