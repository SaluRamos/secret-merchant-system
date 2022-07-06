from scripts.variables import Vars
from scripts.encryption import Encryption
from tkinter import *
from tkinter import _setit as tkinter_set_it
from colorama import Style, Fore
import threading
import time
import os
import datetime

class Interface:

    def __init__(self) -> None:
        self.main_root = Tk()
        self.main_menu = Menu(self.main_root)

    def profit_last_days(max_days: int) -> float:
        profit = 0
        atual_timestamp = time.time()
        for i in Vars.trades:
            trade_date = i['transaction_date'].split(" ")[0].lower()
            if len(trade_date.split('/')[2]) == 2:
                trade_year = int(f"20{trade_date.split('/')[2]}")
            else:
                trade_year = int(trade_date.split('/')[2])
            if trade_date.split("/")[1] not in Vars.months_to_number.keys():
                trade_month = int(trade_date.split("/")[1])
            else:
                trade_month = Vars.months_to_number[trade_date.split("/")[1]]
            trade_dt = datetime.datetime(trade_year, trade_month, int(trade_date.split("/")[0])) #year, month, day
            trade_timestamp = trade_dt.replace(tzinfo = datetime.timezone.utc).timestamp()
            if (atual_timestamp-trade_timestamp)/86400 <= max_days:
                profit += i['profit']
        return round(profit, 2)

    def main_loop(self) -> None:
        while True:
            try:
                quantity = float(self.main_menu.trade_input2.get())
                sell_price = float(self.main_menu.trade_input3.get())
                total_cost = round(quantity*sell_price, 2)
                product_cost = Vars.products[self.main_menu.trade_input1_variable.get()]['buy_price']
                profit = round(total_cost-(product_cost*quantity), 2)
                self.main_menu.trade_totalcost_variable.set(str(total_cost))
                self.main_menu.trade_profit_variable.set(str(profit))
            except:
                pass
            time.sleep(0.1)
            Vars.sleeping_time += 0.1
            self.main_menu.sleeping_time['text'] = f"sleeping time: {round(Vars.sleeping_time, 1)}"
            if Vars.sleeping_time >= Vars.max_sleep_time:
                os._exit(0)

    def update_profit(self) -> None:
        self.main_menu.profit_last7days['text'] = f"lucro últimos 7 dias: {Interface.profit_last_days(7)}"
        self.main_menu.profit_last14days['text'] = f"lucro últimos 14 dias: {Interface.profit_last_days(14)}"
        self.main_menu.profit_last21days['text'] = f"lucro últimos 21 dias: {Interface.profit_last_days(21)}"
        self.main_menu.profit_last28days['text'] = f"lucro últimos 28 dias: {Interface.profit_last_days(28)}"

    def create_window(self) -> None:
        self.main_root.resizable(False, False)
        self.main_root.geometry("900x600")
        self.main_root.config(menu = self.main_menu)
        # self.main_root.iconbitmap(r"images/icon.ico")
        self.main_root.title("SECRET MERCHANT SYSTEM")
        self.interface_font1 = ("Arial", "10")
        self.interface_font2 = ("Arial", "9")
        self.interface_font3 = ("Arial", "10", "bold")
        #new trade interface
        self.main_menu.trade_summary1 = Label(self.main_root, text = "PRODUTO", font = self.interface_font1)
        self.main_menu.trade_summary1.place(x = 10, y = 300)
        self.main_menu.trade_input1_variable = StringVar(self.main_root)
        self.main_menu.trade_input1_variable.set("selecione")
        product_options = list(Vars.products.keys())
        if product_options == []:
            product_options.append("selecione")
        self.main_menu.trade_input1 = OptionMenu(self.main_root, self.main_menu.trade_input1_variable, *product_options)
        self.main_menu.trade_input1.place(x = 220, y = 300, width = 150, height = 25)
        self.main_menu.trade_input1.config(indicatoron = False)
        self.main_menu.trade_summary2 = Label(self.main_root, text = "QTD", font = self.interface_font1)
        self.main_menu.trade_summary2.place(x = 10, y = 325)
        self.main_menu.trade_input2 = Entry(self.main_root, font = self.interface_font1, justify = "center")
        self.main_menu.trade_input2.place(x = 220, y = 325, width = 150, height = 25)
        self.main_menu.trade_summary3 = Label(self.main_root, text = "PREÇO DE VENDA", font = self.interface_font1)
        self.main_menu.trade_summary3.place(x = 10, y = 350)
        self.main_menu.trade_input3 = Entry(self.main_root, font = self.interface_font1, justify = "center")
        self.main_menu.trade_input3.place(x = 220, y = 350, width = 150, height = 25)
        self.main_menu.trade_summary4 = Label(self.main_root, text = "MÉTODO DE PAGAMENTO", font = self.interface_font1)
        self.main_menu.trade_summary4.place(x = 10, y = 375)
        self.main_menu.trade_input4_variable = StringVar(self.main_root)
        self.main_menu.trade_input4_variable.set("selecione")
        self.main_menu.trade_input4 = OptionMenu(self.main_root, self.main_menu.trade_input4_variable, *Vars.payment_methods)
        self.main_menu.trade_input4.place(x = 220, y = 375, width = 150, height = 25)
        self.main_menu.trade_input4.config(indicatoron = False)
        self.main_menu.trade_summary5 = Label(self.main_root, text = "NOME DO COMPRADOR", font = self.interface_font1)
        self.main_menu.trade_summary5.place(x = 10, y = 400)
        self.main_menu.trade_input5 = Entry(self.main_root, font = self.interface_font1, justify = "center")
        self.main_menu.trade_input5.place(x = 220, y = 400, width = 150, height = 25)
        self.main_menu.trade_summary6 = Label(self.main_root, text = "CUSTO TOTAL", font = self.interface_font1)
        self.main_menu.trade_summary6.place(x = 10, y = 425)
        self.main_menu.trade_totalcost_variable = StringVar()
        self.main_menu.trade_totalcost_variable.set("...")
        self.main_menu.trade_output6 = Label(self.main_root, textvariable = self.main_menu.trade_totalcost_variable, font = self.interface_font1, justify = "center")
        self.main_menu.trade_output6.place(x = 220, y = 425, width = 150)
        self.main_menu.trade_summary7 = Label(self.main_root, text = "LUCRO", font = self.interface_font1)
        self.main_menu.trade_summary7.place(x = 10, y = 450)
        self.main_menu.trade_profit_variable = StringVar()
        self.main_menu.trade_profit_variable.set("...")
        self.main_menu.trade_output7 = Label(self.main_root, textvariable = self.main_menu.trade_profit_variable, font = self.interface_font1, justify = "center")
        self.main_menu.trade_output7.place(x = 220, y = 450, width = 150)
        self.main_menu.trade_summary8 = Label(self.main_root, text = "DATA (DIA/MÊS/ANO)", font = self.interface_font1)
        self.main_menu.trade_summary8.place(x = 10, y = 475)
        self.main_menu.trade_input8 = Entry(self.main_root, text = "", font = self.interface_font1, justify = "center")
        self.main_menu.trade_input8.place(x = 220, y = 475, width = 150, height = 25)
        self.main_menu.trade_finish = Button(self.main_root, text = "FINALIZAR TRANSAÇÃO", font = self.interface_font3, command = lambda *args : Interface.trade_button(self))
        self.main_menu.trade_finish.place(x = 10, y = 500, width = 360, height = 25)
        self.main_menu.trade_error = Label(self.main_root, text = "teste\nteste", font = self.interface_font3, fg = "red", bg = "cyan")
        self.main_menu.trade_error.place(x = 10, y = 530, width = 360)
        self.main_menu.trade_remove = Button(self.main_root, text = "REMOVER ÚLTIMA TRANSAÇÃO", font = self.interface_font3, command = lambda *args : Interface.remove_last_trade(self))
        self.main_menu.trade_remove.place(x = 10, y = 570, width = 360, height = 25)
        #new/update product interface
        self.main_menu.newproduct_summary1 = Label(self.main_root, text = "NOME", font = self.interface_font1)
        self.main_menu.newproduct_summary1.place(x = 380, y = 300)
        self.main_menu.newproduct_input1 = Entry(self.main_root, font = self.interface_font1, justify = "center")
        self.main_menu.newproduct_input1.place(x = 530, y = 300, width = 160, height = 25)
        self.main_menu.newproduct_summary2 = Label(self.main_root, text = "PREÇO DE CUSTO", font = self.interface_font1)
        self.main_menu.newproduct_summary2.place(x = 380, y = 325)
        self.main_menu.newproduct_input2 = Entry(self.main_root, font = self.interface_font1, justify = "center")
        self.main_menu.newproduct_input2.place(x = 530, y = 325, width = 160, height = 25)
        self.main_menu.newproduct_summary3 = Label(self.main_root, text = "STOCK", font = self.interface_font1)
        self.main_menu.newproduct_summary3.place(x = 380, y = 350)
        self.main_menu.newproduct_input3 = Entry(self.main_root, font = self.interface_font1, justify = "center")
        self.main_menu.newproduct_input3.place(x = 530, y = 350, width = 160, height = 25)
        self.main_menu.newproduct_finish = Button(self.main_root, text = "ADICIONAR / ATUALIZAR PRODUTO", font = self.interface_font3, command = lambda *args : Interface.product_button(self))
        self.main_menu.newproduct_finish.place(x = 380, y = 375, width = 310, height = 25)
        self.main_menu.products_summary1 = Label(self.main_root, text = "NOME", font = self.interface_font1)
        self.main_menu.products_summary1.place(x = 380, y = 400)
        self.main_menu.products_summary1 = Label(self.main_root, text = "CUSTO", font = self.interface_font1)
        self.main_menu.products_summary1.place(x = 590, y = 400)
        self.main_menu.products_summary1 = Label(self.main_root, text = "STOCK", font = self.interface_font1)
        self.main_menu.products_summary1.place(x = 640, y = 400)
        self.main_menu.products_scrollbar = Scrollbar(orient = "vertical", command = self.on_scroll_products)
        self.main_menu.products_scrollbar.place(x = 695, y = 300, width = 15, height = 293)
        self.main_menu.products_names = Listbox(self.main_root, font = self.interface_font2, justify = "center", yscrollcommand = self.main_menu.products_scrollbar.set)
        self.main_menu.products_names.place(x = 380, y = 420, width = 210, height = 175)
        self.main_menu.products_buyprice = Listbox(self.main_root, font = self.interface_font2, justify = "center", yscrollcommand = self.main_menu.products_scrollbar.set)
        self.main_menu.products_buyprice.place(x = 590, y = 420, width = 50, height = 175)
        self.main_menu.products_stock = Listbox(self.main_root, font = self.interface_font2, justify = "center", yscrollcommand = self.main_menu.products_scrollbar.set)
        self.main_menu.products_stock.place(x = 640, y = 420, width = 50, height = 175)
        Interface.update_product_table(self)
        #db trades interface
        self.main_menu.trade_scrollbar = Scrollbar(orient = "vertical", command = self.on_scroll_trades)
        self.main_menu.trade_scrollbar.place(x = 695, y = 10, width = 15, height = 285)
        self.main_menu.trade_summary1 = Label(self.main_root, text = "PRODUTO", font = self.interface_font1)
        self.main_menu.trade_summary1.place(x = 10, y = 10)
        self.main_menu.trade_summary2 = Label(self.main_root, text = "QTD", font = self.interface_font1)
        self.main_menu.trade_summary2.place(x = 160, y = 10)
        self.main_menu.trade_summary3 = Label(self.main_root, text = "VENDA", font = self.interface_font1)
        self.main_menu.trade_summary3.place(x = 210, y = 10)
        self.main_menu.trade_summary4 = Label(self.main_root, text = "MÉTODO", font = self.interface_font1)
        self.main_menu.trade_summary4.place(x = 260, y = 10)
        self.main_menu.trade_summary5 = Label(self.main_root, text = "COMPRADOR", font = self.interface_font1)
        self.main_menu.trade_summary5.place(x = 360, y = 10)
        self.main_menu.trade_summary6 = Label(self.main_root, text = "CUSTO", font = self.interface_font1)
        self.main_menu.trade_summary6.place(x = 460, y = 10)
        self.main_menu.trade_summary7 = Label(self.main_root, text = "LUCRO", font = self.interface_font1)
        self.main_menu.trade_summary7.place(x = 510, y = 10)
        self.main_menu.trade_summary8 = Label(self.main_root, text = "DATA", font = self.interface_font1)
        self.main_menu.trade_summary8.place(x = 560, y = 10)
        self.main_menu.trade_names = Listbox(self.main_root, font = self.interface_font2, justify = "center", yscrollcommand = self.main_menu.trade_scrollbar.set)
        self.main_menu.trade_names.place(x = 10, y = 30, width = 150, height = 265)
        self.main_menu.trade_quantity = Listbox(self.main_root, font = self.interface_font2, justify = "center", yscrollcommand = self.main_menu.trade_scrollbar.set)
        self.main_menu.trade_quantity.place(x = 160, y = 30, width = 50, height = 265)
        self.main_menu.trade_sellprice = Listbox(self.main_root, font = self.interface_font2, justify = "center", yscrollcommand = self.main_menu.trade_scrollbar.set)
        self.main_menu.trade_sellprice.place(x = 210, y = 30, width = 50, height = 265)
        self.main_menu.trade_method = Listbox(self.main_root, font = self.interface_font2, justify = "center", yscrollcommand = self.main_menu.trade_scrollbar.set)
        self.main_menu.trade_method.place(x = 260, y = 30, width = 100, height = 265)
        self.main_menu.trade_buyer = Listbox(self.main_root, font = self.interface_font2, justify = "center", yscrollcommand = self.main_menu.trade_scrollbar.set)
        self.main_menu.trade_buyer.place(x = 360, y = 30, width = 100, height = 265)
        self.main_menu.trade_cost = Listbox(self.main_root, font = self.interface_font2, justify = "center", yscrollcommand = self.main_menu.trade_scrollbar.set)
        self.main_menu.trade_cost.place(x = 460, y = 30, width = 50, height = 265)
        self.main_menu.trade_profit = Listbox(self.main_root, font = self.interface_font2, justify = "center", yscrollcommand = self.main_menu.trade_scrollbar.set)
        self.main_menu.trade_profit.place(x = 510, y = 30, width = 50, height = 265)
        self.main_menu.trade_date = Listbox(self.main_root, font = self.interface_font2, justify = "center", yscrollcommand = self.main_menu.trade_scrollbar.set)
        self.main_menu.trade_date.place(x = 560, y = 30, width = 130, height = 265)
        Interface.update_trades_table(self)
        self.main_menu.profit_last7days = Label(self.main_root, text = "", font = self.interface_font1)
        self.main_menu.profit_last7days.place(x = 715, y = 30)
        self.main_menu.profit_last14days = Label(self.main_root, text = "", font = self.interface_font1)
        self.main_menu.profit_last14days.place(x = 715, y = 50)
        self.main_menu.profit_last21days = Label(self.main_root, text = "", font = self.interface_font1)
        self.main_menu.profit_last21days.place(x = 715, y = 70)
        self.main_menu.profit_last28days = Label(self.main_root, text = "", font = self.interface_font1)
        self.main_menu.profit_last28days.place(x = 715, y = 90)
        Interface.update_profit(self)
        self.main_menu.sleeping_time = Label(self.main_root, text = "sleeping time: ...", font = self.interface_font1)
        self.main_menu.sleeping_time.place(x = 715, y = 575)
        threading.Thread(target = Interface.main_loop, args = (self,), daemon = False).start()
        self.main_root.mainloop()

    def on_scroll_products(self, *args):
        self.main_menu.products_names.yview(*args)
        self.main_menu.products_buyprice.yview(*args)
        self.main_menu.products_stock.yview(*args)

    def on_scroll_trades(self, *args):
        self.main_menu.trade_names.yview(*args)
        self.main_menu.trade_quantity.yview(*args)
        self.main_menu.trade_sellprice.yview(*args)
        self.main_menu.trade_method.yview(*args)
        self.main_menu.trade_buyer.yview(*args)
        self.main_menu.trade_cost.yview(*args)
        self.main_menu.trade_profit.yview(*args)
        self.main_menu.trade_date.yview(*args)

    def update_product_table(self) -> None:
        Interface.reset_product_table(self)
        avaible_products = []
        for product_name in Vars.products.keys():
            if Vars.products[product_name]['stock'] > 0:
                self.main_menu.products_names.insert(0, product_name)
                self.main_menu.products_buyprice.insert(0, Vars.products[product_name]['buy_price'])
                self.main_menu.products_stock.insert(0, Vars.products[product_name]['stock'])
                avaible_products.append(product_name)
        self.main_menu.trade_input1['menu'].delete(0, 'end')
        self.main_menu.trade_input1_variable.set("selecione")
        for i in avaible_products:
            self.main_menu.trade_input1['menu'].add_command(label = i, command = tkinter_set_it(self.main_menu.trade_input1_variable, i))
        Interface.update_products()

    def reset_product_table(self) -> None:
        self.main_menu.products_names.delete(0, END)
        self.main_menu.products_buyprice.delete(0, END)
        self.main_menu.products_stock.delete(0, END)

    def update_trades_table(self) -> None:
        Interface.reset_trades_table(self)
        for i in Vars.trades:
            self.main_menu.trade_names.insert(0, i['product'])
            self.main_menu.trade_quantity.insert(0, i['quantity'])
            self.main_menu.trade_sellprice.insert(0, i['sell_price'])
            self.main_menu.trade_method.insert(0, i['payment_method'])
            self.main_menu.trade_buyer.insert(0, i['buyer_name'])
            self.main_menu.trade_cost.insert(0, i['total_cost'])
            self.main_menu.trade_profit.insert(0, i['profit'])
            self.main_menu.trade_date.insert(0, i['transaction_date'])
        Interface.update_trades()

    def reset_trades_table(self) -> None:
        self.main_menu.trade_names.delete(0, END)
        self.main_menu.trade_quantity.delete(0, END)
        self.main_menu.trade_sellprice.delete(0, END)
        self.main_menu.trade_method.delete(0, END)
        self.main_menu.trade_buyer.delete(0, END)
        self.main_menu.trade_cost.delete(0, END)
        self.main_menu.trade_profit.delete(0, END)
        self.main_menu.trade_date.delete(0, END)

    def remove_last_trade(self) -> None:
        Vars.trades.pop()
        Interface.update_trades_table(self)

    def trade_button(self) -> None:
        Vars.sleeping_time = 0
        try:
            product_name = self.main_menu.trade_input1_variable.get().lower()
            quantity = float(self.main_menu.trade_input2.get())
            sell_price = float(self.main_menu.trade_input3.get())
            payment_method = self.main_menu.trade_input4_variable.get().lower()
            buyer_name = self.main_menu.trade_input5.get().lower()
            total_cost = float(self.main_menu.trade_output6['text'])
            profit = float(self.main_menu.trade_output7['text'])
            if self.main_menu.trade_input8.get() == "":
                transaction_date = time.strftime("%d/%b/%y")
            else:
                transaction_date = self.main_menu.trade_input8.get().lower()
                trade_year = transaction_date.split("/")[2]
                trade_day = transaction_date.split("/")[0]
                year_verification = int(trade_year)
                day_verification = int(trade_day)
                if len(transaction_date.split("/")) != 3 or len(trade_year) == 1 or len(trade_year) == 3 or len(trade_day) > 2:
                    raise Exception("BAD_DATE")
            if quantity <= Vars.products[product_name]['stock']:
                Vars.trades.append({'product':product_name, 'quantity':quantity, 'sell_price':sell_price, 'payment_method':payment_method, 'buyer_name':buyer_name, 'total_cost':total_cost, 'profit':profit, 'transaction_date':transaction_date})
                self.main_menu.trade_names.insert(0, product_name)
                self.main_menu.trade_quantity.insert(0, quantity)
                self.main_menu.trade_sellprice.insert(0, sell_price)
                self.main_menu.trade_method.insert(0, payment_method)
                self.main_menu.trade_buyer.insert(0, buyer_name)
                self.main_menu.trade_cost.insert(0, total_cost)
                self.main_menu.trade_profit.insert(0, profit)
                self.main_menu.trade_date.insert(0, transaction_date)
                Interface.update_trades()
                Vars.products[product_name]['stock'] -= quantity
                Interface.update_product_table(self)
            else:
                raise Exception("NO_STOCK")
            Interface.update_profit(self)
        except Exception as e:
            if "could not convert string to float" in str(e):
                self.main_menu.trade_error['text'] = "SOME FLOAT ENTRY CANNOT\n BE CONVERTED TO FLOAT"
            elif "list index out of range" in str(e) or str(e) == "BAD_DATE":
                self.main_menu.trade_error['text'] = "WRONG DATE"
            elif str(e) == "NO_STOCK":
                self.main_menu.trade_error['text'] = "INSSUFICIENT STOCK FOR THIS PRODUCT"
            else:
                print(str(e))

    def product_button(self) -> None:
        Vars.sleeping_time = 0
        try:
            product_name = self.main_menu.newproduct_input1.get().lower()
            buy_price = float(self.main_menu.newproduct_input2.get())
            stock = float(self.main_menu.newproduct_input3.get())
            Vars.products[product_name] = {'buy_price':buy_price, 'stock':stock}
            Interface.update_product_table(self)
        except:
            pass

    def update_products() -> None:
        with open("products.txt", "w") as f:
            pass
        with open("products.txt", "a") as f:
            for product in Vars.products.keys():
                if "encrypted_line" not in Vars.products[product].keys():
                    message = f"{product},{Vars.products[product]['buy_price']},{Vars.products[product]['stock']}"
                    encrypted_message = Encryption.password_encrypt(message, Vars.encryption_key)
                    Vars.products[product]['encrypted_line'] = encrypted_message
                    f.write(f"{encrypted_message}\n")
                else:
                    f.write(f"{Vars.products[product]['encrypted_line']}\n")

    def update_trades() -> None:
        with open("trades.txt", "w") as f:
            pass
        with open("trades.txt", "a") as f:
            for index, trade in enumerate(Vars.trades):
                if "encrypted_line" not in trade.keys():
                    message = ""
                    for key in trade.keys():
                        if key != "encrypted_line":
                            message = f"{message}{trade[key]},"
                    message = message[0:len(message)-1]
                    encrypted_message = Encryption.password_encrypt(message, Vars.encryption_key)
                    Vars.trades[index]['encrypted_line'] = encrypted_message
                    f.write(f"{encrypted_message}\n")
                    print(f"{encrypted_message}\n")
                else:
                    f.write(f"{trade['encrypted_line']}\n")
                    print(f"{trade['encrypted_line']}\n")