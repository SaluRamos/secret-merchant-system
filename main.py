import os
import platform
import time
from scripts.encryption import Encryption
from scripts.interface import Interface
from scripts.variables import Vars
from scripts.general import General
from scripts.loader import Loader



if __name__ == "__main__":
    General.clear_terminal()
    Vars.encryption_key = General.get_password("type password key: ")
    General.clear_terminal()
    try:
        Loader.load_products()
        Loader.load_trades()
        Loader.load_debts()
        # esse código serve para atualizar products.txt e trades.txt durante desenvolvimento
        # Interface.full_update_trades()
        # os._exit(0)
    except:
        print("different password!         ")
        sure = input("are you sure (y/n)? ")
        if sure.lower() == "y":
            pass
        else:
            os._exit(0)
    General.clear_terminal()
    if Vars.products == {} and Vars.trades == []:
        print("THIS WILL BE YOUR NEW PASSWORD! REMEMBER IT!")
    Interface().create_window()
