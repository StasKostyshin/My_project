import locale
import tkinter as tk
from tkinter import ttk
import sqlite3
import avto_num
import login
import voise
from tkinter.messagebox import showerror, showwarning, showinfo
import pyttsx3
import SAVE_BD
from time import strftime
import settings_meny
from PIL import ImageTk, Image
import csv

# engine = pyttsx3.init('sapi5')#################
# voices = engine.getProperty('voices')#########################
# engine.setProperty('voice', voices[1].id)#########################

locale.setlocale(locale.LC_ALL, 'ru')

write_str_num = ("Поиск: по Номеру авто\Ф.И.О.")
write_str_avtonum = ("Поиск: автоматически по Номеру авто\Ф.И.О.")
write_str_org = ("Поиск по организациям")
write_str_avtonum_null = ("Не соответствует количеству знаков")
write_str_avtonum_errors = ("Не распознан с камеры")
write_cars_in = ("Поиск по номерам/Ф.И.О..Есть в списке: ")
write_cars_not = ("Нет в списке: ")

def voice_in_text(voice):
    voice_ = ''
    for i in voice:
        voice_ += i
    voice_on_text = voice_.replace('%','')
    return voice_on_text

def in_text(rows):
    org = []
    for car in rows:
        org.append(car[1])
    org_ = ','.join(org)
    return org_

# def speak(audio):#######################Функция для вставки голосавого помошника
#     engine.say(audio)#######################
#     engine.runAndWait()########################
names = []


def save_in_fail(name, organization):
    with open("history.csv", mode="a", encoding='utf-8') as w_file:
        file_writer = csv.writer(w_file, delimiter=",", lineterminator="\r")
        if name in names:
            file_writer.writerow(["Имя:" f"{name} вышел", "Организация:" f"{organization}", "Дата:" f"{strftime('%d%B %Y Время: %H:%M:%S')}"])
        else:
            file_writer.writerow(["Имя:" f"{name} вошёл", "Организация:" f"{organization}", "Дата:" f"{strftime('%d%B %Y Время: %H:%M:%S')}"])

def history_save_( organization, str_write):# Функция сохранения в Базу данных истории событий организации
    for i in organization:
        su_db.insert_data_in(f"{str_write}: {i[1]}", f"{i[1]}", f"{strftime('%d%B %Y Время: %H:%M:%S')}")
        break

def history_save_cars(cars,cars_, str_write_):# Функция сохрания в Базу данных событийй поиска авто, сотрудников сторонних организаций
    organizations = in_text(cars)
    search = []
    for car_ in cars_:
        search.append(car_[2])
    su_db.insert_data_in(f"{str_write_}: {organizations}", f"Номер/Ф.И.О.: {search[0]}", f"{strftime('%d%B %Y Время: %H:%M:%S')}")
    save_in_fail(search[0], organizations)

def history_error(str_write):# Функция сохрания в Базу данных ошибки по автопоиску
    su_db.insert_data_in(f'{str_write}: Ошибка', f'Нет', f"{strftime('%d%B %Y Время: %H:%M:%S')}" )

def in_search(self):
    for child in self.tree.get_children():# Удаление всех существующих элементов в дереве
        self.tree.delete(child)
    for row in self.db.c.fetchall(): # Вставка новых элементов на основе данных из базы данных
        self.tree.insert('', 'end', values=row)

def in_search_(self, organization):
    for child in self.tree.get_children(): # Удаление всех существующих элементов в дереве
        self.tree.delete(child)
    for row in organization: # Вставка новых элементов на основе данных из списка
        self.tree.insert('', 'end', values=row)

def date_in(self):
    self.tree.column('ID', width=280)
    self.tree.heading('ID', text=f'Дата внесения')

def search_num(self, number_cars):# Функция по поиску по Ф.И.О. либо ноиеру
    self.db.c.execute('''SELECT last_name FROM employees WHERE last_name LIKE ?''', number_cars)
    self.cars = db.c.fetchall()
    if number_cars in self.cars:
        self.db.c.execute(
        '''SELECT in_date, name FROM organizations LEFT JOIN employees ON organizations.id=employees.organization_id
        WHERE last_name LIKE ?''', number_cars)
        self.cars = db.c.fetchall()
        organizations = in_text(self.cars)
        showinfo(title="Найдено", message=f"{number_cars[0]} найдено в {organizations}")
        in_search_(self, self.cars)
        date_in(self)
        self.db.c.execute('''SELECT * FROM employees WHERE last_name LIKE ?''', number_cars)
        self.cars_ = db.c.fetchall()
        history_save_cars(self.cars, self.cars_, write_cars_in)
        names.append(number_cars[0])
    else:
        su_db.insert_data_in(f"{write_str_num}:{number_cars[0]}",f"{write_cars_not}:{number_cars[0]}", f"{strftime('%d%B %Y Время: %H:%M:%S')}")
        showinfo(title="В базе нет", message=f"{number_cars[0]} не найдено")
        save_in_fail(number_cars[0], write_cars_not)
        names.append(number_cars[0])
        Main.view_records(self)
