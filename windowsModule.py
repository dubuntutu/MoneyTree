import pyautogui as pag
import time
import random
import datetime
import tkinter as tk
import tkinter.messagebox
import threading
import os, signal, sys
import psycopg2 as sql
import subprocess

from siteModule import Site
from countdownModule import CountdownWindow

class MainWindow():
    def __init__(self, parent, site, date_login, login, password):
        self.parent = parent
        self.site = site
        self.site.get_config()
        self.site_num = tk.IntVar()
        self.site_num.set(self.site.SITE_PAGE)
        self.search_num = tk.IntVar()
        self.search_num.set(self.site.SEARCH_PAGE)
        self.logging = tk.BooleanVar()
        self.logging.set(False)
        self.scrolling = tk.BooleanVar()
        self.scrolling.set(True)
        self.searching = tk.BooleanVar()
        self.searching.set(False)
        self.break_bool = tk.BooleanVar()
        self.break_bool.set(True)
        self.log = ''
        self.click_amount = 0
        self.date_login = date_login
        self.login = login
        self.password = password

        frame = tk.Frame(self.parent)
        frame.grid(row=0, column=0, sticky=tk.NSEW)

        self.CalibrateButton = tk.Button(frame, text='Калибровка', command=self.calibrate, underline=0)
        self.TimeButton = tk.Button(frame, text='Время', command=self.time, underline=0)
        self.strNumLabel = tk.Label(frame, text='№ страницы', anchor=tk.E)
        self.strNumEntry = tk.Entry(frame, textvariable=self.site_num)
        self.searchNumLabel = tk.Label(frame, text='№ стр поиска', anchor=tk.E)
        self.searchNumEntry = tk.Entry(frame, textvariable=self.search_num)
        #self.loggingLabel = tk.Label(frame, text='logging', anchor=tk.E)
        #self.loggingCheckbutton = tk.Checkbutton(frame, variable=self.logging, onvalue=True, offvalue=False)
        self.scrollingLabel = tk.Label(frame, text='scrolling', anchor=tk.E)
        self.scrollingCheckbutton = tk.Checkbutton(frame, variable=self.scrolling, onvalue=True, offvalue=False)
        self.searchingLabel = tk.Label(frame, text='searching', anchor=tk.E)
        self.searchingCheckbutton = tk.Checkbutton(frame, variable=self.searching, onvalue=True, offvalue=False)
        self.breakLabel = tk.Label(frame, text='Перерыв', anchor=tk.E)
        self.breakCheckbutton = tk.Checkbutton(frame, variable=self.break_bool, onvalue=True, offvalue=False)
        self.startButton = tk.Button(frame, text='Start', command=self.start_script)
        self.stopButton = tk.Button(frame, text='Stop', command=self.end_script)

        self.CalibrateButton.grid(row=0, column=3, columnspan=2, sticky=tk.NSEW)
        self.TimeButton.grid(row=1, column=3, columnspan=2, sticky=tk.NSEW)
        self.strNumLabel.grid(row=2, column=3, sticky=tk.NSEW)
        self.strNumEntry.grid(row=2, column=4, sticky=tk.NSEW)
        self.searchNumLabel.grid(row=3, column=3, sticky=tk.NSEW)
        self.searchNumEntry.grid(row=3, column=4, sticky=tk.NSEW)
        #self.loggingLabel.grid(row=4, column=3, sticky=tk.NSEW)
        #self.loggingCheckbutton.grid(row=4, column=4, sticky=tk.NSEW)
        self.scrollingLabel.grid(row=5, column=3, sticky=tk.NSEW)
        self.scrollingCheckbutton.grid(row=5, column=4, columnspan=2, sticky=tk.NSEW)
        self.searchingLabel.grid(row=6, column=3, sticky=tk.NSEW)
        self.searchingCheckbutton.grid(row=6, column=4, sticky=tk.NSEW)
        self.breakLabel.grid(row=7, column=3, sticky=tk.NSEW)
        self.breakCheckbutton.grid(row=7, column=4, sticky=tk.NSEW)
        self.startButton.grid(row=9, column=3, sticky=tk.NSEW)
        self.stopButton.grid(row=9, column=4, sticky=tk.NSEW)

        scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL)
        self.textBox = tk.Text(frame, yscrollcommand=scrollbar.set)
        scrollbar['command'] = self.textBox.yview
        scrollbar.grid(row=0, column=1, rowspan=9, sticky=tk.NS)
        self.textBox.grid(row=0, column=0, rowspan=9, sticky=tk.NSEW)

        window = self.parent.winfo_toplevel()
        window.rowconfigure(0, weight=1)
        window.columnconfigure(0, weight=1)
        
        frame.rowconfigure(8, weight=999)
        frame.columnconfigure(0, weight=999)
        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(2, weight=1)
        frame.columnconfigure(3, weight=1)
        frame.columnconfigure(4, weight=1)

        self.parent.geometry('500x500')
        self.parent.title('MoneyTree')

    def save_settings(self, *ignore):
        if not self.site_num.get() > 0:
            tk.messagebox.showwarning('Error', 'Минимальный номер страницы с рекламой: 1')
            return
        if not self.search_num.get() > 0:
            tk.messagebox.showwarning('Error', 'Минимальный номер страницы с поиском: 1')
            return
        if self.search_num.get() == self.site_num.get():
            tk.messagebox.showwarning('Error', 'Номера страниц не могут совпадать.')
            return
        self.site.SITE_PAGE = self.site_num.get()
        self.site.write_config()
        return True
        #self.site.SEARCH_PAGE

    def start_script(self, *ignore):
        choice = tk.messagebox.askyesnocancel('Save settings', 'Сохранить параметры в конфигурационный файл?')
        if choice is None:
            return
        elif choice:
            if not self.save_settings():
                return
        self.thread = threading.Thread(target=self.script, daemon=True)
        self.stop = False
        self.thread.start()

    def end_script(self, *ignore):
        self.stop = True
        self.textBox.insert(tk.END, 'Stopped\n\n')

    def script(self):                       #перенаправить поток вывода из функций Site в TextBox
        self.textBox.insert('Doing something...')
        time.sleep(1)

    def calibrate(self):
        form = CalibrationWindow(self.parent, self.site)

    def loginwindow(self):
        window = LoginWindow(self.parent)

    def time(self):
        form = TimeWindow(self.parent, self.site)

    def quit(self, *ignore):
        choice = tk.messagebox.askyesnocancel('Save settings', 'Сохранить параметры в конфигурационный файл?')
        if choice is None:
            return
        elif choice:
            if not self.save_settings():
                return

        con, cur = None, None
        try:
            con = sql.connect(database='test', user=self.login, password=self.password)
            cur = con.cursor()
            date_logout = datetime.datetime.now().isoformat(timespec='seconds')
            cur.execute("""UPDATE loginrecord SET date_logout=%s WHERE date_login=%s AND login=%s;""", (date_logout, self.date_login, self.login))
            con.commit()
        finally:
            if cur: cur.close()
            if con: con.close()

        self.parent.destroy()

