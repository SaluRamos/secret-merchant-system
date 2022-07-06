import os
import getch
import time

class General:

    def get_password(value: str, character_substitute: str = "*", resize_adjust: bool = True) -> str:
        password = ''
        initial_chars = len(value)
        line = value
        if resize_adjust == False:
            reset_line = ""
            for i in range(os.get_terminal_size().columns):
                reset_line = f"{reset_line} "
        while True:
            print(line, end = "\r")
            new_char = getch.getch()
            if new_char == "\r" or new_char == "\n":
                break
            if ord(new_char) == 127 and len(line) > initial_chars:
                line = line[0:len(line)-1]
                password = password[0:len(password)-1]
            elif ord(new_char) != 127 and (len(line)+len(password)) <= os.get_terminal_size().columns:
                line = f"{line}{character_substitute}"
                password = f"{password}{new_char}"
            if resize_adjust == True:
                reset_line = ""
                for i in range(os.get_terminal_size().columns):
                    reset_line = f"{reset_line} "
            print(reset_line, end = "\r")
        print()
        return password