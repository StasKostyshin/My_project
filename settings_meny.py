import os
import tkinter as tk
from tkinter import ttk
from tkinter import *
from PIL import ImageTk, Image
import hashlib
import pyttsx3
from tkinter import filedialog as fd
from avto_num import read_text_in_photo
from gtts import gTTS
import pdfplumber
from pathlib import Path
import multiprocessing
import subprocess
from playsound import playsound
from tkinter.messagebox import showerror, showinfo
import threading
import vlc


engine = pyttsx3.init('sapi5')#################
voices = engine.getProperty('voices')#########################
engine.setProperty('voice', voices[1].id)#########################

def speak(audio):# Функция для вставки голосавого помошника
    engine.say(audio)
    engine.runAndWait()

def reference():# Функция для открытия файла HTML
    url = "index.html"
    try:  # should work on Windows
        os.startfile(url)
    except AttributeError:
        try:  # should work on MacOS and most linux versions
            subprocess.call(['open', url])
        except:
            print('Could not open URL')


def camera_id():# Функция для указания ID камеры
    window = tk.Toplevel()
    window.title('Сохранение ID камеры')
    window.geometry("400x130+400+300")
    window.iconbitmap('image/logo_cam.ico')
    window.resizable(False, False)

    label_camera = tk.Label(window, text='ID камеры наблюдения')
    label_camera.place(x=50, y=30)

    camera_entry = ttk.Entry(window)
    camera_entry.place(x=200, y=30)

    btn_ok = ttk.Button(window, text='Сохранить')
    btn_ok.place(x=220, y=70)
    btn_ok.bind('<Button-1>', lambda event: save_cam(camera_entry.get()))
    btn_ok.bind('<Button1-1>', lambda event: window.destroy(), add='+')

    def save_cam(camera_id):# Функция сохранения указаных данных в файл
        speak('Camera ID data saved')
        with open('camera.txt', 'w', encoding='utf-8') as camera:
            camera.write(camera_entry.get())

# def fail_in_txt():
def file_in_txt():
    filetypes = ( # Переменная с файлами изображения
        ("Изображения", "*.jpg;*.jpeg;*.png;*.gif;*.bmp"),
        ("Все файлы", "*.*")
    )
    image_input = fd.askopenfilename(filetypes=filetypes)# Выберм только файлы изображений
    if Path(image_input).is_file(): # Если выбранный файл файл
        read_text_in_photo(image_input)# Прочитаем текс из файла если он есть
        os.startfile('text.txt')# Выведем этот текст на экран
    else:# Если файл не выбран
        showerror(title='Файл не выбран', message='Вы не выбрали файл')# Покажем сообщение о не выборе файла

def read_pdf():# Функция преобразования PDF в аудиокнигу а так-же прослушивание взятого PDF
    file_path = fd.askopenfilename(filetypes=[('PDF Файлы','*.pdf')])# Выберем тольклько файлы формата PDF
    if Path(file_path).is_file():
        with pdfplumber.PDF(open(file=file_path, mode='rb')) as pdf:# Открытие PDF на чтение в бинарном формате
            pages = [page.extract_text() for page in pdf.pages]# Извлечение данных постранично из PDF

        text = ''.join(pages)# добавим страницы в переменную
        text = text.replace('\n','')# Заменим перенос строки в переменной
        my_audio = gTTS(text=text, lang='ru', slow=False)

        file_name = Path(file_path).stem
        if not os.path.isdir("C:/Audio_books/"):# Если директории на диске C с именем Audio_books нет
            os.mkdir("C:/Audio_books/")# создадим данную категорию
        try:
            my_audio.save(f'C:/Audio_books/{file_name}.mp3') # Сохраним аудиокнигу в созданную директорию
            showinfo(title='Создан', message=f'Аудио книга {file_name} создана')
        except:
            showerror(title='Разрыв', message='Обрыв с интернетом, необходимо проверить соединение')
    else:
        showerror(title='Файл не выбран', message='Вы не выбрали файл')


def pdf_in_audio():
    flow_pdf = threading.Thread(target=read_pdf)
    flow_pdf.start()



