from scripts.variables import Vars
from scripts.encryption import Encryption
from tkinter import *
from tkinter import _setit as tkinter_set_it
import threading
import time

class Interface:

    def __init__(self) -> None:
        self.main_root = Tk()
        self.main_menu = Menu(self.main_root)

    def main_loop(self) -> None:
        while True:
            self.main_menu.trade_time.set(time.strftime("%b/%d/%y %H:%M:%S"))
            try:
                quantity = float(self.main_menu.trade_input2.get())
                sell_price = float(self.main_menu.trade_input3.get())
                total_cost = round(quantity*sell_price, 2)
                self.main_menu.trade_totalcost.set(str(total_cost))
                product_cost = Vars.products[self.main_menu.trade_input1_variable.get()]['buy_price']
                profit = round(total_cost-(product_cost*quantity), 2)
                self.main_menu.trade_profit.set(str(profit))
            except Exception as e:
                print(f"cant: {str(e)}")
            time.sleep(0.1)

    def create_window(self) -> None:
        self.main_root.resizable(False, False)
        self.main_root.geometry("700x530")
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
        self.main_menu.trade_input1 = OptionMenu(self.main_root, self.main_menu.trade_input1_variable, *list(Vars.products.keys()))
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
        self.main_menu.trade_totalcost = StringVar()
        self.main_menu.trade_totalcost.set("...")
        self.main_menu.trade_output6 = Label(self.main_root, textvariable = self.main_menu.trade_totalcost, font = self.interface_font1, justify = "center")
        self.main_menu.trade_output6.place(x = 220, y = 425, width = 150)
        self.main_menu.trade_summary7 = Label(self.main_root, text = "LUCRO", font = self.interface_font1)
        self.main_menu.trade_summary7.place(x = 10, y = 450)
        self.main_menu.trade_profit = StringVar()
        self.main_menu.trade_profit.set("...")
        self.main_menu.trade_output7 = Label(self.main_root, textvariable = self.main_menu.trade_profit, font = self.interface_font1, justify = "center")
        self.main_menu.trade_output7.place(x = 220, y = 450, width = 150)
        self.main_menu.trade_summary8 = Label(self.main_root, text = "DATA", font = self.interface_font1)
        self.main_menu.trade_summary8.place(x = 10, y = 475)
        self.main_menu.trade_time = StringVar()
        self.main_menu.trade_time.set("...")
        self.main_menu.trade_output8 = Label(self.main_root, textvariable = self.main_menu.trade_time, font = self.interface_font1, justify = "center")
        self.main_menu.trade_output8.place(x = 220, y = 475, width = 150)
        self.main_menu.trade_finish = Button(self.main_root, text = "FINALIZAR TRANSAÇÃO", font = self.interface_font3, command = lambda *args : Interface.trade_button(self))
        self.main_menu.trade_finish.place(x = 10, y = 495, width = 360, height = 25)
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
        self.main_menu.products_names = Listbox(self.main_root, font = self.interface_font2)
        self.main_menu.products_names.place(x = 380, y = 400, width = 222, height = 120)
        self.main_menu.products_buyprice = Listbox(self.main_root, font = self.interface_font2, justify = "center")
        self.main_menu.products_buyprice.place(x = 600, y = 400, width = 42, height = 120)
        self.main_menu.products_stock = Listbox(self.main_root, font = self.interface_font2, justify = "center")
        self.main_menu.products_stock.place(x = 640, y = 400, width = 50, height = 120)
        Interface.update_product_table(self)
        #db trades interface
        #produto,quantidade,preço venda,método,comprador,custo total,lucro,data
        self.main_menu.trade_summary1 = Label(self.main_root, text = "PREÇO DE CUSTO", font = self.interface_font1)
        self.main_menu.trade_summary1.place()
        self.main_menu.trade_names = Listbox(self.main_root, font = self.interface_font2, bg = "black", fg  = "white")
        self.main_menu.trade_names.place(x = 10, y = 10, width = 150, height = 280)
        self.main_menu.trade_names.insert(999, "teste")

        self.main_menu.trade_names = Listbox(self.main_root, font = self.interface_font2, bg = "black", fg  = "white")
        self.main_menu.trade_names.place(x = 10, y = 10, width = 150, height = 280)
        self.main_menu.trade_names.insert(999, "teste")

        self.main_menu.trade_names = Listbox(self.main_root, font = self.interface_font2, bg = "black", fg  = "white")
        self.main_menu.trade_names.place(x = 10, y = 10, width = 150, height = 280)
        self.main_menu.trade_names.insert(999, "teste")

        self.main_menu.trade_names = Listbox(self.main_root, font = self.interface_font2, bg = "black", fg  = "white")
        self.main_menu.trade_names.place(x = 10, y = 10, width = 150, height = 280)
        self.main_menu.trade_names.insert(999, "teste")
        # threading.Thread(target = Interface.main_loop, args = (self,), daemon = False).start()
        self.main_root.mainloop()

    def update_product_table(self) -> None:
        #atualiza tabela de produtos
        Interface.reset_product_table(self)
        avaible_products = []
        for product_name in Vars.products.keys():
            if Vars.products[product_name]['stock'] >= 0:
                self.main_menu.products_names.insert(999, product_name)
                self.main_menu.products_buyprice.insert(999, Vars.products[product_name]['buy_price'])
                self.main_menu.products_stock.insert(999, Vars.products[product_name]['stock'])
                avaible_products.append(product_name)
        #atualizar optionmenu dos produtos
        self.main_menu.trade_input1['menu'].delete(0, 'end')
        self.main_menu.trade_input1_variable.set("selecione")
        for i in avaible_products:
            self.main_menu.trade_input1['menu'].add_command(label = i, command = tkinter_set_it(self.main_menu.trade_input1_variable, i))

    def reset_product_table(self):
        self.main_menu.products_names.delete(0, END)
        self.main_menu.products_buyprice.delete(0, END)
        self.main_menu.products_stock.delete(0, END)

    def trade_button(self) -> None:
        product = self.main_menu.trade_input1_variable.get()
        quantity = float(self.main_menu.trade_input2.get())
        sell_price = float(self.main_menu.trade_input3.get())
        payment_method = self.main_menu.trade_input4_variable.get()
        buyer_name = self.main_menu.trade_input5.get()
        total_cost = float(self.main_menu.trade_output6['text'])
        profit = float(self.main_menu.trade_output7['text'])
        transaction_date = self.main_menu.trade_output8['text']
        Vars.trades.append({'product':product, 'quantity':quantity, 'sell_price':sell_price, 'payment_method':payment_method, 'buyer_name':buyer_name, 'total_cost':total_cost, 'profit':profit, 'transaction_date':transaction_date})

    def product_button(self) -> None:
        try:
            product_name = self.main_menu.newproduct_input1.get()
            buy_price = float(self.main_menu.newproduct_input2.get())
            stock = float(self.main_menu.newproduct_input3.get())
            Vars.products[product_name] = {'buy_price':buy_price, 'stock':stock}
            Interface.update_product_table(self)
        except:
            pass





    def update_products() -> None:
        with open("products.txt", "w+") as f:
            for product in Vars.products.keys():
                message = f"{product},{Vars.products[product]['buy_price']},{Vars.products[product]['stock']}"
                encrypted_message = Encryption.password_encrypt(message, Vars.encryption_key)
                f.write(f"\n{encrypted_message.decode()}")

    def update_trades() -> None:
        with open("products.txt", "w+") as f:
            for trade in Vars.trades:
                message = ""
                for key in trade.keys():
                    message = f"{message}{trade[key]},"
                message = f"{message}\n"
                encrypted_message = Encryption.password_encrypt(message, Vars.encryption_key)
                f.write(f"\n{encrypted_message.decode()}")