#########################################################################
class Main(tk.Frame):# Основной Класс наследуемый от tk.Frame(главное окно приложения)
    def __init__(self, root):# метод конструктора класса
        super().__init__(root)# конструктор родительского класса
        self.init_main()# вызов метода
        self.db = db
        self.su_db = su_db
        self.view_records()# вызов метода

    def init_main(self):
        toolbar = tk.Frame(bg = '#d7d8e0', bd=2)# Виджет рамки с цветом и границей
        toolbar.pack(side=tk.TOP, fill=tk.X)

        self.image_names_about = ImageTk.PhotoImage(file='image/fon_about.png')

        settings_meny.menu_set(root)

        self.add_img = tk.PhotoImage(file='image/add.png')
        btn_open_dialog = tk.Button(toolbar, text='Добавить', command=self.open_dialog, bg='#d7d8e0', bd=0,
                                    compound=tk.TOP, image=self.add_img, borderwidth = 0)
        btn_open_dialog.pack(side=tk.LEFT)

        self.refresh_img = tk.PhotoImage(file='image/refresh.png')
        btn_refresh = tk.Button(toolbar, text='Обновить', bg='#d7d8e0', bd=0, image=self.refresh_img,
                                compound=tk.TOP, command=self.view_records)
        btn_refresh.pack(side=tk.LEFT)

        root.bind('<Double-Button-1>', lambda event: self.double())

        root.bind("<Escape>", lambda x: settings_meny.read_pdf)

        self.search_img = tk.PhotoImage(file='image/search.png')
        btn_search = tk.Button(toolbar, text='Поиск', bg='#d7d8e0', bd=0, image=self.search_img,
                               compound=tk.TOP, command=self.open_search_dialog)
        btn_search.pack(side=tk.LEFT)

        self.avto_img = tk.PhotoImage(file='image/camera.png')
        btn_avto = tk.Button(toolbar, text='Автопоиск', bg='#d7d8e0', bd=0, image=self.avto_img,
                             compound=tk.TOP, command=self.avto_input)
        btn_avto.pack(side=tk.LEFT)

        self.vois_img = tk.PhotoImage(file='image/voise_search.png')
        voice_avto = tk.Button(toolbar, text='Голос поиск', bg='#d7d8e0', bd=0, image=self.vois_img,
                               compound=tk.TOP, command=self.voice_input)
        voice_avto.pack(side=tk.LEFT)

        self.delete_emp_img = tk.PhotoImage(file='image/delete_epm.png')
        btn_delete_emp = tk.Button(toolbar, text='Удалить данные', bg='#d7d8e0', bd=0, image=self.delete_emp_img,
                               compound=tk.TOP, command=self.delete_records_emp)
        btn_delete_emp.pack(side=tk.LEFT)

        self.delete_img = tk.PhotoImage(file='image/delete_org.png')
        btn_delete = tk.Button(toolbar, text='Удалить орг-ю', bg='#d7d8e0', bd=0, image=self.delete_img,
                               compound=tk.TOP, command=self.delete_records)
        btn_delete.pack(side=tk.LEFT)

        self.his_img = tk.PhotoImage(file='image/history.png')
        btn_his_img = tk.Button(toolbar, text='Истории событий', bg='#d7d8e0', bd=0, image=self.his_img,
                               compound=tk.TOP, command=self.open_history_dialog)
        btn_his_img.pack(side=tk.LEFT)

        self.tree = ttk.Treeview(self, columns=("ID", 'organization'), height=15, show='headings')


    def records(self, org_entry, emp_entry): # Функция записи в базу данных основную и запись в базу истории
        self.db.insert_data(org_entry, emp_entry)
        self.su_db.insert_data_in(f"Добавлено: организация/в организацию: {org_entry}", f"Данные: {emp_entry}",
                                  f"{strftime('%d%B %Y время: %H:%M:%S')}")
        self.view_records()

    def view_records(self):# Функция основного окна
        self.tree.column('ID', width=30, anchor=tk.CENTER)
        self.tree.column('organization', width=755, anchor=tk.CENTER)
        self.tree.heading('ID', text='ID')
        self.tree.heading('organization', text='Организация')
        self.tree.pack()
        self.db.c.execute('''SELECT * FROM organizations''')
        in_search(self)

    def double(self): #### Функция двойного клика для просмотра содержимого в организации
        date_in(self)
        self.tree.heading('organization', text=f'Данные в организации')
        for selected_item in self.tree.selection():
            self.db.c.execute(
                '''SELECT hire_date, last_name FROM employees JOIN organizations ON organizations.id=employees.organization_id
                    WHERE name LIKE ?''', (self.tree.set(selected_item, '#2'),))
            in_search(self)

    def search_cars(self, number_cars):#Функция по поиску номеров авто, Ф.И.О. в базе данных
        self.tree.heading('organization', text=f'{number_cars} в Организации')
        number_cars = (number_cars,)
        search_num(self, number_cars)

    def search_organization(self, organization):# Функция поиска по организациям
        self.tree.heading('organization', text=f'организации по поиску {organization}')
        organization = ('%' + organization + '%',)
        self.db.c.execute(
                '''SELECT * FROM organizations WHERE name LIKE ?''', organization)
        self.organization = db.c.fetchall()
        in_search_(self, self.organization)
        history_save_(self.organization, write_str_org)

    def avto_input(self):# Функция по фото из камеры
        try:
            number_cars = avto_num.main()
            if len(number_cars) < 7 or len(number_cars) > 7:
                showwarning(title='Не верное количество', message=f'Не верное количество знаков в номере авто {number_cars}, '
                                                               'введите вручную')
                history_error(write_str_avtonum_null)
                Search()
            else:
                self.tree.heading('organization', text=f'{number_cars} в Организации')
                number_cars = (f"{number_cars}",)
                search_num(self, number_cars)
        except:
            showerror(title='Ошибка распознавания', message= 'Камера не верно распознала номер, '
                                                             'введите вручную!')
            history_error(write_str_avtonum_errors)
            Search()

    def voice_input(self):# Функция поиска по голосу
        try:
            voice = voise.main()
            date_in(self)######################################################
            self.tree.heading('organization', text=f'{voice} в Организации')
            voice = (f"%{voice}%",)
            if voice == ('%%',):
                showerror(title='Ошибка распознавания', message='Голоса не слышно, '
                                                                'введите в ручную')
                Main.view_records(self)
                Search()
            else:
                self.db.c.execute(
                    '''SELECT in_date, name FROM organizations LEFT JOIN employees ON organizations.id=employees.organization_id
                    WHERE last_name LIKE ?''', voice)
                self.voice = db.c.fetchall()
                if self.voice == []:
                    Main.view_records(self)
                    voice_on_text = voice_in_text(voice)
                    showinfo(title="Не найдено", message=f"{voice_on_text} не найдено")
                    self.su_db.insert_data_in(f"Голосовой поиск : В базе не найдено",
                                              f"{voice_on_text}",
                                              f"{strftime('%d%B %Y Время: %H:%M:%S')}")
                else:
                    organization = in_text(self.voice)
                    voice_on_text = voice_in_text(voice)
                    showinfo(title="Найдено", message=f"{voice_on_text} Найдено в организации: {organization}")
                    self.su_db.insert_data_in(f"Голосовой поиск. Найден в: {organization}",
                                              f"{voice_on_text}",
                                              f"{strftime('%d%B %Y Время: %H:%M:%S')}")
                    in_search_(self, self.voice)


        except:
            showerror(title='Ошибка распознавания', message='Голосовая команда не верная, '
                                                    'введите вручную!')
            Search()

    def delete_records(self):# Функция удаления организации
        for selection_item in self.tree.selection():
            showinfo(title="Удалена организация", message=(str(self.tree.set(selection_item, '#2'))))
            self.db.c.execute('''DELETE FROM organizations WHERE id=?''', (self.tree.set(selection_item, '#1'),))
            self.db.c.execute('''DELETE FROM employees WHERE organization_id=?''', (self.tree.set(selection_item, '#1'),))
            self.su_db.insert_data_in(
                f"Удалено: организация {self.tree.set(self.tree.selection()[0], '#2')} ", f"", f"{strftime('%d%B %Y Время: %H:%M:%S')}")
            in_search(self)
            self.db.conn.commit()
            self.view_records()

    def delete_records_emp(self):# Функция удаления данных из организации
        for selected_item in self.tree.selection():
            showinfo(title="Удалены данные", message=(str(self.tree.set(selected_item, '#2'))))
            self.db.c.execute('''DELETE FROM employees WHERE last_name = ?''', (str(self.tree.set(selected_item,'#2')),))
            self.su_db.insert_data_in(
                    f"Удалено: данные {self.tree.set(selected_item, '#2')} ", f"",f"{strftime('%d%B %Y Время: %H:%M:%S')}")
            in_search(self)
            self.db.conn.commit()
            self.view_records()

    def open_dialog(self):
        Clild()

    def open_search_dialog(self):
        Search()

    def open_history_dialog(self):
        hist()