def menu_set(root):# Запуск главного цикла окна
    menu = tk.Menu()
    root.config(menu=menu)

    admin_meny = tk.Menu(menu, tearoff=0)
    menu.add_cascade(label='Администрирование', menu=admin_meny)
    admin_meny.add_command(label='Регистрация', command=registration)
    admin_meny.add_command(label='Указание ID Камеры', command=camera_id)

    fail_meny = tk.Menu(menu, tearoff=0)
    menu.add_cascade(label='Работа с файлами', menu=fail_meny)
    fail_meny.add_command(label='Считать текс с фото', command=file_in_txt)
    fail_meny.add_command(label='Прочитать PDF', command=pdf_in_audio)

    help_meny = tk.Menu(menu, tearoff=0)
    menu.add_cascade(label='Помощь', menu=help_meny)
    help_meny.add_command(label='Справка', command=reference)
    help_meny.add_command(label='О программе', command=about_program)

def registration():# Функция регистрации######################################
    winreg=tk.Toplevel()
    winreg.title('регистрирование пользователя')
    winreg.geometry("550x500+50+50")
    winreg.resizable(False,False)
    global image_address_registration
    image_address_registration = ImageTk.PhotoImage(file='image/fon_registration.png')
    winreg.iconbitmap('image/login.ico')#####

    creg=Canvas(winreg,width=550, height=500, bg='#C0C0C0')
    creg.pack(expand=True, fill= BOTH)

    creg.create_image(70, 20, anchor='nw', image=image_address_registration)

    creg.create_text(270,20,justify=CENTER,width=520, text='Регистрация',font=('Courier',20,'bold'), fill='#800080')
    creg.create_text(270,70, text='Введите логин',font=('Courier',14, 'bold'), fill='#800080')
    reg_login=Entry(creg, font=('Courier',14,'bold'))
    creg.create_window(170, 85, anchor=NW, window=reg_login, width=220, height=30 )
    creg.create_text(270,150, text='Введите пароль',font=('Courier',14, 'bold'), fill='#800080')
    reg_password=Entry(creg, show="*", font=('Courier',14,'bold'))
    creg.create_window(170,170, anchor=NW, window=reg_password, width=220, height=30 )

    butreg=tk.Button(creg, text='Регистрация', font=('Courier',14,'bold'),fg='#800080',command=lambda: [save()])
    creg.create_window(170, 220, anchor=NW, window=butreg, width=220, height=50)


    def save():
        login_save = hashlib.sha256(reg_login.get().encode() + reg_password.get().encode()).hexdigest()
        with open('login.csv', 'w') as log:
            log.write(f'{login_save}')

        creg.create_text(270, 310, text='Регистрация завершена, данные сохранены', font=('Courier', 14, 'bold'))
        butreg = tk.Button(creg, text='Выход', font=('Courier', 14, 'bold'), command=lambda: [winreg.destroy()])
        creg.create_window(170, 370, anchor=NW, window=butreg, width=220, height=50)

def about_program():  # Функция о программе#######################################
    win_about=tk.Toplevel()
    win_about.title('О программе')
    win_about.geometry("550x500+50+50")
    global image_address_about
    image_address_about = ImageTk.PhotoImage(file='image/fon_about.png')
    win_about.iconbitmap('image/invoice.ico')  ##########
    creg=Canvas(win_about,width=550, height=500, bg='gold')
    creg.pack(expand=True, fill= BOTH)

    creg.create_image(0, 0, anchor='nw',image=image_address_about)

    creg.create_text(270,50,justify=LEFT,width=500,text="""Программа создана при поддержке учебного центра:
    """,font=('Courier',15,'bold', ), fill='#90EE90')
    creg.create_text(270,120,justify=LEFT,width=500, text='Цель программы: '
                                                  'улучшить и компьютеризи́ровать работу сотрудников охраны', font=('Courier', 16, 'bold'), fill='#90EE90')
    creg.create_text(270,330, text='Дата релиза: 2023 год',font=('Courier',16, 'bold'), fill='#90EE90')
    creg.create_text(270,350, text='Разработчик: Костышин Станислав Максимович.',font=('Courier',15, 'bold'),fill='#90EE90')
