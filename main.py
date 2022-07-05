import os
from tkinter import *
from scripts.encryption import Encryption
from scripts.interface import Interface
from scripts.variables import Vars

if __name__ == "__main__":
    os.system("clear")
    try:
        Vars.load_products()
        Vars.load_trades()
    except:
        print("different password!")
        os._exit(0)
    if Vars.products == {} and Vars.trades == []:
        print("THIS WILL BE YOUR NEW PASSWORD! REMEMBER IT!")
    Interface().create_window()
