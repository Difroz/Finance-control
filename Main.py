import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb
import datetime as dt

import database as datb
import logic as lc


class InputWind(tk.Toplevel):

    def __init__(self):
        super().__init__()
        self.main()
        self.login()

    def main(self):
        self.title('Вход в программу')
        self.geometry('200x80+500+200')
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()

    def login(self):
        login_lable = tk.Label(self, text='Login:')
        pass_lable = tk.Label(self, text='Password:')
        self.login_entry = tk.Entry(self, width=20)
        self.pass_entry = tk.Entry(self, width=20)
        login_lable.grid(row=0, column=0)
        pass_lable.grid(row=1, column=0)
        self.login_entry.grid(row=0, column=1)
        self.pass_entry.grid(row=1, column=1)
        enter_bnt = tk.Button(self, text='Войти', command=self.autentification)
        enter_bnt.grid(row=2, column=0)
        create_btn = tk.Button(self, text='Создать базу данных', command=self.create_user)
        create_btn.grid(row=2, column=1)

    def autentification(self):
        global db, app, login
        login = self.login_entry.get()
        password = self.pass_entry.get()
        check = new_db.check_user(login)

        if login == 0 or password == 0:
            mb.showerror(title='Ошибка', message='Пустые поля')
        if check == None:
            mb.showerror(title='Ошибка', message='Пользователя с таким именем не существует')
            self.login_entry.delete(0, 20)
            self.pass_entry.delete(0, 20)
        else:
            mb.showinfo(title='Вход', message='Вход выполнен.')
            db = datb.DB(login)
            self.destroy()
            app = Main(root)

    def create_user(self):
        login = self.login_entry.get()
        password = self.pass_entry.get()
        check = new_db.check_user(login)
        global db
        if login == 0 or password == 0:
            mb.showerror(title='Ошибка', message='Пустые поля')
        if check is None:
            new_db.add_users(login, password)
            mb.showinfo(title='Регистрация', message='Регистрация прошла успешно. Выполните вход')
            db = datb.DB(login)
            db.create_table()

        else:
            mb.showerror(title='Ошибка', message='Пользователь с таким именем уже существует')


class Main(tk.Frame):

    def __init__(self, master):
        super().__init__(master)
        self.add_img = tk.PhotoImage(file=r'C:\PyProject\Main\Finance Asistanser\images\keeper.png')
        self.init_main()
        self.notebook = Notebook()

    def init_main(self):
        toolbar = tk.Frame(bd=2, bg='white')
        toolbar.pack(fill=tk.X, side=tk.TOP)
        bt_open_bills_wd = tk.Button(toolbar, text='Счета', command=self.open_bills_wd,
                                     bd=1, bg='white', compound=tk.TOP, image=self.add_img)
        bt_open_bills_wd.pack(side=tk.LEFT)

        bt_open_salary_wd = tk.Button(toolbar, text='Источники доходов', command=self.open_salary_wd,
                                      bd=1, bg='white', compound=tk.TOP)
        bt_open_salary_wd.pack(side=tk.LEFT)

        bt_open_must_costs_wd = tk.Button(toolbar, text='Обязательные расходы', command=self.open_must_costs_wd,
                                          bd=1, bg='white', compound=tk.TOP)
        bt_open_must_costs_wd.pack(side=tk.LEFT)

        bt_open_categories_wd = tk.Button(toolbar, text='Категории расходов', command=self.open_categories_wd,
                                          bd=1, bg='white', compound=tk.TOP)
        bt_open_categories_wd.pack(side=tk.LEFT)

        bt_open_categories_wd = tk.Button(toolbar, text='Просмотр статистики', command=self.add_analitic,
                                          bd=1, bg='white', compound=tk.TOP)
        bt_open_categories_wd.pack(side=tk.LEFT)

    def open_bills_wd(self):
        BillsWindow()

    def open_salary_wd(self):
        SalaryWindow()

    def open_must_costs_wd(self):
        MustCostsWindow()

    def open_categories_wd(self):
        CategoriesWindow()

    def add_analitic(self):
        self.notebook.add_analitic()


