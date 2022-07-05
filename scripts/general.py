import os
import getch
import time

class General:

    def get_password(value: str, character_substitute: str = "*") -> str:
        password = ''
        initial_chars = len(value)
        line = value
        while True:
            print(line, end = "\r")
            new_char = getch.getch()
            if new_char == "\r" or new_char == "\n":
                break
            if ord(new_char) == 127 and len(line) > initial_chars:
                line = line[0:len(line)-1]
                password = password[0:len(password)-1]
            elif ord(new_char) != 127:
                line = f"{line}{character_substitute}"
                password = f"{password}{new_char}"
            print("                                        ", end = "\r")
        print()
        return password