from scripts.general import General
import os
from scripts.encryption import Encryption

class Vars:

    encryption_key = ""
    products = {}
    trades = []
    payment_methods = ["dinheiro", "pix", "dinheiro e pix", "débito", "crédito", "fiado", "consumo", "desconhecido", "perdido/roubado", "agrado/presente"]
    sleeping_time = 0
    max_sleep_time = 300
    months_to_number = {'jan':1, 'janeiro':1, 'feb':2, 'fev':2, 'fevereiro':2, 'mar':3, 'março':3, 'apr':4, 'abr':4, 'abril':4, 'may':5, 'mai':5, 'maio':5, 'jun':6, 'junho':6, 'jul':7, 'julho':7, 'aug':8, 'ago':8, 'agosto':8, 'sep':9, 'set':9, 'setembro':9, 'oct':10, 'out':10, 'outubro':10, 'nov':11, 'novembro':11, 'dec':12, 'dez':12, 'dezembro':12}

    def load_products() -> None:
        if os.path.exists("products.txt") == False:
            with open("trades.txt", "w") as f:
                pass
        with open("products.txt", "r") as f:
            products = f.readlines()
            amount_products = len(products)
            for index, line in enumerate(products):
                print(f"LOADING PRODUCT {index + 1} of {amount_products}", end = "\r")
                encrypted_line = line.strip("\n")
                line = Encryption.password_decrypt(line, Vars.encryption_key)
                Vars.products[line.split(",")[0]] = {'buy_price':float(line.split(",")[1]), 'stock':float(line.split(",")[2]), 'encrypted_line':encrypted_line}
            print()

    def load_trades() -> None:
        if os.path.exists("trades.txt") == False:
            with open("trades.txt", "w") as f:
                pass
        with open("trades.txt", "r") as f:
            trades = f.readlines()
            amount_trades = len(trades)
            for index, line in enumerate(trades):
                print(f"LOADING TRADE {index + 1} of {amount_trades}", end = "\r")
                encrypted_line = line.strip("\n")
                line = Encryption.password_decrypt(line, Vars.encryption_key)
                Vars.trades.append({'product':line.split(",")[0], 'quantity':float(line.split(",")[1]), 'sell_price':float(line.split(",")[2]), 'payment_method':line.split(",")[3], 'buyer_name':line.split(",")[4], 'total_cost':float(line.split(",")[5]), 'profit':float(line.split(",")[6]), 'transaction_date':line.split(",")[7], 'encrypted_line':encrypted_line})
            print()