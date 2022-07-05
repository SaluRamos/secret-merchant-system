from tkinter import *
from scripts.encryption import Encryption
import sys
import os

class Vars:

    def load_products(key) -> dict:
        products = {}
        open_method = "r"
        if os.path.exists("products.txt") == False:
            open_method = "w"
        with open("products.txt", open_method) as f:
            for line in f.readlines():
                line = Encryption.password_decrypt(line, key)
                products[line.split(",")[0]] = {'buy_price':float(line.split(",")[1]), 'stock':float(line.split(",")[2])}
        return products

    def load_trades(key) -> dict:
        products = {}
        open_method = "r"
        if os.path.exists("trades.txt") == False:
            open_method = "w"
        with open("trades.txt", open_method) as f:
            for line in f.readlines():
                line = Encryption.password_decrypt(line, key)
                products[line.split(",")[0]] = {'buy_price':float(line.split(",")[1]), 'stock':float(line.split(",")[2])}
        return products

    encryption_key = "arnoldzilla321"
    products = load_products(encryption_key)
    trades = load_trades(encryption_key)
    payment_methods = ["dinheiro", "pix", "débito", "crédito", "fiado"]