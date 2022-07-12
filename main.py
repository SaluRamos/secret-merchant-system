from doctest import testfile
import os
import platform
from scripts.encryption import Encryption
from scripts.interface import Interface
from scripts.variables import Vars
from scripts.general import General
from scripts.loader import Loader

def clear_terminal() -> None:
        system_type = platform.system()
        if system_type == "Windows":
            os.system("cls")
        elif system_type == "Linux":
            os.system("clear")

if __name__ == "__main__":
    clear_terminal()
    Vars.encryption_key = General.get_password("type password key: ")
    clear_terminal()
    try:
        Loader.load_products()
        Loader.load_trades()
    except:
        print("different password!         ")
        sure = input("are you sure (y/n)? ")
        if sure.lower() == "y":
            pass
        else:
            os._exit(0)
    clear_terminal()
    if Vars.products == {} and Vars.trades == []:
        print("THIS WILL BE YOUR NEW PASSWORD! REMEMBER IT!")
    Interface().create_window()
