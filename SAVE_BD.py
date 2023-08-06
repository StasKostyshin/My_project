import sqlite3
import tkinter as tk
from tkinter import ttk

def in_search(self):
    for child in self.tree.get_children():# Удаление всех существующих элементов в дереве
        self.tree.delete(child)
    for row in self.su_db.c.fetchall(): # Вставка новых элементов на основе данных из базы данных
        self.tree.insert('', 'end', values=row)


class History(tk.Frame):
    def __init__(self, win):
        win.title(f"История запросов")
        super().__init__(win)
        self.init_main_hist()
        self.su_db = su_BD()
        self.view_records()

    def init_main_hist(self):
        self.coon = sqlite3.connect('cars_in.db')  # Название базы данных
        self.c = self.coon.cursor()
        toolbar = tk.Toplevel(bg='#d7d8e0', bd=2)
        # toolbar.pack(side=tk.TOP, fill=tk.X)

        self.search_img = tk.PhotoImage(file='image/search.png')
        btn_search = tk.Button(toolbar, text='Поиск в истории', bg='#d7d8e0', bd=0, image=self.search_img,
                               compound=tk.TOP, command=self.open_search_dialog)
        btn_search.pack(side=tk.LEFT)

        self.refresh_img = tk.PhotoImage(file='image/refresh.png')
        btn_refresh = tk.Button(toolbar, text='Обновить историю', bg='#d7d8e0', bd=0, image=self.refresh_img,
                                compound=tk.TOP, command=self.view_records)
        btn_refresh.pack(side=tk.LEFT)

        self.tree = ttk.Treeview(toolbar, columns=("ID", 'organization', 'number_cars', 'date'), show='headings')

        self.tree.column('ID', width=20, anchor=tk.N)
        self.tree.column('organization', width=530, anchor=tk.N)
        self.tree.column('number_cars', width=200, anchor=tk.N)
        self.tree.column('date', width=200, anchor=tk.N)

        self.tree.heading('ID', text='ID')
        self.tree.heading('organization', text='Действия')
        self.tree.heading('number_cars', text='Номер/Ф.И.О.')
        self.tree.heading('date', text='Дата/Время')


        self.tree.pack()
        self.init_history()


    def view_records(self):
        self.su_db.c.execute('''SELECT * FROM cars_in''')
        in_search(self)

    def search_records(self, number_cars):
        number_cars = ('%' + number_cars + '%',)
        self.su_db.c.execute('''SELECT * FROM cars_in WHERE number_cars LIKE ?''', number_cars)
        in_search(self)

    def search_organization(self, organization):
        organization = ('%' + organization + '%',)
        self.su_db.c.execute('''SELECT * FROM cars_in WHERE organization LIKE ?''', organization)
        in_search(self)
    #
    def search_date(self, date):
        self.su_db.c.execute('''SELECT * FROM cars_in WHERE date LIKE ?''', (f'%{date}%',))
        in_search(self)

    def open_search_dialog(self):
        Search(self)

    def init_history(self):
        try:
            coon = sqlite3.connect('cars_in.db')
            c = coon.cursor()
            c.execute('''SELECT * FROM cars_in''')
            rows = c.fetchall()
            [self.tree.delete(i) for i in self.tree.get_children()]
            [self.tree.insert('', 'end', values=row) for row in rows]
            coon.close()
        except Exception as e:
            print(f'Ошибка: {e}')

class Search(tk.Toplevel):# класс по поиску из базы данных
    def __init__(self, app):
        app.pack()
        super().__init__()
        self.init_search()
        self.view = app

    def init_search(self):
        self.title('Поиск')
        self.geometry('450x100+400+300')
        self.resizable(False, False)

        label_search = tk.Label(self, text='Поиск')
        label_search.place(x=50, y=20)

        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=105, y=20, width=150)

        btn_cancel = tk.Button(self, text='Закрыть',bg='red', command=self.destroy)
        btn_cancel.place(x=355, y=50)

        btn_search = ttk.Button(self, text='Поиск авто/Ф.И.О.')
        btn_search.place(x=235, y=50)

        btn_search_org = ttk.Button(self, text='Поиск по действиям')
        btn_search_org.place(x=110, y=50)

        btn_search_date = ttk.Button(self, text='Поиск по дате')
        btn_search_date.place(x=20, y=50)

        btn_search.bind('<Button-1>', lambda event: self.view.search_records(self.entry_search.get().title()))
        btn_search.bind('<Button-1>', lambda event: self.destroy(), add='+')

        btn_search_org.bind('<Button-1>', lambda event: self.view.search_organization(self.entry_search.get()))
        btn_search_org.bind('<Button-1>', lambda event: self.destroy(), add='+')

        btn_search_date.bind('<Button-1>', lambda event: self.view.search_date(self.entry_search.get().title()))
        btn_search_date.bind('<Button-1>', lambda event: self.destroy(), add='+')


class su_BD:
    def __init__(self):  # Функция по созданию базы данных
        self.coon = sqlite3.connect('cars_in.db')  # Название базы данных
        self.c = self.coon.cursor()
        self.c.execute(  # Создание базы данных с тремя колонками
            '''CREATE TABLE IF NOT EXISTS cars_in (id integer primary key, organization text, number_cars text, date text)'''
        )
        self.coon.commit()  # Сохранение

    def insert_data_in(self, organization, number_car,
                       ctime):  # добавление в базу данных значений в колонки organization, number_cars
        self.c.execute(f'''INSERT INTO cars_in (organization, number_cars, date) VALUES (?, ?, ?)''',
                       (organization, number_car, ctime))
        self.coon.commit()  # Сохранение изменений


