import tkinter as tk
from tkinter import *
import pyttsx3
import subprocess
import hashlib
import sys

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def speak(audio):# Функция вывода голоса
    engine.say(audio)
    engine.runAndWait()

def on_closing():
    speak('Login window closed')
    sys.exit()

def login():
    winlog = tk.Tk()
    winlog.title('Введите логин и пароль')
    winlog.iconbitmap('image/login.ico')
    winlog.geometry("860x550+300+200")
    winlog.resizable(False, False)
    winlog.protocol("WM_DELETE_WINDOW", on_closing)


    clog = Canvas(winlog, width=550, height=500, bg='#333333')
    clog.pack(expand=True, fill=BOTH)

    clog.create_text(430, 20, justify=CENTER, width=520, text='Авторизация', font=('Courier', 24, 'bold',))
    clog.create_text(430, 70, text='Введите логин', font=('Courier', 16, 'bold'))
    entry_login = Entry(clog, font=('Courier', 16, 'bold'))
    clog.create_window(330, 85, anchor=NW, window=entry_login, width=220, height=40)
    clog.create_text(430, 150, text='Введите пароль', font=('Courier', 16, 'bold'))
    entry_password = Entry(clog, show="*", font=('Courier', 16, 'bold'))
    clog.create_window(330, 170, anchor=NW, window=entry_password, width=220, height=40)

    butlog = tk.Button(clog, text='Ввод',bg='#FF3399', font=('Courier', 16, 'bold'), command=lambda: [log_pas()])
    clog.create_window(330, 240, anchor=NW, window=butlog, width=220, height=50)



    def log_pas():
        # Шифруем входяшие данные от пользователя использую библиотеку hashlib. с алгоритмом sha256 и методом hexdigest() имеюшим только 16-е значения
        login_and_password = hashlib.sha256(entry_login.get().encode() + entry_password.get().encode()).hexdigest()

        try:# Пробуем (если файл с данными есть)
            with open('login.csv', 'r') as log:# Открываем файл
                line = log.readline().strip()# присваиваем переменной первую строку из прочитанного файла
                if line == login_and_password: # Сравниваем данный с файла с введёнными данными
                        speak('Correct login and password. You can continue')
                        winlog.destroy() # Уничтожаем окно

                else:
                    speak('Invalid password or login')# слушаем что парол или логин введены не верно
        except:# Если файла с данными нет
            winlog.destroy()# Уничтожаем окно
            speak('Login and password are not assigned. Entrance to the application is free')# Узнаём что вход свободный

    winlog.mainloop()

if __name__ == '__main__':
    login()