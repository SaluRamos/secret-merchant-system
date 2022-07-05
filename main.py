import os
from tkinter import *
from scripts.encryption import Encryption
from scripts.interface import Interface
from scripts.variables import Vars

if __name__ == "__main__":
    os.system("clear")
    Vars.load_products()
    Vars.load_trades()
    Interface().create_window()
