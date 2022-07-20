from scripts.variables import Vars
from scripts.encryption import Encryption
from scripts.interface import Interface
import os

class Loader:

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
                new_trade = {'product':line.split(",")[0], 'quantity':float(line.split(",")[1]), 'sell_price':float(line.split(",")[2]), 'payment_method':line.split(",")[3], 'buyer_name':line.split(",")[4], 'total_cost':float(line.split(",")[5]), 'profit':float(line.split(",")[6]), 'transaction_date':line.split(",")[7].lower(), 'encrypted_line':encrypted_line, "comission_percent":float(line.split(",")[8]), "comission_name":line.split(",")[9]}
                new_trade['unix_date'] = Interface.get_date_timestamp(new_trade['transaction_date'])
                new_trade['id'] = Vars.next_trade_id
                Vars.next_trade_id += 1
                Vars.trades.append(new_trade)
            print()

    def load_debts() -> None:
        if os.path.exists("debts.txt") == False:
            with open("debts.txt", "w") as f:
                pass
        with open("debts.txt", "r") as f:
            debts = f.readlines()
            amount_debts = len(debts)
            for index, line in enumerate(debts):
                print(f"LOADING DEBT {index + 1} of {amount_debts}", end = "\r")
                encrypted_line = line.strip("\n")
                line = Encryption.password_decrypt(line, Vars.encryption_key)
                new_debt = {'value':float(line.split(",")[1]), 'encrypted_line':encrypted_line}
                Vars.debts[line.split(",")[0]] = new_debt
            print()