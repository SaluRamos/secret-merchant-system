import os
from scripts.encryption import Encryption
from scripts.interface import Interface
from scripts.variables import Vars
from scripts.general import General

if __name__ == "__main__":
    os.system("clear")
    Vars.encryption_key = General.get_password("type password key: ")
    print()
    try:
        Vars.load_products()
        Vars.load_trades()
    except:
        print("different password!")
        sure = input("are you sure (y/n)? ")
        if sure.lower() == "y":
            pass
        else:
            os._exit(0)
    os.system("clear")
    if Vars.products == {} and Vars.trades == []:
        print("THIS WILL BE YOUR NEW PASSWORD! REMEMBER IT!")
    Interface().create_window()
