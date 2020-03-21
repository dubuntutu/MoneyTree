import pyautogui as pag
import time
import random
import datetime
import configparser
import tkinter as tk
import tkinter.messagebox
import threading
import os, signal, sys
import psycopg2 as sql
import subprocess
from windowsModule import *

VERSION_DATE = datetime.date.fromisoformat('2020-03-09')

if not 'MoneyTree.py' in os.listdir():      #Проверка, чтобы файл, который, в случае чего, следует удалить, имел определенное название "MoneyTree.exe"
    tk.messagebox.showwarning('Error', 'Не найдет исполняемый файл.\nПереустановите программу.')
    sys.exit()

con, cur = None, None       #Если в базе данных найдется свежее обновление, программа удаляет сама себя и записывает ссылку на облако в файл
try:        
    con = sql.connect(database='test', user='test', password='test')
    cur = con.cursor()
    cur.execute('''SELECT url FROM updatelist WHERE update_date=(SELECT max(update_date) from updatelist) AND update_date > %s;''', [VERSION_DATE])
    url = cur.fetchone()
    if url is not None:
        tk.messagebox.showwarning('Update', 'Перейдите по ссылке и установите новую версию программы. Текущая версия больше не доступна\n%s\n(Ссылка записана в файл в текущей папке)' %(url))
        with open('url.txt', 'w')as fh:
            fh.write(url[0])
        os.remove('MoneyTree.py')
        sys.exit()
except sql.DatabaseError as err:
    tk.messagebox.showwarning('Error', err)
    time.sleep(2)
    sys.exit()
except EnvironmentError as err:
    tk.messagebox.showwarning('Error', err)
    time.sleep(2)
    sys.exit()
finally:
    if cur: cur.close()
    if con: con.close()

app = tk.Tk()
window = LoginWindow(app)
app.mainloop()