class CalibrationWindow(tk.Toplevel):
    def __init__(self, parent, site):
        super(CalibrationWindow, self).__init__(parent)
        self.parent = parent
        self.site = site
        self.icon_position_x = tk.IntVar()
        self.icon_position_x.set(self.site.ICON_BROWSER_BUTTON[0])
        self.icon_position_y = tk.IntVar()
        self.icon_position_y.set(self.site.ICON_BROWSER_BUTTON[1])
        self.update_position_x = tk.IntVar()
        self.update_position_x.set(self.site.UPDATE_BUTTON_POSITION_COORDS[0])
        self.update_position_y = tk.IntVar()
        self.update_position_y.set(self.site.UPDATE_BUTTON_POSITION_COORDS[1])
        self.adv_position_x = tk.IntVar()
        self.adv_position_x.set(self.site.ADV_BUTTON_POSITION_COORDS[0])
        self.adv_position_y = tk.IntVar()
        self.adv_position_y.set(self.site.ADV_BUTTON_POSITION_COORDS[1])
        self.close_position_x = tk.IntVar()
        self.close_position_x.set(self.site.CLOSE_BUTTON_POSITION_COORDS[0])
        self.close_position_y = tk.IntVar()
        self.close_position_y.set(self.site.CLOSE_BUTTON_POSITION_COORDS[1])

        frame = tk.Frame(self)
        frame.grid(row=0, column=0, sticky=tk.NSEW)

        self.titleLabel = tk.Label(frame, text='Текущие координаты', anchor=tk.CENTER)
        self.xLabel = tk.Label(frame, text='X', anchor=tk.CENTER)
        self.yLabel = tk.Label(frame, text='Y', anchor=tk.CENTER)
        self.browserButton = tk.Button(frame, text='Иконка браузера', command=self.icon_browser_calibrate)
        self.browserXEntry = tk.Label(frame, textvariable=self.icon_position_x) 
        self.browserYEntry = tk.Label(frame, textvariable=self.icon_position_y)
        self.updateButton = tk.Button(frame, text='Кнопка обновления', command=self.update_calibrate)
        self.updateXEntry = tk.Label(frame, textvariable=self.update_position_x)
        self.updateYEntry = tk.Label(frame, textvariable=self.update_position_y)
        self.advButton = tk.Button(frame, text='Позиция рекламы', command=self.adv_calibrate)
        self.advXEntry = tk.Label(frame, textvariable=self.adv_position_x)
        self.advYEntry = tk.Label(frame, textvariable=self.adv_position_y)
        self.closeButton = tk.Button(frame, text='Кнопка закрытия', command=self.close_calibrate)
        self.closeXEntry = tk.Label(frame, textvariable=self.close_position_x)
        self.closeYEntry = tk.Label(frame, textvariable=self.close_position_y)
        self.okButton = tk.Button(frame, text='Ok', command=self.saveSettings, underline=0)
        self.cancelButton = tk.Button(frame, text='Cancel', command=self.cancel, underline=0)

        self.titleLabel.grid(row=0, column=2, columnspan=2, sticky=tk.EW)
        self.xLabel.grid(row=1, column=2, sticky=tk.EW)
        self.yLabel.grid(row=1, column=3, sticky=tk.EW)
        self.browserButton.grid(row=2, column=0, columnspan=2, sticky=tk.EW)
        self.browserXEntry.grid(row=2, column=2, sticky=tk.EW)
        self.browserYEntry.grid(row=2, column=3, sticky=tk.EW)
        self.updateButton.grid(row=3, column=0, columnspan=2, sticky=tk.EW)
        self.updateXEntry.grid(row=3, column=2, sticky=tk.EW)
        self.updateYEntry.grid(row=3, column=3, sticky=tk.EW)
        self.advButton.grid(row=4, column=0, columnspan=2, sticky=tk.EW)
        self.advXEntry.grid(row=4, column=2, sticky=tk.EW)
        self.advYEntry.grid(row=4, column=3, sticky=tk.EW)
        self.closeButton.grid(row=5, column=0, columnspan=2, sticky=tk.EW)
        self.closeXEntry.grid(row=5, column=2, sticky=tk.EW)
        self.closeYEntry.grid(row=5, column=3, sticky=tk.EW)
        self.okButton.grid(row=6, column=2, sticky=tk.EW)
        self.cancelButton.grid(row=6, column=3, sticky=tk.EW)

        self.wm_attributes('-topmost', True)
        self.protocol('WM_DELETE_WINDOW', self.cancel)
        self.grab_set()
        self.wait_window(self)
    def icon_browser_calibrate(self):
        form = CalibrationMessage(self, 'Наведите мышку на иконку браузера на панели быстрого доступа в нижней части экрана и нажмите Enter...', (self.icon_position_x, self.icon_position_y))

    def update_calibrate(self):
        form = CalibrationMessage(self, 'Наведите мышку на иконку обновления страницы браузера и нажмите Enter...', (self.update_position_x, self.update_position_y))

    def adv_calibrate(self):
        form = CalibrationMessage(self, 'Наведите мышку на блок рекламы (желательно чуть ниже верхней границы блока и чуть левее середины страницы) и нажмите Enter...', (self.adv_position_x, self.adv_position_y))

    def close_calibrate(self):
        form = CalibrationMessage(self, 'Наведите мышку на иконку закрытия вкладки браузера и нажмите Enter...', (self.close_position_x, self.close_position_y))

    def saveSettings(self):
        self.site.ICON_BROWSER_BUTTON = (self.icon_position_x.get(), self.icon_position_y.get())
        self.site.UPDATE_BUTTON_POSITION_COORDS = (self.update_position_x.get(), self.update_position_y.get())
        self.site.ADV_BUTTON_POSITION_COORDS  = (self.adv_position_x.get(), self.adv_position_y.get())
        self.site.CLOSE_BUTTON_POSITION_COORDS = (self.close_position_x.get(), self.close_position_y.get())
        self.site.write_config()
        self.cancel()

    def cancel(self, *ignore):
        self.parent.focus_set()
        self.destroy()