class Clild(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self):
        self.title("Добавить наименование организации")
        self.geometry('400x220+400+300')
        self.resizable(False, False)

        label_organization = tk.Label(self, text='Название организации')
        label_organization.place(x=50, y=50)

        label_select = tk.Label(self, text='Номер авто/Ф.И.О')
        label_select.place(x=50, y=80)

        self.org_entry = ttk.Entry(self)
        self.org_entry.place(x=200, y=50)

        self.emp_entry = ttk.Entry(self)
        self.emp_entry.place(x=200, y=80)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=300, y=170)

        self.btn_ok = ttk.Button(self, text='Добавить')
        self.btn_ok.place(x=220, y=170)
        self.btn_ok.bind('<Button-1>', lambda event: self.view.records(self.org_entry.get(),
                                                                        self.emp_entry.get()))

class Search(tk.Toplevel): # класс по поиску из базы данных
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app

    def init_search(self):
        self.title('Поиск')
        self.geometry('400x100+400+300')
        self.resizable(False, False)

        label_search = tk.Label(self, text='Поиск')
        label_search.place(x=50, y=20)

        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=105, y=20, width=150)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=295, y=50)

        btn_search = ttk.Button(self, text='Поиск авто/Ф.И.О.')
        btn_search.place(x=172, y=50)

        btn_search_org = ttk.Button(self, text='Поиск по организациям')
        btn_search_org.place(x=20, y=50)

        btn_search.bind('<Button-1>', lambda event: self.view.search_cars(self.entry_search.get().title()))
        btn_search.bind('<Button-1>', lambda event: self.destroy(), add='+')

        btn_search_org.bind('<Button-1>', lambda event: self.view.search_organization(self.entry_search.get()))
        btn_search_org.bind('<Button-1>', lambda event: self.destroy(), add='+')


