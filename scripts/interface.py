from scripts.variables import Vars
from scripts.encryption import Encryption
import tkinter as tk
from tkinter import _setit as tkinter_set_it
from matplotlib import pyplot as plt
from PIL import Image
import numpy
import threading
import time
import os
import datetime

class Interface:

    def __init__(self) -> None:
        self.main_root = tk.Tk()
        self.main_menu = tk.Menu(self.main_root)

    def verify_date(transaction_date: str) -> None:
        transaction_date = transaction_date.lower()
        trade_year = transaction_date.split("/")[2]
        trade_day = transaction_date.split("/")[0]
        int(trade_year) #year_verification
        int(trade_day) #day_verification
        if len(transaction_date.split("/")) != 3 or len(trade_year) == 1 or len(trade_year) == 3 or len(trade_day) > 2:
            raise Exception("BAD_DATE")

    def get_date_timestamp(trade_date: str) -> float:
        trade_date = trade_date.lower()
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
        return trade_timestamp

    #return profit from all trades since 'max_days'
    def profit_last_days(max_days: int) -> float:
        profit = 0
        atual_timestamp = time.time()
        for i in Vars.trades:
            trade_date = i['transaction_date'].split(" ")[0].lower()
            trade_timestamp = Interface.get_date_timestamp(trade_date)
            if (atual_timestamp - trade_timestamp)/86400 <= max_days:
                profit += i['profit']
        return round(profit, 2)

    #return specific product info since 'date'
    def get_product_info(product_name: str, from_date: str) -> dict:
        profit = 0
        sold_quantity = 0
        sold_buyers = 0
        min_valid_timestamp = Interface.get_date_timestamp(from_date)
        for trade in Vars.trades:
            if product_name in trade['product'] and Interface.get_date_timestamp(trade['transaction_date']) >= min_valid_timestamp:
                profit += trade['profit']
                sold_quantity += trade['quantity']
                sold_buyers += 1
        return {'profit':round(profit, 2), 'sold_quantity':round(sold_quantity, 2), 'sold_buyers':sold_buyers}

    def get_trades_profit_insights() -> dict:
        profits = {}
        for trade in Vars.trades:
            if trade['profit'] > 0:
                if trade['product'] not in profits.keys():
                    profits[trade['product']] = trade['profit']
                else:
                    profits[trade['product']] += trade['profit']
        for i in profits.keys():
            profits[i] = round(profits[i], 2)
        return profits

    def get_trades_qtd_insights() -> dict:
        quantitys = {}
        for trade in Vars.trades:
            if trade['profit'] > 0:
                if f"{trade['product']}, qtd:{trade['quantity']}" not in quantitys.keys():
                    quantitys[f"{trade['product']}, qtd:{trade['quantity']}"] = 1
                else:
                    quantitys[f"{trade['product']}, qtd:{trade['quantity']}"] += 1
        valid_quantitys = {}
        for product in quantitys.keys():
            if quantitys[product] >= Vars.min_insight_valid_qtd_qtd:
                valid_quantitys[product] = quantitys[product]
        return valid_quantitys

    #rename all product name from all trade with str 'from_names' inside trade product name for to_name (adm only)
    def rename_trades_product_name(self, from_names: list, to_name: str) -> None:
        trades_copy = Vars.trades.copy()
        for index, trade in enumerate(trades_copy):
            if trade['product'] in from_names:
                Vars.trades[index]['product'] = to_name
        Interface.update_trades_table(self)
        Interface.full_update_trades()

    #thread main loop para verificações
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
                Interface.exit()

    #update interface profit info
    def update_profit(self) -> None:
        self.main_menu.profit_last24hours['text'] = f"lucro últimas 24 horas: {Interface.profit_last_days(1)}"
        self.main_menu.profit_last7days['text'] = f"lucro últimos 7 dias: {Interface.profit_last_days(7)}"
        self.main_menu.profit_last14days['text'] = f"lucro últimos 14 dias: {Interface.profit_last_days(14)}"
        self.main_menu.profit_last30days['text'] = f"lucro últimos 30 dias: {Interface.profit_last_days(30)}"
        self.main_menu.profit_last60days['text'] = f"lucro últimos 60 dias: {Interface.profit_last_days(60)}"

    def create_window(self) -> None:
        self.main_root.resizable(False, False)
        self.main_root.geometry("960x600")
        self.main_root.config(menu = self.main_menu)
        # self.main_root.iconbitmap(r"images/icon.ico")
        self.main_root.title("SECRET MERCHANT SYSTEM")
        self.interface_font1 = ("Arial", "9")
        self.interface_font2 = ("Arial", "10", "bold")
        #new/remove trade
        self.main_menu.trade_summary1 = tk.Label(self.main_root, text = "PRODUTO", font = self.interface_font1)
        self.main_menu.trade_summary1.place(x = 10, y = 303)
        self.main_menu.trade_input1_variable = tk.StringVar(self.main_root)
        self.main_menu.trade_input1_variable.set("selecione")
        product_options = list(Vars.products.keys())
        if product_options == []:
            product_options.append("selecione")
        self.main_menu.trade_input1 = tk.OptionMenu(self.main_root, self.main_menu.trade_input1_variable, *product_options)
        self.main_menu.trade_input1.place(x = 220, y = 300, width = 150, height = 25)
        self.main_menu.trade_input1.config(indicatoron = False)
        self.main_menu.trade_summary2 = tk.Label(self.main_root, text = "QUANTIDADE", font = self.interface_font1)
        self.main_menu.trade_summary2.place(x = 10, y = 328)
        self.main_menu.trade_input2 = tk.Entry(self.main_root, font = self.interface_font1, justify = "center")
        self.main_menu.trade_input2.place(x = 220, y = 325, width = 150, height = 25)
        self.main_menu.trade_summary3 = tk.Label(self.main_root, text = "PREÇO DE VENDA", font = self.interface_font1)
        self.main_menu.trade_summary3.place(x = 10, y = 353)
        self.main_menu.trade_input3 = tk.Entry(self.main_root, font = self.interface_font1, justify = "center")
        self.main_menu.trade_input3.place(x = 220, y = 350, width = 150, height = 25)
        self.main_menu.trade_summary4 = tk.Label(self.main_root, text = "MÉTODO DE PAGAMENTO", font = self.interface_font1)
        self.main_menu.trade_summary4.place(x = 10, y = 378)
        self.main_menu.trade_input4_variable = tk.StringVar(self.main_root)
        self.main_menu.trade_input4_variable.set("selecione")
        self.main_menu.trade_input4 = tk.OptionMenu(self.main_root, self.main_menu.trade_input4_variable, *Vars.payment_methods)
        self.main_menu.trade_input4.place(x = 220, y = 375, width = 150, height = 25)
        self.main_menu.trade_input4.config(indicatoron = False)
        self.main_menu.trade_summary5 = tk.Label(self.main_root, text = "NOME DO COMPRADOR", font = self.interface_font1)
        self.main_menu.trade_summary5.place(x = 10, y = 403)
        self.main_menu.trade_input5 = tk.Entry(self.main_root, font = self.interface_font1, justify = "center")
        self.main_menu.trade_input5.place(x = 220, y = 400, width = 150, height = 25)
        self.main_menu.trade_summary6 = tk.Label(self.main_root, text = "CUSTO TOTAL", font = self.interface_font1)
        self.main_menu.trade_summary6.place(x = 10, y = 428)
        self.main_menu.trade_totalcost_variable = tk.StringVar()
        self.main_menu.trade_totalcost_variable.set("...")
        self.main_menu.trade_output6 = tk.Label(self.main_root, textvariable = self.main_menu.trade_totalcost_variable, font = self.interface_font1, justify = "center")
        self.main_menu.trade_output6.place(x = 220, y = 425, width = 150)
        self.main_menu.trade_summary7 = tk.Label(self.main_root, text = "LUCRO", font = self.interface_font1)
        self.main_menu.trade_summary7.place(x = 10, y = 453)
        self.main_menu.trade_profit_variable = tk.StringVar()
        self.main_menu.trade_profit_variable.set("...")
        self.main_menu.trade_output7 = tk.Label(self.main_root, textvariable = self.main_menu.trade_profit_variable, font = self.interface_font1, justify = "center")
        self.main_menu.trade_output7.place(x = 220, y = 450, width = 150)
        self.main_menu.trade_summary8 = tk.Label(self.main_root, text = "DATA (DIA/MÊS/ANO)", font = self.interface_font1)
        self.main_menu.trade_summary8.place(x = 10, y = 478)
        self.main_menu.trade_input8 = tk.Entry(self.main_root, text = "", font = self.interface_font1, justify = "center")
        self.main_menu.trade_input8.place(x = 220, y = 475, width = 150, height = 25)
        self.main_menu.trade_load = tk.Button(self.main_root, text = "CARREGAR TRANSAÇÃO COM INDEX", font = self.interface_font2, command = lambda *args : Interface.load_trade_info(self))
        self.main_menu.trade_load.place(x = 10, y = 510, width = 300, height = 25)
        self.main_menu.trade_load_index = tk.Entry(self.main_root, text = "", font = self.interface_font1, justify = "center")
        self.main_menu.trade_load_index.place(x = 320, y = 510, width = 50, height = 25)
        self.main_menu.trade_finish = tk.Button(self.main_root, text = "ADD/UPD TRANSAÇÃO COM INDEX", font = self.interface_font2, command = lambda *args : Interface.trade_button(self))
        self.main_menu.trade_finish.place(x = 10, y = 540, width = 300, height = 25)
        self.main_menu.trade_finish_index = tk.Entry(self.main_root, text = "", font = self.interface_font1, justify = "center")
        self.main_menu.trade_finish_index.place(x = 320, y = 540, width = 50, height = 25)
        self.main_menu.trade_remove = tk.Button(self.main_root, text = "REMOVER TRANSAÇÃO COM INDEX", font = self.interface_font2, command = lambda *args : Interface.remove_a_trade(self))
        self.main_menu.trade_remove.place(x = 10, y = 570, width = 300, height = 25)
        self.main_menu.trade_remove_index = tk.Entry(self.main_root, text = "", font = self.interface_font1, justify = "center")
        self.main_menu.trade_remove_index.place(x = 320, y = 570, width = 50, height = 25)
        #trade interface
        self.main_menu.trade_scrollbar = tk.Scrollbar(orient = "vertical", command = self.on_scroll_trades)
        self.main_menu.trade_scrollbar.place(x = 695, y = 10, width = 15, height = 285)
        self.main_menu.trade_summary1 = tk.Label(self.main_root, text = "PRODUTO", font = self.interface_font1, justify = "center")
        self.main_menu.trade_summary1.place(x = 10, y = 10, width = 150)
        self.main_menu.trade_summary2 = tk.Label(self.main_root, text = "QTD", font = self.interface_font1, justify = "center")
        self.main_menu.trade_summary2.place(x = 160, y = 10, width = 50)
        self.main_menu.trade_summary3 = tk.Label(self.main_root, text = "VENDA", font = self.interface_font1, justify = "center")
        self.main_menu.trade_summary3.place(x = 210, y = 10, width = 50)
        self.main_menu.trade_summary4 = tk.Label(self.main_root, text = "MÉTODO", font = self.interface_font1, justify = "center")
        self.main_menu.trade_summary4.place(x = 260, y = 10, width = 100)
        self.main_menu.trade_summary5 = tk.Label(self.main_root, text = "COMPRADOR", font = self.interface_font1, justify = "center")
        self.main_menu.trade_summary5.place(x = 360, y = 10, width = 150)
        self.main_menu.trade_summary6 = tk.Label(self.main_root, text = "CUSTO", font = self.interface_font1, justify = "center")
        self.main_menu.trade_summary6.place(x = 510, y = 10, width = 50)
        self.main_menu.trade_summary7 = tk.Label(self.main_root, text = "LUCRO", font = self.interface_font1, justify = "center")
        self.main_menu.trade_summary7.place(x = 560, y = 10, width = 50)
        self.main_menu.trade_summary8 = tk.Label(self.main_root, text = "DATA", font = self.interface_font1, justify = "center")
        self.main_menu.trade_summary8.place(x = 610, y = 10, width = 80)
        self.main_menu.trade_names = tk.Listbox(self.main_root, font = self.interface_font1, justify = "center", yscrollcommand = self.main_menu.trade_scrollbar.set)
        self.main_menu.trade_names.place(x = 10, y = 30, width = 150, height = 265)
        self.main_menu.trade_quantity = tk.Listbox(self.main_root, font = self.interface_font1, justify = "center", yscrollcommand = self.main_menu.trade_scrollbar.set)
        self.main_menu.trade_quantity.place(x = 160, y = 30, width = 50, height = 265)
        self.main_menu.trade_sellprice = tk.Listbox(self.main_root, font = self.interface_font1, justify = "center", yscrollcommand = self.main_menu.trade_scrollbar.set)
        self.main_menu.trade_sellprice.place(x = 210, y = 30, width = 50, height = 265)
        self.main_menu.trade_method = tk.Listbox(self.main_root, font = self.interface_font1, justify = "center", yscrollcommand = self.main_menu.trade_scrollbar.set)
        self.main_menu.trade_method.place(x = 260, y = 30, width = 100, height = 265)
        self.main_menu.trade_buyer = tk.Listbox(self.main_root, font = self.interface_font1, justify = "center", yscrollcommand = self.main_menu.trade_scrollbar.set)
        self.main_menu.trade_buyer.place(x = 360, y = 30, width = 150, height = 265)
        self.main_menu.trade_cost = tk.Listbox(self.main_root, font = self.interface_font1, justify = "center", yscrollcommand = self.main_menu.trade_scrollbar.set)
        self.main_menu.trade_cost.place(x = 510, y = 30, width = 50, height = 265)
        self.main_menu.trade_profit = tk.Listbox(self.main_root, font = self.interface_font1, justify = "center", yscrollcommand = self.main_menu.trade_scrollbar.set)
        self.main_menu.trade_profit.place(x = 560, y = 30, width = 50, height = 265)
        self.main_menu.trade_date = tk.Listbox(self.main_root, font = self.interface_font1, justify = "center", yscrollcommand = self.main_menu.trade_scrollbar.set)
        self.main_menu.trade_date.place(x = 610, y = 30, width = 80, height = 265)
        Interface.update_trades_table(self)
        #new/update/remove product
        self.main_menu.newproduct_summary1 = tk.Label(self.main_root, text = "NOME", font = self.interface_font1)
        self.main_menu.newproduct_summary1.place(x = 380, y = 303)
        self.main_menu.newproduct_input1 = tk.Entry(self.main_root, font = self.interface_font1, justify = "center")
        self.main_menu.newproduct_input1.place(x = 540, y = 300, width = 150, height = 25)
        self.main_menu.newproduct_summary2 = tk.Label(self.main_root, text = "PREÇO DE CUSTO", font = self.interface_font1)
        self.main_menu.newproduct_summary2.place(x = 380, y = 328)
        self.main_menu.newproduct_input2 = tk.Entry(self.main_root, font = self.interface_font1, justify = "center")
        self.main_menu.newproduct_input2.place(x = 540, y = 325, width = 150, height = 25)
        self.main_menu.newproduct_summary3 = tk.Label(self.main_root, text = "STOCK (TIP: USE  ' ± ' )", font = self.interface_font1)
        self.main_menu.newproduct_summary3.place(x = 380, y = 353)
        self.main_menu.newproduct_input3 = tk.Entry(self.main_root, font = self.interface_font1, justify = "center")
        self.main_menu.newproduct_input3.place(x = 540, y = 350, width = 150, height = 25)
        self.main_menu.newproduct_finish = tk.Button(self.main_root, text = "ADD/UPD PRODUTO", font = self.interface_font2, command = lambda *args : Interface.product_button(self))
        self.main_menu.newproduct_finish.place(x = 380, y = 380, width = 310, height = 25)
        self.main_menu.product_remove = tk.Button(self.main_root, text = "REMOVER PRODUTO POR NOME", font = self.interface_font2, command = lambda *args : Interface.remove_product(self))
        self.main_menu.product_remove.place(x = 380, y = 410, width = 310, height = 25)
        #product interface
        self.main_menu.products_summary1 = tk.Label(self.main_root, text = "NOME", font = self.interface_font1, justify = "center")
        self.main_menu.products_summary1.place(x = 380, y = 435, width = 210)
        self.main_menu.products_summary2 = tk.Label(self.main_root, text = "CUSTO", font = self.interface_font1, justify = "center")
        self.main_menu.products_summary2.place(x = 590, y = 435, width = 50)
        self.main_menu.products_summary3 = tk.Label(self.main_root, text = "STOCK", font = self.interface_font1, justify = "center")
        self.main_menu.products_summary3.place(x = 640, y = 435, width = 50)
        self.main_menu.products_scrollbar = tk.Scrollbar(orient = "vertical", command = self.on_scroll_products)
        self.main_menu.products_scrollbar.place(x = 695, y = 300, width = 15, height = 293)
        self.main_menu.products_names = tk.Listbox(self.main_root, font = self.interface_font1, justify = "center", yscrollcommand = self.main_menu.products_scrollbar.set)
        self.main_menu.products_names.place(x = 380, y = 450, width = 210, height = 145)
        self.main_menu.products_buyprice = tk.Listbox(self.main_root, font = self.interface_font1, justify = "center", yscrollcommand = self.main_menu.products_scrollbar.set)
        self.main_menu.products_buyprice.place(x = 590, y = 450, width = 50, height = 145)
        self.main_menu.products_stock = tk.Listbox(self.main_root, font = self.interface_font1, justify = "center", yscrollcommand = self.main_menu.products_scrollbar.set)
        self.main_menu.products_stock.place(x = 640, y = 450, width = 50, height = 145)
        Interface.update_product_table(self)
        #insights and sleeping time
        self.main_menu.sleeping_time = tk.Label(self.main_root, text = "sleeping time: ...", font = self.interface_font1)
        self.main_menu.sleeping_time.place(x = 715, y = 30)
        self.main_menu.profit_last24hours = tk.Label(self.main_root, text = "", font = self.interface_font1)
        self.main_menu.profit_last24hours.place(x = 715, y = 50)
        self.main_menu.profit_last7days = tk.Label(self.main_root, text = "", font = self.interface_font1)
        self.main_menu.profit_last7days.place(x = 715, y = 70)
        self.main_menu.profit_last14days = tk.Label(self.main_root, text = "", font = self.interface_font1)
        self.main_menu.profit_last14days.place(x = 715, y = 90)
        self.main_menu.profit_last30days = tk.Label(self.main_root, text = "", font = self.interface_font1)
        self.main_menu.profit_last30days.place(x = 715, y = 110)
        self.main_menu.profit_last60days = tk.Label(self.main_root, text = "", font = self.interface_font1)
        self.main_menu.profit_last60days.place(x = 715, y = 130)
        self.main_menu.search_button = tk.Button(self.main_root, text = "INSIGHTS DE QUANTIDADE", font = self.interface_font2, command = lambda *args : Interface.show_temp_matplot_pie_chart(Interface.get_trades_qtd_insights(), "quantity_insights"))
        self.main_menu.search_button.place(x = 715, y = 150, width = 235, height = 25)
        self.main_menu.search_button = tk.Button(self.main_root, text = "INSIGHTS DE LUCRO", font = self.interface_font2, command = lambda *args : Interface.show_temp_matplot_pie_chart(Interface.get_trades_profit_insights(), "profit_insights"))
        self.main_menu.search_button.place(x = 715, y = 180, width = 235, height = 25)
        Interface.update_profit(self)
        #search
        self.main_menu.search_summary1 = tk.Label(self.main_root, text = "NOME", font = self.interface_font1)
        self.main_menu.search_summary1.place(x = 715, y = 218)
        self.main_menu.search_name = tk.Entry(self.main_root, font = self.interface_font1, justify = "center")
        self.main_menu.search_name.place(x = 850, y = 215, width = 100, height = 25)
        self.main_menu.search_summary2 = tk.Label(self.main_root, text = "DESDE (DIA/MÊS/ANO)", font = self.interface_font1)
        self.main_menu.search_summary2.place(x = 715, y = 248)
        self.main_menu.search_date = tk.Entry(self.main_root, font = self.interface_font1, justify = "center")
        self.main_menu.search_date.place(x = 850, y = 245, width = 100, height = 25)
        self.main_menu.search_button = tk.Button(self.main_root, text = "PESQUISAR INFO DO PRODUTO", font = self.interface_font2, command = lambda *args : Interface.search_button(self))
        self.main_menu.search_button.place(x = 715, y = 275, width = 235, height = 25)
        self.main_menu.search_result_profit = tk.Label(self.main_root, text = "LUCRO DO PRODUTO: ...", font = self.interface_font1)
        self.main_menu.search_result_profit.place(x = 715, y = 305)
        self.main_menu.search_result_totalbuyers = tk.Label(self.main_root, text = "TOTAL DE COMPRADORES: ...", font = self.interface_font1)
        self.main_menu.search_result_totalbuyers.place(x = 715, y = 325)
        self.main_menu.search_result_soldquantity = tk.Label(self.main_root, text = "TOTAL VENDIDO: ...", font = self.interface_font1)
        self.main_menu.search_result_soldquantity.place(x = 715, y = 345)
        #exit
        self.main_menu.search_button = tk.Button(self.main_root, text = "SAIR", font = self.interface_font2, command = lambda *args : Interface.exit())
        self.main_menu.search_button.place(x = 715, y = 540, width = 235, height = 50)
        self.main_root.protocol("WM_DELETE_WINDOW", lambda *args : None)
        #main_loop thread
        threading.Thread(target = Interface.main_loop, args = (self,), daemon = False).start()
        #tk loop
        self.main_root.mainloop()

    def exit():
        Interface.update_products()
        Interface.update_trades()
        os._exit(0)

    def show_temp_matplot_pie_chart(info: dict, picture_name: str) -> None:
        Vars.sleeping_time = 0
        labels = list(info.keys())
        sizes = []
        for i in info.keys():
            sizes.append(info[i])
        p, tx, autotexts = plt.pie(sizes, labels = labels, autopct = "", shadow = False)
        for i, a in enumerate(autotexts):
            a.set_text(f"{sizes[i]}")
        plt.axis("equal")
        plt.savefig(f"{picture_name}.png")
        plt.close()
        Image.open(fr"{picture_name}.png").show()
        os.remove(f"{picture_name}.png")

    #gerencia scroll da tabela de produtos
    def on_scroll_products(self, *args):
        self.main_menu.products_names.yview(*args)
        self.main_menu.products_buyprice.yview(*args)
        self.main_menu.products_stock.yview(*args)

    #gerencia scroll da tabela de transações
    def on_scroll_trades(self, *args):
        self.main_menu.trade_names.yview(*args)
        self.main_menu.trade_quantity.yview(*args)
        self.main_menu.trade_sellprice.yview(*args)
        self.main_menu.trade_method.yview(*args)
        self.main_menu.trade_buyer.yview(*args)
        self.main_menu.trade_cost.yview(*args)
        self.main_menu.trade_profit.yview(*args)
        self.main_menu.trade_date.yview(*args)

    #atualiza tabela de produtos
    def update_product_table(self) -> None:
        Interface.reset_product_table(self)
        avaible_products = []
        for product_name in Vars.products.keys():
            if Vars.products[product_name]['stock'] > 0:
                self.main_menu.products_names.insert(0, product_name)
                self.main_menu.products_buyprice.insert(0, round(Vars.products[product_name]['buy_price'], 2))
                self.main_menu.products_stock.insert(0, round(Vars.products[product_name]['stock'], 2))
                avaible_products.append(product_name)
        self.main_menu.trade_input1['menu'].delete(0, 'end')
        self.main_menu.trade_input1_variable.set("selecione")
        for i in avaible_products:
            self.main_menu.trade_input1['menu'].add_command(label = i, command = tkinter_set_it(self.main_menu.trade_input1_variable, i))

    #limpa a tabela de produtos
    def reset_product_table(self) -> None:
        self.main_menu.products_names.delete(0, tk.END)
        self.main_menu.products_buyprice.delete(0, tk.END)
        self.main_menu.products_stock.delete(0, tk.END)

    #atualiza a tabela de transações
    def update_trades_table(self) -> None:
        Interface.reset_trades_table(self)
        for index, i in enumerate(Vars.trades):
            self.main_menu.trade_names.insert(0, f"{index + 1} - {i['product']}")
            self.main_menu.trade_quantity.insert(0, i['quantity'])
            self.main_menu.trade_sellprice.insert(0, i['sell_price'])
            self.main_menu.trade_method.insert(0, i['payment_method'])
            self.main_menu.trade_buyer.insert(0, i['buyer_name'])
            self.main_menu.trade_cost.insert(0, i['total_cost'])
            self.main_menu.trade_profit.insert(0, i['profit'])
            self.main_menu.trade_date.insert(0, i['transaction_date'])

    #limpa a tabela de transações
    def reset_trades_table(self) -> None:
        self.main_menu.trade_names.delete(0, tk.END)
        self.main_menu.trade_quantity.delete(0, tk.END)
        self.main_menu.trade_sellprice.delete(0, tk.END)
        self.main_menu.trade_method.delete(0, tk.END)
        self.main_menu.trade_buyer.delete(0, tk.END)
        self.main_menu.trade_cost.delete(0, tk.END)
        self.main_menu.trade_profit.delete(0, tk.END)
        self.main_menu.trade_date.delete(0, tk.END)

    #ação do botão de remover transação
    def remove_a_trade(self) -> None:
        Vars.sleeping_time = 0
        try:
            trade_index = abs(int(self.main_menu.trade_remove_index.get())) - 1
            if (trade_index + 1) > len(Vars.trades):
                raise Exception("INVALID_INDEX")
        except:
            return
        trade_product = Vars.trades[trade_index]['product']
        trade_quantity = Vars.trades[trade_index]['quantity']
        Vars.products[trade_product]['stock'] += trade_quantity
        del Vars.trades[trade_index]
        Interface.update_trades_table(self)
        Interface.update_product_table(self)

    #ação do botão de remover produto
    def remove_product(self) -> None:
        Vars.sleeping_time = 0
        product_name = self.main_menu.newproduct_input1.get().lower()
        del Vars.products[product_name]
        del Vars.products[product_name]['encrypted_line']
        Interface.update_product_table(self)

    #ação do botão de add/upd transação
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
                transaction_date = self.main_menu.trade_input8.get()
                Interface.verify_date(transaction_date)
            if quantity <= Vars.products[product_name]['stock']:
                update_index = self.main_menu.trade_finish_index.get()
                if update_index == "":
                    new_trade = {}
                    new_trade['product'] = product_name
                    new_trade['quantity'] = quantity
                    new_trade['sell_price'] = sell_price
                    new_trade['payment_method'] = payment_method
                    new_trade['buyer_name'] = buyer_name
                    new_trade['total_cost'] = total_cost
                    new_trade['profit'] = profit
                    new_trade['transaction_date'] = transaction_date
                    Vars.trades.append(new_trade)
                else:
                    try:
                        update_index = abs(int(update_index)) - 1
                        if (update_index + 1) > len(Vars.trades):
                            raise Exception("INVALID_INDEX")
                    except:
                        return
                    updated_trade_product = Vars.trades[update_index]['product']
                    updated_trade_quantity = Vars.trades[update_index]['quantity']
                    Vars.trades[update_index]['product'] = product_name
                    Vars.trades[update_index]['quantity'] = quantity
                    Vars.trades[update_index]['sell_price'] = sell_price
                    Vars.trades[update_index]['payment_method'] = payment_method
                    Vars.trades[update_index]['buyer_name'] = buyer_name
                    Vars.trades[update_index]['total_cost'] = total_cost
                    Vars.trades[update_index]['profit'] = profit
                    Vars.trades[update_index]['transaction_date'] = transaction_date
                    del Vars.trades[update_index]['encrypted_line']
                    Vars.products[updated_trade_product]['stock'] += updated_trade_quantity
                Vars.products[product_name]['stock'] -= quantity
                Interface.update_trades_table(self)
                del Vars.products[product_name]['encrypted_line']
                Interface.update_product_table(self)
            else:
                raise Exception("NO_STOCK")
            Interface.update_profit(self)
        except:
            pass

    #carrega dados de um trade nos campos de entrada de transações
    def load_trade_info(self) -> None:
        Vars.sleeping_time = 0
        try:
            trade_index = abs(int(self.main_menu.trade_load_index.get())) - 1
            if (trade_index + 1) > len(Vars.trades):
                raise Exception("INVALID_INDEX")
        except:
            return
        self.main_menu.trade_input1_variable.set(Vars.trades[trade_index]['product'])
        self.main_menu.trade_input2.delete(0, tk.END)
        self.main_menu.trade_input2.insert(0, Vars.trades[trade_index]['quantity'])
        self.main_menu.trade_input3.delete(0, tk.END)
        self.main_menu.trade_input3.insert(0, Vars.trades[trade_index]['sell_price'])
        self.main_menu.trade_input4_variable.set(Vars.trades[trade_index]['payment_method'])
        self.main_menu.trade_input5.delete(0, tk.END)
        self.main_menu.trade_input5.insert(0, Vars.trades[trade_index]['buyer_name'])
        self.main_menu.trade_input8.delete(0, tk.END)
        self.main_menu.trade_input8.insert(0, Vars.trades[trade_index]['transaction_date'])

    #ação do botão de add/upd produto
    def product_button(self) -> None:
        Vars.sleeping_time = 0
        try:
            product_name = self.main_menu.newproduct_input1.get().lower()
            buy_price = float(self.main_menu.newproduct_input2.get())
            stock = self.main_menu.newproduct_input3.get()
            if "+" in stock:
                stock = Vars.products[product_name]['stock'] + float(stock)
                Vars.products[product_name] = {'buy_price':buy_price, 'stock':stock}
            elif "-" in stock:
                stock = Vars.products[product_name]['stock'] - abs(float(stock))
                Vars.products[product_name] = {'buy_price':buy_price, 'stock':stock}
            else:
                Vars.products[product_name] = {'buy_price':buy_price, 'stock':float(stock)}
            Interface.update_product_table(self)
        except:
            pass

    #ação do botão de pesquisa
    def search_button(self) -> None:
        Vars.sleeping_time = 0
        try:
            name = self.main_menu.search_name.get().lower()
            date = self.main_menu.search_date.get()
            Interface.verify_date(date)
            product_info = Interface.get_product_info(name, date)
            self.main_menu.search_result_profit['text'] = f"LUCRO DO PRODUTO: {product_info['profit']}"
            self.main_menu.search_result_totalbuyers['text'] = f"TOTAL DE COMPRADORES: {product_info['sold_buyers']}"
            self.main_menu.search_result_soldquantity['text'] = f"TOTAL VENDIDO: {product_info['sold_quantity']}"
        except:
            pass

    #se aproveita da criptografia pronta para salvar o arquivo
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

    #se aproveita da criptografia pronta para salvar o arquivo
    def update_trades() -> None:
        with open("trades.txt", "w") as f:
            pass
        with open("trades.txt", "a") as f:
            for trade in Vars.trades:
                if "encrypted_line" not in trade.keys():
                    message = ""
                    for key in trade.keys():
                        if key != "encrypted_line":
                            message = f"{message}{trade[key]},"
                    message = message[0:len(message)-1]
                    encrypted_message = Encryption.password_encrypt(message, Vars.encryption_key)
                    f.write(f"{encrypted_message}\n")
                else:
                    f.write(f"{trade['encrypted_line']}\n")

    #refaz a criptografia para salvar arquivo (adm_only)
    def full_update_trades() -> None:
        with open("trades.txt", "w") as f:
            pass
        with open("trades.txt", "a") as f:
            for trade in Vars.trades:
                message = ""
                for key in trade.keys():
                    if key != "encrypted_line":
                        message = f"{message}{trade[key]},"
                message = message[0:len(message)-1]
                encrypted_message = Encryption.password_encrypt(message, Vars.encryption_key)
                f.write(f"{encrypted_message}\n")