class CalibrationMessage(tk.Toplevel):
    """Окно калибровки опции конфига.

    parent - объект родитель
    message - сообщение, выводимое в окне (куда нужно навести мышь)
    coords_var - tuple(var_x, var_y) кортеж из двух переменных куда следует записать координаты
    """
    def __init__(self, parent, message, coords_var):
        super(CalibrationMessage, self).__init__(parent)
        self.parent = parent
        self.coords_var = coords_var
        self.focus_set()

        frame = tk.Frame(self, width=200, height=100)
        frame.grid(row=1, column=1, padx=20, pady=20, sticky=tk.NSEW)

        self.messageTitle = tk.Label(frame, text=message)
        self.messageTitle.grid(row=0, column=0, sticky=tk.NSEW)
        self.messageTitle.rowconfigure(0, pad=100)
        self.messageTitle.columnconfigure(0, pad=300)

        window = self.parent.winfo_toplevel()
        window.rowconfigure(0, weight=1)
        window.columnconfigure(0, weight=1)

        self.bind('<Return>', self.calibrate)
        self.bind('<Alt-z>', self.cancel)

        self.wm_attributes('-topmost', True)
        self.protocol('WM_DELETE_WINDOW', self.cancel)
        self.grab_set()
        self.wait_window()

    def calibrate(self, *ignore):
        coords = pag.position()
        self.coords_var[0].set(coords[0])
        self.coords_var[1].set(coords[1])
        self.cancel()

    def cancel(self, *ignore):
        self.parent.focus_set()
        self.destroy()

