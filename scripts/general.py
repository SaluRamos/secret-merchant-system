from base64 import decode
import os
import time
import platform

class General:

    def clear_terminal() -> None:
        system_type = platform.system()
        if system_type == "Windows":
            os.system("cls")
        elif system_type == "Linux":
            os.system("clear")

    def atual_date():
        return time.strftime("%d/%b/%y")

    def get_password(value: str, character_substitute: str = "*", resize_adjust: bool = True) -> str:
        password = ''
        initial_chars = len(value)
        line = value
        if resize_adjust == False:
            reset_line = ""
            for i in range(os.get_terminal_size().columns):
                reset_line = f"{reset_line} "
        if platform.system() == "Linux":
            try:
                import getch
                getchar_func = getch.getch
            except:
                pass
        elif platform.system() == "Windows":
            try:
                import msvcrt
                getchar_func = msvcrt.getch
            except:
                pass
        while True:
            print(line, end = "\r")
            new_char = getchar_func().decode("utf-8")
            if new_char == "\r" or new_char == "\n":
                break
            if (ord(new_char) == 127  or ord(new_char) == 8) and len(line) > initial_chars:
                line = line[0:len(line)-1]
                password = password[0:len(password)-1]
            elif ord(new_char) != 127 and ord(new_char) != 8 and (len(line)+len(password)) <= os.get_terminal_size().columns:
                if character_substitute != "":
                    line = f"{line}{character_substitute}"
                else:
                    line = f"{line}{new_char}"
                password = f"{password}{new_char}"
            if resize_adjust == True:
                reset_line = ""
                for i in range(os.get_terminal_size().columns):
                    reset_line = f"{reset_line} "
            print(reset_line, end = "\r")
        print()
        return password