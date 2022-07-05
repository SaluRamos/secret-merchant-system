from tkinter import *
from scripts.encryption import Encryption
import sys
import os

class Vars:

    encryption_key = "arnoldzilla321"
    products = {'bucha':{'stock':5, 'buy_price':2}}
    trades = []
    payment_methods = ["dinheiro", "pix", "débito", "crédito", "fiado"]
    sleeping_time = 0
    max_sleep_time = 300
    months_to_number = {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6, 'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}

    def load_products() -> None:
        # if os.path.exists("products.txt") == False:
        #     with open("trades.txt", "w") as f:
        #         pass
        with open("products.txt", "r") as f:
            for line in f.readlines():
                line = Encryption.password_decrypt(line, Vars.encryption_key)
                Vars.products[line.split(",")[0]] = {'buy_price':float(line.split(",")[1]), 'stock':float(line.split(",")[2])}

    def load_trades() -> None:
        # if os.path.exists("trades.txt") == False:
        #     with open("trades.txt", "w") as f:
        #         pass
        with open("trades.txt", "r") as f:
            for line in f.readlines():
                line = Encryption.password_decrypt(line, Vars.encryption_key)
                Vars.trades.append({'product':line.split(",")[0], 'quantity':float(line.split(",")[1]), 'sell_price':float(line.split(",")[2]), 'payment_method':line.split(",")[3], 'buyer_name':line.split(",")[4], 'total_cost':float(line.split(",")[5]), 'profit':float(line.split(",")[6]), 'transaction_date':line.split(",")[7]})