class TimeWindow(tk.Toplevel):
    def __init__(self, parent, site):
        super(TimeWindow, self).__init__(parent)
        self.parent = parent
        self.site = site

        self.time_to_wait_on_site_from = tk.IntVar()
        self.time_to_wait_on_site_from.set(self.site.TIME_TO_WAIT_ON_SITE[0])
        self.time_to_wait_on_site_to = tk.IntVar()
        self.time_to_wait_on_site_to.set(self.site.TIME_TO_WAIT_ON_SITE[1])
        self.break_time_from = tk.IntVar()
        self.break_time_from.set(self.site.BREAK_TIME[0])
        self.break_time_to = tk.IntVar()
        self.break_time_to.set(self.site.BREAK_TIME[1])
        self.delay_time = tk.IntVar()
        self.delay_time.set(self.site.DELAY_TIME)

        self.frame = tk.Frame(self)
        self.frame.grid(row=0, column=0, sticky=tk.NSEW)

        self.titleLable = tk.Label(self, text='Диапазон', anchor=tk.CENTER)
        self.fromLable = tk.Label(self, text='От', anchor=tk.CENTER)
        self.toLable = tk.Label(self, text='До', anchor=tk.CENTER)
        self.waitOnSiteLabel = tk.Label(self, text='Ожидание на сайте', anchor=tk.CENTER)
        self.waitOnSiteFromEntry = tk.Entry(self, textvariable=self.time_to_wait_on_site_from)
        self.waitOnSiteToEntry = tk.Entry(self, textvariable=self.time_to_wait_on_site_to)
        self.breakLabel = tk.Label(self, text='Перерыв', anchor=tk.CENTER)
        self.breakTimeFromEntry = tk.Entry(self, textvariable=self.break_time_from)
        self.breakTimeToEntry = tk.Entry(self, textvariable=self.break_time_to)
        self.delayLabel = tk.Label(self, text='Задержка перед действием', anchor=tk.CENTER)
        self.delayEntry = tk.Entry(self, textvariable=self.delay_time)
        self.okButton = tk.Button(self, text='Ok', command=self.saveSettings, underline=0)
        self.cancelButton = tk.Button(self, text='Cancel', command=self.cancel, underline=0)

        self.titleLable.grid(row=0, column=2, columnspan=2, sticky=tk.EW)
        self.fromLable.grid(row=1, column=2, sticky=tk.EW)
        self.toLable.grid(row=1, column=3, sticky=tk.EW)
        self.waitOnSiteLabel.grid(row=2, column=0, columnspan=2, sticky=tk.EW)
        self.waitOnSiteFromEntry.grid(row=2, column=2, sticky=tk.EW)
        self.waitOnSiteToEntry.grid(row=2, column=3, sticky=tk.EW)
        self.breakLabel.grid(row=3, column=0, columnspan=2, sticky=tk.EW)
        self.breakTimeFromEntry.grid(row=3, column=2, sticky=tk.EW)
        self.breakTimeToEntry.grid(row=3, column=3, sticky=tk.EW)
        self.delayLabel.grid(row=4, column=0, columnspan=2, sticky=tk.EW)
        self.delayEntry.grid(row=4, column=2, columnspan=2, sticky=tk.EW)
        self.okButton.grid(row=5, column=2, sticky=tk.EW)
        self.cancelButton.grid(row=5, column=3, sticky=tk.EW)

        self.protocol('WM_DELETE_WINDOW', self.cancel)
        self.grab_set()
        self.wait_window()

    def saveSettings(self, *ignore):
        if not self.time_to_wait_on_site_from.get() >= 180:
            tk.messagebox.showwarning('Error', 'Минимальное время "Ожидания на сайте": 180 секунд')
            return
        if not self.time_to_wait_on_site_to.get() >= self.time_to_wait_on_site_from.get() + 60:
            tk.messagebox.showwarning('Error', 'Правая граница диапазона "Ожидание на сайте" должна быть, как минимум, на 60 секунд больше левой.')
            return
        if not self.break_time_from.get() >= 1800:
            tk.messagebox.showwarning('Error', 'Минимальное время "Перерыва": 1800 секунд')
            return
        if not self.break_time_to.get() >= self.break_time_from.get() + 1800:
            tk.messagebox.showwarning('Error', 'Правая граница диапазона "Перерыв" должна быть, как минимум, на 1800 секунд больше левой.')
            return
        if not self.delay_time.get() >= 2:
            tk.messagebox.showwarning('Error', 'Минимальное время "Задержки перед действием": 2 секунды')
            return
        
        self.site.TIME_TO_WAIT_ON_SITE = (self.time_to_wait_on_site_from.get(), self.time_to_wait_on_site_to.get())
        self.site.BREAK_TIME = (self.break_time_from.get(), self.break_time_to.get())
        self.site.DELAY_TIME  = self.delay_time.get()
        self.site.write_config()
        self.cancel()

    def cancel(self, *ignore):
        self.parent.focus_set()
        self.destroy()