class BillsWindow(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.table_name = 'bills'
        self.title('Счета')
        self.geometry('280x200+500+200')
        self.grab_set()
        self.focus_set()
        self.init()
        self.create_table()
        self.show_info()

    def init(self):
        self.tools = tk.Frame(self, bd=2, bg='white')
        self.tools.pack(fill=tk.Y, side=tk.RIGHT)

        self.btn_add = tk.Button(self.tools, text='Добавить', command=self.add_wd, width=15)
        self.btn_add.grid(row=0, column=0)

        self.btn_change = tk.Button(self.tools, text='Редактировать', command=self.change_wd, width=15)
        self.btn_change.grid(row=1, column=0)

        self.btn_delete = tk.Button(self.tools, text='Удалить', command=self.delete, width=15)
        self.btn_delete.grid(row=2, column=0)

        self.sum_lable = tk.LabelFrame(self.tools, text='Общая сумма:')
        self.sum_lable.grid(row=3, column=0, ipady=10)
        self.sum_value_lable = tk.Label(self.sum_lable, text=self.sum_frame())
        self.sum_value_lable.pack()

    def create_table(self):
        self.table = ttk.Treeview(self, columns=('ID', 'name', 'sum'), height=30, show='headings')
        self.table.column('ID', width=10)
        self.table.column('name', width=50)
        self.table.column('sum', width=25)
        self.table.heading('ID', text='ID', anchor=tk.CENTER)
        self.table.heading('name', text='Название', anchor=tk.CENTER)
        self.table.heading('sum', text='Баланс', anchor=tk.CENTER)
        self.table.pack(fill=tk.BOTH)

    def add_wd(self):
        self.main = tk.Toplevel(self)
        self.main.title('Добавить счет')
        self.main.geometry('250x100+300+200')
        self.main.grab_set()
        self.main.focus_set()
        self.bill_name_lable = tk.Label(self.main, text='Имя счета')
        self.bill_name_lable.grid(row=0, column=0)
        self.bill_name_entry = tk.Entry(self.main, width=20)
        self.bill_name_entry.grid(row=0, column=1)
        self.bill_sum_lable = tk.Label(self.main, text='Сумма на счете:')
        self.bill_sum_lable.grid(row=1, column=0)
        self.bill_sum_entry = tk.Entry(self.main, width=20)
        self.bill_sum_entry.grid(row=1, column=1)
        self.values = tk.BooleanVar()
        self.bill_status = ttk.Checkbutton(self.main, text='Счет для сбережений', variable=self.values, onvalue=1,
                                           offvalue=0)
        self.bill_status.grid(row=2, column=1)
        self.btn_add_bill = tk.Button(self.main, text='Добавить')
        self.btn_add_bill.bind('<Button-1>', lambda event: self.add_bill(self.bill_name_entry.get(),
                                                                         self.bill_sum_entry.get()))
        self.btn_add_bill.grid(row=3, column=1)

    def change_wd(self):
        self.main = tk.Toplevel(self)
        self.main.title('Редактировать счет')
        self.main.geometry('250x100+300+200')
        self.main.grab_set()
        self.main.focus_set()
        self.bill_name_lable = tk.Label(self.main, text='Имя счета')
        self.bill_name_lable.grid(row=0, column=0)
        self.bill_name_entry = tk.Entry(self.main, width=20)
        self.bill_name_entry.grid(row=0, column=1)
        self.bill_sum_lable = tk.Label(self.main, text='Сумма на счете:')
        self.bill_sum_lable.grid(row=1, column=0)
        self.bill_sum_entry = tk.Entry(self.main, width=20)
        self.bill_sum_entry.grid(row=1, column=1)
        self.btn_add_bill = tk.Button(self.main, text='Редактировать', )
        self.default_values()
        self.values = tk.BooleanVar()
        self.bill_status = ttk.Checkbutton(self.main, text='Счет для сбережений', variable=self.values, onvalue=1,
                                           offvalue=0)
        self.bill_status.grid(row=2, column=1)
        self.btn_add_bill.bind('<Button-1>', lambda event: self.change_bill(self.bill_name_entry.get(),
                                                                            self.bill_sum_entry.get()))
        self.btn_add_bill.grid(row=3, column=1)

    def add_bill(self, bill_name, bill_sum):
        bill_status = int(self.values.get())
        db.add_bill(bill_name, bill_sum, bill_status)
        self.show_info()
        self.sum_value_lable['text'] = self.sum_frame()
        self.main.destroy()

    def change_bill(self, bill_name, bill_sum):
        bill_status = int(self.values.get())
        string_id = self.table.set(self.table.selection()[0], '#1')
        db.change_bill(string_id, bill_name, bill_sum, bill_status)
        self.show_info()
        self.sum_value_lable['text'] = self.sum_frame()
        self.main.destroy()

    def delete(self):
        string_id = [self.table.set(self.table.selection()[0], '#1')]
        db.delete_bill(string_id)
        self.sum_value_lable['text'] = self.sum_frame()
        self.show_info()

    def show_info(self):
        db.show_info(self.table, self.table_name)

    def show_info_bill(self):
        db.show_info_bills(self.table)

    def sum_frame(self):
        self.frame = lc.BillsFrame(login)
        return self.frame.sum_bills()

    def default_values(self):
        string_id = [self.table.set(self.table.selection()[0], '#1')]
        values = db.select_bill(string_id)
        self.bill_name_entry.insert(0, values[1])
        self.bill_sum_entry.insert(0, values[2])


class SalaryWindow(BillsWindow):
    def __init__(self):
        super().__init__()
        self.app = app
        self.title('Источники доходов')
        self.geometry('300x200+500+200')
        self.table_name = 'salary'
        self.show_info()

    def create_table(self):
        self.table = ttk.Treeview(self, columns=('ID', 'name', 'sum'), height=30, show='headings')
        self.table.column('ID', width=10)
        self.table.column('name', width=50)
        self.table.column('sum', width=25)
        self.table.heading('ID', text='ID', anchor=tk.CENTER)
        self.table.heading('name', text='Источник', anchor=tk.CENTER)
        self.table.heading('sum', text='Сумма', anchor=tk.CENTER)
        self.table.pack(fill=tk.BOTH)

    def add_wd(self):
        self.main = tk.Toplevel(self)
        self.main.title('Добавить источник дохода')
        self.main.geometry('250x100+300+200')
        self.main.grab_set()
        self.main.focus_set()
        self.bill_name_lable = tk.Label(self.main, text='Источник')
        self.bill_name_lable.grid(row=0, column=0)
        self.bill_name_entry = tk.Entry(self.main, width=20)
        self.bill_name_entry.grid(row=0, column=1)
        self.bill_sum_lable = tk.Label(self.main, text='Сумма:')
        self.bill_sum_lable.grid(row=1, column=0)
        self.bill_sum_entry = tk.Entry(self.main, width=20)
        self.bill_sum_entry.grid(row=1, column=1)
        self.btn_add_bill = tk.Button(self.main, text='Добавить', )
        self.btn_add_bill.bind('<Button-1>', lambda event: self.add_bill(self.bill_name_entry.get(),
                                                                         self.bill_sum_entry.get()))
        self.btn_add_bill.grid(row=2, column=1)

    def change_wd(self):
        self.main = tk.Toplevel(self)
        self.main.title('Редактировать')
        self.main.geometry('250x100+300+200')
        self.main.grab_set()
        self.main.focus_set()
        self.bill_name_lable = tk.Label(self.main, text='Источник')
        self.bill_name_lable.grid(row=0, column=0)
        self.bill_name_entry = tk.Entry(self.main, width=20)
        self.bill_name_entry.grid(row=0, column=1)
        self.bill_sum_lable = tk.Label(self.main, text='Сумма:')
        self.bill_sum_lable.grid(row=1, column=0)
        self.bill_sum_entry = tk.Entry(self.main, width=20)
        self.bill_sum_entry.grid(row=1, column=1)
        self.btn_add_bill = tk.Button(self.main, text='Редактировать', )
        self.default_values()
        self.btn_add_bill.bind('<Button-1>', lambda event: self.change_bill(self.bill_name_entry.get(),
                                                                            self.bill_sum_entry.get()))
        self.btn_add_bill.grid(row=2, column=1)


    def add_bill(self, costs_name, costs_sum):
        db.add_salary(costs_name, costs_sum)
        self.show_info()
        self.sum_value_lable['text'] = self.sum_frame()
        self.main.destroy()
        self.app.notebook.destroy()
        self.app.notebook = Notebook()
        self.app.notebook.select([0])

    def change_bill(self, costs_name, costs_sum):
        try:
            string_id = self.table.set(self.table.selection()[0], '#1')
            db.change_salary(string_id, costs_name, costs_sum)
        except:
            self.main.destroy()
            mb.showerror(title='Ошибка', message='Выдели строку')
        self.show_info()
        self.sum_value_lable['text'] = self.sum_frame()
        self.main.destroy()
        self.app.notebook.destroy()
        self.app.notebook = Notebook()
        self.app.notebook.select([0])

    def delete(self):
        string_id = [self.table.set(self.table.selection()[0], '#1')]
        db.delete_salary(string_id)
        self.sum_value_lable['text'] = self.sum_frame()
        self.show_info()
        self.app.notebook.destroy()
        self.app.notebook = Notebook()
        self.app.notebook.select([0])

    def sum_frame(self):
        self.frame = lc.SalaryFrame(login)
        return self.frame.sum_salary()

    def default_values(self):
        string_id = [self.table.set(self.table.selection()[0], '#1')]
        values = db.select_salary(string_id)
        self.bill_name_entry.insert(0, values[1])
        self.bill_sum_entry.insert(0, values[2])


class CategoriesWindow(BillsWindow):
    def __init__(self):
        super().__init__()
        self.title('Категории расходов')
        self.table_name = 'categories'
        self.sum_value_lable.destroy()
        self.sum_lable.destroy()
        self.show_info()

    def create_table(self):
        self.table = ttk.Treeview(self, columns=('ID', 'name'), height=15, show='headings')
        self.table.column('ID', width=10)
        self.table.column('name', width=50)
        self.table.heading('ID', text='ID', anchor=tk.CENTER)
        self.table.heading('name', text='Название', anchor=tk.CENTER)
        self.table.pack(fill=tk.BOTH)

    def add_wd(self):
        self.main = tk.Toplevel(self)
        self.main.title('Добавить категорию')
        self.name_lable = tk.Label(self.main, text='Название категории')
        self.name_lable.grid(row=0, column=0)
        self.name_entry = tk.Entry(self.main, width=20)
        self.name_entry.grid(row=0, column=1)
        self.btn_add_bill = tk.Button(self.main, text='Добавить')
        self.btn_add_bill.bind('<Button-1>', lambda event: self.add_category(self.name_entry.get()))
        self.btn_add_bill.grid(row=2, column=1)

    def add_category(self, category_name):
        db.add_category(category_name)
        self.show_info()

    def change_wd(self):
        self.main = tk.Toplevel(self)
        self.main.title('Редактировать категорию')
        self.main.geometry('250x100+300+200')
        self.main.grab_set()
        self.main.focus_set()
        self.name_lable = tk.Label(self.main, text='Название категории')
        self.name_lable.grid(row=0, column=0)
        self.name_entry = tk.Entry(self.main, width=20)
        self.name_entry.grid(row=0, column=1)
        self.btn_add_bill = tk.Button(self.main, text='Редактировать', )
        self.default_values()
        self.btn_add_bill.bind('<Button-1>', lambda event: self.change_category(self.name_entry.get()))
        self.btn_add_bill.grid(row=2, column=1)

    def change_category(self, category_name):
        string_id = self.table.set(self.table.selection()[0], '#1')
        db.change_category(string_id, category_name)
        self.show_info()

    def delete(self):
        string_id = [self.table.set(self.table.selection()[0], '#1')]
        db.delete_category(string_id)
        self.show_info()

    def default_values(self):
        string_id = [self.table.set(self.table.selection()[0], '#1')]
        values = db.select_categories(string_id)
        self.name_entry.insert(0, values)


class MustCostsWindow(BillsWindow):
    def __init__(self):
        super().__init__()
        self.app = app
        self.title('Обязательные расходы')
        self.table_name = 'must_costs'
        self.init()
        self.show_info()

    def create_table(self):
        self.table = ttk.Treeview(self, columns=('ID', 'name', 'sum'), height=30, show='headings')
        self.table.column('ID', width=10)
        self.table.column('name', width=50)
        self.table.column('sum', width=25)
        self.table.heading('ID', text='ID', anchor=tk.CENTER)
        self.table.heading('name', text='Название', anchor=tk.CENTER)
        self.table.heading('sum', text='Сумма', anchor=tk.CENTER)
        self.table.pack(fill=tk.BOTH)

    def add_wd(self):
        self.main = tk.Toplevel(self)
        self.main.title('Добавить обязательный расход')
        self.main.geometry('250x100+300+200')
        self.main.grab_set()
        self.main.focus_set()
        self.bill_name_lable = tk.Label(self.main, text='Название')
        self.bill_name_lable.grid(row=0, column=0)
        self.bill_name_entry = tk.Entry(self.main, width=20)
        self.bill_name_entry.grid(row=0, column=1)
        self.bill_sum_lable = tk.Label(self.main, text='Сумма:')
        self.bill_sum_lable.grid(row=1, column=0)
        self.bill_sum_entry = tk.Entry(self.main, width=20)
        self.bill_sum_entry.grid(row=1, column=1)
        self.btn_add_bill = tk.Button(self.main, text='Добавить', )
        self.app.notebook.destroy()
        self.app.notebook = Notebook()
        self.app.notebook.select([0])
        self.btn_add_bill.bind('<Button-1>', lambda event: self.add_bill(self.bill_name_entry.get(),
                                                                         self.bill_sum_entry.get()))
        self.btn_add_bill.grid(row=2, column=1)

    def change_wd(self):
        self.main = tk.Toplevel(self)
        self.main.title('Редактировать')
        self.main.geometry('250x100+300+200')
        self.main.grab_set()
        self.main.focus_set()
        self.bill_name_lable = tk.Label(self.main, text='Название')
        self.bill_name_lable.grid(row=0, column=0)
        self.bill_name_entry = tk.Entry(self.main, width=20)
        self.bill_name_entry.grid(row=0, column=1)
        self.bill_sum_lable = tk.Label(self.main, text='Сумма:')
        self.bill_sum_lable.grid(row=1, column=0)
        self.bill_sum_entry = tk.Entry(self.main, width=20)
        self.bill_sum_entry.grid(row=1, column=1)
        self.btn_add_bill = tk.Button(self.main, text='Редактировать', )
        self.default_values()
        self.app.notebook.destroy()
        self.app.notebook = Notebook()
        self.app.notebook.select([0])
        self.btn_add_bill.bind('<Button-1>', lambda event: self.change_bill(self.bill_name_entry.get(),
                                                                            self.bill_sum_entry.get()))
        self.btn_add_bill.grid(row=2, column=1)


    def add_bill(self, costs_name, costs_sum):
        db.add_must_costs(costs_name, costs_sum)
        self.show_info()
        self.sum_value_lable['text'] = self.sum_frame()
        self.main.destroy()
        self.app.notebook.destroy()
        self.app.notebook = Notebook()
        self.app.notebook.select([0])

    def change_bill(self, costs_name, costs_sum):
        string_id = self.table.set(self.table.selection()[0], '#1')
        db.change_must_costs(costs_name, costs_sum, string_id)
        self.show_info()
        self.sum_value_lable['text'] = self.sum_frame()
        self.main.destroy()
        self.app.notebook.destroy()
        self.app.notebook = Notebook()
        self.app.notebook.select([0])

    def delete(self):
        string_id = [self.table.set(self.table.selection()[0], '#1')]
        self.sum_value_lable['text'] = self.sum_frame()
        db.delete_must_costs(string_id)
        self.show_info()
        self.sum_frame()
        self.app.notebook.destroy()
        self.app.notebook = Notebook()
        self.app.notebook.select([0])

    def sum_frame(self):
        self.frame = lc.MustCostsFrame(login)
        return self.frame.sum_mc()

    def default_values(self):
        string_id = [self.table.set(self.table.selection()[0], '#1')]
        values = db.select_mc(string_id)
        self.bill_name_entry.insert(0, values[1])
        self.bill_sum_entry.insert(0, values[2])


class CostsTableWindow(tk.Frame, BillsWindow):
    def __init__(self):
        super().__init__()
        self.table_name = 'costs'

        self.add_img = tk.PhotoImage(file=r'C:\PyProject\Main\Finance Asistanser\images\add.png')
        self.edit_img = tk.PhotoImage(file=r'C:\PyProject\Main\Finance Asistanser\images\edit.png')
        self.delete_img = tk.PhotoImage(file=r'C:\PyProject\Main\Finance Asistanser\images\delete.png')

        self.tools = tk.Frame(self, bd=2, bg='white')

        self.btn_add = tk.Button(self.tools, bd=1, bg='white', compound=tk.TOP, command=self.open_add_window,
                                 image=self.add_img)
        self.btn_add.pack(side=tk.TOP)

        self.btn_change = tk.Button(self.tools, bd=1, bg='white', compound=tk.TOP, command=self.open_change_window,
                                    image=self.edit_img)
        self.btn_change.pack(side=tk.TOP)

        self.btn_delete = tk.Button(self.tools, bd=1, bg='white', compound=tk.TOP, command=self.delete_string,
                                    image=self.delete_img)
        self.btn_delete.pack(side=tk.TOP)

        self.tools.pack(fill=tk.Y, side=tk.RIGHT)
        self.create_tree()
        self.show_info()

    def create_tree(self):
        self.costs_tree = ttk.Treeview(self, columns=('ID',
                                           'name',
                                           'category',
                                           'date',
                                           'sum',
                                           'bill_id'),
                                  height=15, show='headings')
        self.costs_tree.column('ID', width=15, anchor=tk.CENTER)
        self.costs_tree.column('name', width=50, anchor=tk.CENTER)
        self.costs_tree.column('category', width=50, anchor=tk.CENTER)
        self.costs_tree.column('date', width=50, anchor=tk.CENTER)
        self.costs_tree.column('sum', width=20, anchor=tk.CENTER)
        self.costs_tree.column('bill_id', width=30, anchor=tk.CENTER)

        self.costs_tree.heading('ID', text='ID')
        self.costs_tree.heading('name', text='Наименование')
        self.costs_tree.heading('category', text='Категория расходов')
        self.costs_tree.heading('date', text='Дата')
        self.costs_tree.heading('sum', text='Сумма')
        self.costs_tree.heading('bill_id', text='Счет')
        self.costs_tree.pack(fill=tk.BOTH)

    def open_add_window(self):
        AddCostsWindow()

    def open_change_window(self):
        try:
            ChangeCostsWindow(self.costs_tree, self.show_info)
        except IndexError:
            return mb.showerror(title='Ошибка', message='Выдели строку для редактирования')

    def delete_string(self):
        string_id = self.costs_tree.set(self.costs_tree.selection()[0], '#1')
        values = db.select_old_sum_id_costs([string_id])
        db.bill_sum_plus(values[0], values[1])
        db.delete_costs([string_id])
        self.show_info()

    def show_info(self):
        db.get_costs_val(self.costs_tree)


class AddCostsWindow(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.app = app
        self.title('Добавить')
        self.geometry('250x150+500+200')
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()
        self.categories_dict = self.create_categories_dict()
        self.bills_dict = self.create_bills_dict()
        self.init()
        self.default_date()

    def init(self):
        name_lable = tk.Label(self, text='Наименование:')
        self.name_entry = tk.Entry(self, width=15)
        name_lable.grid(row=0, column=0)
        self.name_entry.grid(row=0, column=1)

        date_lable = tk.Label(self, text='Дата:')
        self.date_entry = tk.Entry(self, width=10)
        date_lable.grid(row=1, column=0)
        self.date_entry.grid(row=1, column=1)

        sum_lable = tk.Label(self, text='Сумма:')
        self.sum_entry = tk.Entry(self, width=10)
        sum_lable.grid(row=2, column=0)
        self.sum_entry.grid(row=2, column=1)

        category_lable = tk.Label(self, text='Категория:')
        self.category = ttk.Combobox(self, values=list(self.categories_dict.keys()))
        category_lable.grid(row=3, column=0)
        self.category.grid(row=3, column=1)

        bills_lable = tk.Label(self, text='Счет списания:')
        self.bills = ttk.Combobox(self, values=list(self.bills_dict.keys()))
        bills_lable.grid(row=4, column=0)
        self.bills.grid(row=4, column=1)

        self.btn_add_costs = tk.Button(self, text='Добавить')
        self.btn_add_costs.bind('<Button-1>', lambda event: self.add_costs(self.name_entry.get(),
                                                                          self.category.get(),
                                                                          self.date_entry.get(),
                                                                          self.sum_entry.get(),
                                                                          self.bills.get()))
        self.btn_add_costs.grid(row=5, column=1)

    def create_categories_dict(self):
        table_values = db.get_values('categories')
        categories_dict = {y:x for x, y in table_values}
        return categories_dict

    def create_bills_dict(self):
        table_values = db.get_values('bills')
        bills_dict = {y:x for x, y, z, i in table_values if i==0}
        return bills_dict

    def add_costs(self, costs_name, categories, date, costs_sum, bills):
        categories_id = self.categories_dict[categories]
        bills_id = self.bills_dict[bills]
        db.add_costs(costs_name, categories_id, date, costs_sum, bills_id)
        costs_sum_new = abs(float(costs_sum.replace(',', '.')))
        db.bill_sum_minus(costs_sum_new, bills_id)
        self.app.notebook.destroy()
        self.app.notebook = Notebook()
        self.app.notebook.select([1])

    def default_date(self):
        today = dt.datetime.today().strftime('%Y.%m.%d')
        self.date_entry.insert(0, today)


class ChangeCostsWindow(AddCostsWindow):
    def __init__(self, tree=None, info=None):
        super().__init__()
        self.title('Редактировать')
        self.costs_tree = tree
        self.show_info = info
        self.default_values()
        self.btn_add_costs['text'] = 'Редактировать'
        self.btn_add_costs.bind('<Button-1>', lambda event: self.change_costs(self.name_entry.get(),
                                                                              self.category.get(),
                                                                              self.date_entry.get(),
                                                                              self.sum_entry.get(),
                                                                              self.bills.get()))

    def change_costs(self, costs_name, categories, date, costs_sum, bills):
        categories_id = self.categories_dict[categories]
        bills_id = self.bills_dict[bills]
        string_id = self.costs_tree.set(self.costs_tree.selection()[0], '#1')
        old_values = db.select_old_sum_id_costs([string_id])
        old_sum = abs(old_values[0])
        db.bill_sum_plus(old_sum, old_values[1])
        db.change_costs(string_id, costs_name, categories_id, date, costs_sum, bills_id)
        costs_sum_new = abs(float(costs_sum))
        db.bill_sum_minus(costs_sum_new, bills_id)
        self.show_info()
        self.app.notebook.destroy()
        self.app.notebook = Notebook()
        self.app.notebook.select([1])
        self.destroy()

    def default_values(self):
        string_id = self.costs_tree.set(self.costs_tree.selection()[0], '#1')
        values = db.get_string_values_costs(string_id)
        self.name_entry.insert(0, values[1])
        self.category.current(values[2]-1)
        self.date_entry.insert(0, values[3])
        self.sum_entry.insert(0, values[4])
        self.bills.current(values[5]-1)

    def default_date(self):
        pass


class AddIncomeWindow(AddCostsWindow):
    def __init__(self):
        super().__init__()
        self.init()
        self.default_date()

    def init(self):

        date_lable = tk.Label(self, text='Дата:')
        self.date_entry = tk.Entry(self, width=10)
        date_lable.grid(row=1, column=0)
        self.date_entry.grid(row=1, column=1)

        sum_lable = tk.Label(self, text='Сумма:')
        self.sum_entry = tk.Entry(self, width=10)
        sum_lable.grid(row=2, column=0)
        self.sum_entry.grid(row=2, column=1)

        salary_lable = tk.Label(self, text='Источник')
        self.category = ttk.Combobox(self, values=list(self.categories_dict.keys()))
        salary_lable.grid(row=3, column=0)
        self.category.grid(row=3, column=1)

        bills_lable = tk.Label(self, text='Счет зачисления:')
        self.bills = ttk.Combobox(self, values=list(self.bills_dict.keys()))
        bills_lable.grid(row=4, column=0)
        self.bills.grid(row=4, column=1)

        self.btn_add_costs = tk.Button(self, text='Добавить')
        self.btn_add_costs.bind('<Button-1>', lambda event: self.add_income(self.date_entry.get(),
                                                                            self.category.get(),
                                                                            self.sum_entry.get(),
                                                                            self.bills.get()))
        self.btn_add_costs.grid(row=5, column=1)

    def create_categories_dict(self):
        table_values = db.get_values('salary')
        categories_dict = {y:x for x, y, z, in table_values}
        return categories_dict

    def add_income(self, date, salary, income_sum, bill):
        salary_id = self.categories_dict[salary]
        bill_id = self.bills_dict[bill]
        db.add_income(date, salary_id, income_sum, bill_id)
        db.bill_sum_plus(income_sum, bill_id)
        self.app.notebook.destroy()
        self.app.notebook = Notebook()
        self.app.notebook.select([2])

class ChangeIncomeWindow(AddIncomeWindow):
    def __init__(self, tree, info):
        super().__init__()
        self.costs_tree = tree
        self.show_info = info
        self.default_values()
        self.btn_add_costs['text'] = 'Редактировать'
        self.btn_add_costs.bind('<Button-1>', lambda event: self.change_income(self.date_entry.get(),
                                                                               self.category.get(),
                                                                               self.sum_entry.get(),
                                                                               self.bills.get()))

    def change_income(self, date, salary, income_sum, bill):
        string_id = self.costs_tree.set(self.costs_tree.selection()[0], '#1')
        salary_id = self.categories_dict[salary]
        bill_id = self.bills_dict[bill]
        old_values = db.select_old_sum_id_income([string_id])
        db.bill_sum_minus(old_values[0], old_values[1])
        db.change_income(string_id, date, salary_id, income_sum, bill_id)
        db.bill_sum_plus(income_sum, bill_id)
        self.app.notebook.destroy()
        self.app.notebook = Notebook()
        self.app.notebook.select([2])

    def default_values(self):
        string_id = self.costs_tree.set(self.costs_tree.selection()[0], '#1')
        values = db.get_string_values_income(string_id)
        self.date_entry.insert(0, values[1])
        self.category.current(values[2]-1)
        self.sum_entry.insert(0, values[3])
        self.bills.current(values[4]-1)

    def default_date(self):
        pass


class IncomeTableWindow(CostsTableWindow):
    def __init__(self):
        super().__init__()
        self.table_name = 'income'

    def create_tree(self):
        self.income_tree = ttk.Treeview(self, columns=('ID', 'date', 'salary', 'income_sum', 'bill_id'),
                                        height=15, show='headings')
        self.income_tree.column('ID', width=30, anchor=tk.CENTER)
        self.income_tree.column('date', width=30, anchor=tk.CENTER)
        self.income_tree.column('salary', width=150, anchor=tk.CENTER)
        self.income_tree.column('income_sum', width=100, anchor=tk.CENTER)
        self.income_tree.column('bill_id', width=30, anchor=tk.CENTER)

        self.income_tree.heading('ID', text='ID')
        self.income_tree.heading('date', text='Дата')
        self.income_tree.heading('salary', text='Источник дохода')
        self.income_tree.heading('income_sum', text='Сумма')
        self.income_tree.heading('bill_id', text='Счет')
        self.income_tree.pack(fill=tk.BOTH)

    def open_add_window(self):
        AddIncomeWindow()

    def open_change_window(self):
        ChangeIncomeWindow(self.income_tree, self.show_info)

    def delete_string(self):
        string_id = self.income_tree.set(self.income_tree.selection()[0], '#1')
        old_values = db.select_old_sum_id_income([string_id])
        db.bill_sum_minus(old_values[0], old_values[1])
        db.delete_income([string_id])
        self.show_info()

    def show_info(self):
        db.get_income_val(self.income_tree)


class GoalTableWindow(CostsTableWindow):
    def __init__(self):
        super().__init__()
        self.table_name = 'goals'
        self.show_info()

    def create_tree(self):
        self.goal_tree = ttk.Treeview(self, columns=('ID', 'goal_name', 'goal_sum', 'goal_date'),
                                      height=15, show='headings')
        self.goal_tree.column('ID', width=10, anchor=tk.CENTER)
        self.goal_tree.column('goal_name', width=100, anchor=tk.CENTER)
        self.goal_tree.column('goal_sum', width=50, anchor=tk.CENTER)
        self.goal_tree.column('goal_date', width=50, anchor=tk.CENTER)

        self.goal_tree.heading('ID', text='ID')
        self.goal_tree.heading('goal_name', text='Цель')
        self.goal_tree.heading('goal_sum', text='Сумма')
        self.goal_tree.heading('goal_date', text='Дата ')
        self.goal_tree.pack(fill=tk.BOTH)

    def open_add_window(self):
        AddGoalWindow()

    def open_change_window(self):
        goal_id = self.goal_tree.set(self.goal_tree.selection()[0], '#1')
        ChangeGoalWindow(goal_id)

    def delete_string(self):
        string_id = self.goal_tree.set(self.goal_tree.selection()[0], '#1')
        db.delete_goal([string_id])
        self.show_info()

    def show_info(self):
        db.show_info(self.goal_tree, self.table_name)


class AddGoalWindow(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.app = app
        self.title('Добавить')
        self.geometry('200x150+500+200')
        self.resizable(False, False)
        self.focus_set()
        self.grab_set()
        self.main()

    def main(self):
        self.lable_goal = tk.Label(self, text='Цель:')
        self.lable_goal.grid(row=0, column=0)
        self.entry_goal_name = tk.Entry(self, width=15)
        self.entry_goal_name.grid(row=0, column=1)

        self.lable_sum = tk.Label(self, text='Сумма')
        self.lable_sum.grid(row=1, column=0)
        self.entry_sum = tk.Entry(self, width=15)
        self.entry_sum.grid(row=1, column=1)

        self.lable_date = tk.Label(self, text='Дата')
        self.lable_date.grid(row=2, column=0)
        self.entry_date = tk.Entry(self, width=15)
        self.entry_date.grid(row=2, column=1)

        self.btn_add = tk.Button(self, text='Добавить', width=10)
        self.btn_add.bind('<Button-1>', lambda event: self.function_goal(self.entry_goal_name.get(),
                                                                         self.entry_sum.get(),
                                                                         self.entry_date.get()))
        self.btn_add.grid(row=3, column=1)

    def function_goal(self, name, summ, date):
        db.add_goal(name, summ, date)
        self.app.notebook.destroy()
        self.app.notebook = Notebook()
        self.app.notebook.select([3])


class ChangeGoalWindow(AddGoalWindow):
    def __init__(self, goal_id):
        super().__init__()
        self.goal_id = goal_id
        self.title('Редактировать')

    def function_goal(self, name, summ, date):
        db.change_goal(name, summ, date, self.goal_id)
        self.app.notebook.destroy()
        self.app.notebook = Notebook()
        self.app.notebook.select([3])


class MainWindow(tk.Frame):
    def __init__(self):
        super().__init__()
        self.data = lc.ParamTable(login)
        self.main_param()
        self.view_param_table()



    def main_param(self):
        self.title_lable = tk.LabelFrame(self, text='Таблица параметров')
        self.main_table = ttk.Treeview(self.title_lable, columns=('param', 'weak', 'month'), show='headings')
        self.main_table.column('param', width=150, anchor=tk.CENTER)
        self.main_table.column('weak', width=50, anchor=tk.CENTER)
        self.main_table.column('month', width=50, anchor=tk.CENTER)
        self.main_table.heading('param', text='Параметры')
        self.main_table.heading('weak', text='Неделя')
        self.main_table.heading('month', text='Месяц')
        self.main_table.pack(side=tk.LEFT)
        self.title_lable.grid(row=1, column=0)

    def view_param_table(self):
        [self.main_table.delete(i) for i in self.main_table.get_children()]
        [self.main_table.insert('', 'end', values=row) for row in self.data.create_table()]


class AnaliticWindow(tk.Frame):
    def __init__(self):
        super().__init__()
        self.data = lc.CostsFrame(login)
        self.dict_cat = self.create_categories_dict()
        self.now_window = tk.Frame(self)
        self.previous_window = tk.Frame(self)
        self.now_window.grid(row=0, column=0)
        self.previous_window.grid(row=0, column=1)
        self.now_month()
        self.previous_month()


    def weaks_costs(self, master):
        self.weak_table = ttk.Treeview(master, columns=('weak', 'sum_weak'), show='headings')
        self.weak_table.column('weak', width=50, anchor=tk.CENTER)
        self.weak_table.column('sum_weak', width=50, anchor=tk.CENTER)
        self.weak_table.heading('weak', text='Неделя')
        self.weak_table.heading('sum_weak', text='Сумма')
        self.weak_table.grid(row=0, column=0)

    def cat_costs(self, master):
        self.cat_table = ttk.Treeview(master, columns=('cat', 'cat_sum'), show='headings')
        self.cat_table.column('cat', width=100, anchor=tk.CENTER)
        self.cat_table.column('cat_sum', width=50, anchor=tk.CENTER)
        self.cat_table.heading('cat', text='Категория')
        self.cat_table.heading('cat_sum', text='Сумма')
        self.cat_table.grid(row=0, column=1)

    def show_weaks_costs(self, month='now'):
        values = self.data.filter_weak_sum(month).values.tolist()
        [self.weak_table.delete(i) for i in self.weak_table.get_children()]
        [self.weak_table.insert('', 'end', values=row) for row in values]

    def show_cat_costs(self, month='now'):
        values = self.data.filter_categories_sum(month).values.tolist()
        for i in range(len(values)):
            values[i][0] = self.dict_cat[values[i][0]]
        [self.cat_table.delete(i) for i in self.cat_table.get_children()]
        [self.cat_table.insert('', 'end', values=row) for row in values]

    def create_categories_dict(self):
        table_values = db.get_values('categories')
        categories_dict = {x:y for x, y in table_values}
        return categories_dict

    def previous_month(self):
        self.weaks_costs(self.previous_window)
        self.cat_costs(self.previous_window)
        self.show_weaks_costs(month='previous')
        self.show_cat_costs(month='previous')
        self.lable_sum_weak = tk.Label(self.previous_window,
                                       text='Общая сумма:{}'.format(self.data.sum_weakcosts))
        self.lable_sum_weak.grid(row=1, column=0, columnspan=2)

    def now_month(self):
        self.weaks_costs(self.now_window)
        self.cat_costs(self.now_window)
        self.show_weaks_costs(month='now')
        self.show_cat_costs(month='now')
        self.lable_sum_weak = tk.Label(self.now_window,
                                  text='Общая сумма:{}'.format(self.data.sum_weakcosts))
        self.lable_sum_weak.grid(row=1, column=0, columnspan=2)


class Notebook(ttk.Notebook):
    def __init__(self):
        super().__init__(root)
        self.init()
        self.pack(expand=1, fill='both')

    def init(self):
        self.add(MainWindow(), text='Главная')
        self.add(CostsTableWindow(), text='Список расходов')
        self.add(IncomeTableWindow(), text='Список Доходов')
        self.add(GoalTableWindow(), text='Финансовое планирование')

    def add_analitic(self):
        self.add(AnaliticWindow(), text='Финансовый анализ')


if __name__ == "__main__":
    root = tk.Tk()
    root.title('Safe Coins')
    root.geometry('700x500+300+100')
    new_db = datb.DbMain()
    app = InputWind()
    app.lift(root)
    app.mainloop()