def hist():
    SAVE_BD.History(root)

class DB: # Класс для создания и заполнения базы данных
    def __init__(self):
        self.conn = sqlite3.connect('organizations.db')# Создание базы данных
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS organizations
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              name TEXT NOT NULL,
              in_date TEXT NOT NULL)''')# Создание таблицы организаций
        self.c.execute('''CREATE TABLE IF NOT EXISTS employees
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              organization_id INTEGER NOT NULL,
              last_name TEXT NOT NULL,
              hire_date TEXT NOT NULL,
              FOREIGN KEY (organization_id) REFERENCES organizations(id))''')# Создание таблицы сотрудников(номеров авто)
        self.conn.commit()

    def insert_data(self, ogr_entry, emp_entry):
        self.c.execute('SELECT id FROM organizations WHERE name=?', (ogr_entry,))
        org_id = self.c.fetchone()
        if org_id is None:
            self.c.execute('INSERT INTO organizations (name, in_date) VALUES (?, ?)',
                           (ogr_entry, f"{strftime('%d%B %Y Время: %H:%S')}"))
            org_id = self.c.lastrowid
        else:
            org_id = org_id[0]

        # Добавляем сотрудника
        self.c.execute('INSERT INTO employees (organization_id, last_name, hire_date) VALUES (?, ?, ?)',
                    (org_id, emp_entry, f"{strftime('%d%B %Y Время: %H:%M:%S')}"))
        self.conn.commit()
        showinfo(title='Данные сохранены', message=f'Данные сохранены в {ogr_entry} добавилось {emp_entry}')

if __name__ == "__main__":
    login.login()
    root = tk.Tk() # Присвоение переменной модели tkinter
    db = DB()
    su_db = SAVE_BD.su_BD()
    app = Main(root)
    app.pack()
    root.title(f"Сторонние организации") # название окна
    root.iconbitmap('image/sec.ico')
    root.geometry("850x500+300+200") # размер окна
    root.resizable(False, False) # запрет на измение окна
    root.mainloop()