class LoginWindow():
    def __init__(self, parent):
        self.parent = parent
        self.login = tk.StringVar()
        self.login.set('login')
        self.password = tk.StringVar()
        self.password.set('password')

        frame = tk.Frame(self.parent)
        frame.grid(row=0, column=0, sticky=tk.NSEW)

        self.loginLable = tk.Label(frame, text='login', anchor=tk.E)
        self.loginEntry = tk.Entry(frame, textvariable=self.login)
        self.passwordLable = tk.Label(frame, text='password', anchor=tk.E)
        self.passwordEntry = tk.Entry(frame, textvariable=self.password)
        self.okButton = tk.Button(frame, text='Ok', command=self.confirm, underline=0)
        self.cancelButton = tk.Button(frame, text='Cancel', command=self.quit, underline=0)

        self.loginLable.grid(row=1, column=1, sticky=tk.NSEW)
        self.loginEntry.grid(row=1, column=2, sticky=tk.NSEW)
        self.passwordLable.grid(row=2, column=1, sticky=tk.NSEW)
        self.passwordEntry.grid(row=2, column=2, sticky=tk.NSEW)
        self.okButton.grid(row=4, column=1, sticky=tk.NSEW)
        self.cancelButton.grid(row=4, column=2, sticky=tk.NSEW)

        window=self.parent.winfo_toplevel()
        window.rowconfigure(0, weight=1)
        window.columnconfigure(0, weight=1)

        frame.rowconfigure(0, weight=1, pad=50)
        frame.rowconfigure(5, weight=1, pad=50)
        frame.columnconfigure(0, weight=1, pad=50)
        frame.columnconfigure(3, weight=1, pad=50)

    def confirm(self, *ignore):
        con, cur = None, None
        try:
            con = sql.connect(database='test', user=self.login.get(), password=self.password.get())
            cur = con.cursor()
            cur.execute("""SELECT * FROM logindata WHERE login=%s AND password=%s;""", (self.login.get(), self.password.get()))
            if cur.fetchone() is None:
                tk.messagebox.showwarning('Login', 'Вы ввели неправильную комбинацию логина и пароля\nПопробуйте снова')
            else:
                date_login = datetime.datetime.now().isoformat(timespec='seconds')
                cur.execute("""INSERT INTO loginrecord (login, date_login) VALUES (%s, %s)""", (self.login.get(), date_login))
                con.commit()
                site = Site()
                try:
                    site.get_config()
                except (KeyError, ValueError):
                    tk.messagebox.showwarning('Config', 'Отсутствует или поврежден конфиг-файл, создаем новый.')
                    site.make_configfile()
                window = MainWindow(self.parent, site, date_login, self.login.get(), self.password.get())

        except sql.DatabaseError as err:
            print(err)
            tk.messagebox.showwarning('DataBase', 'Ошибка базы данных.\nОбратитесь к разработчику')
        finally:
            if cur: cur.close()
            if con: con.close()

    def quit(self, *ignore):
        self.parent.destroy()
        sys.exit()



