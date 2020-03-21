import pyautogui as pag
import time
import random
import datetime
import configparser
import os

class Site():
    """Класс Site предназначен для работы с браузером посредством мышки и клавиатуры.
       Во время работы скрипта не рекомендуется выполнять какие либо действия, иначе программа может сбиться,
       и поребуется перезагрузка скрипта.

       В конце каждого метода гарантированно выполняется пауза, т.е. не обязательно заставлять программу ждать
       после каждого вызова метода класса.

    >>>site1 = Site()
    """
    def make_configfile(self, fh='config.txt'):
        config = configparser.ConfigParser()
        config['TIME_PARAMETERS'] = {}
        par = config['TIME_PARAMETERS']
        par['TIME_TO_WAIT_ON_SITE_FROM'] = str(180)
        par['TIME_TO_WAIT_ON_SITE_TO'] = str(360)
        par['BREAK_TIME_FROM'] = str(3600)
        par['BREAK_TIME_TO'] = str(5400)
        par['DELAY_TIME'] = str(2)

        config['POSITION_PARAMETERS'] = {}
        par = config['POSITION_PARAMETERS']
        par['ICON_BROWSER_BUTTON_X'] = str(1)
        par['ICON_BROWSER_BUTTON_Y'] = str(1)
        par['UPDATE_BUTTON_POSITION_COORDS_X'] = str(1)
        par['UPDATE_BUTTON_POSITION_COORDS_Y'] = str(1)
        par['ADV_BUTTON_POSITION_COORDS_X'] = str(1)
        par['ADV_BUTTON_POSITION_COORDS_Y'] = str(1)
        par['CLOSE_BUTTON_POSITION_COORDS_X'] = str(1)
        par['CLOSE_BUTTON_POSITION_COORDS_Y'] = str(1)

        config['BROWSER_PARAMETERS'] = {}
        par = config['BROWSER_PARAMETERS']
        par['SEARCH_PAGE'] = str(1)
        par['SITE_PAGE'] = str(2)

        try:
            os.remove('config.txt')
        except:
            pass
        with open(fh, 'w') as fh:
            config.write(fh)

    def get_config(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.txt')

        par = self.config['TIME_PARAMETERS']
        self.TIME_TO_WAIT_ON_SITE = (int(par['TIME_TO_WAIT_ON_SITE_FROM']), int(par['TIME_TO_WAIT_ON_SITE_TO']))
        self.DELAY_TIME = int(par['DELAY_TIME'])
        self.BREAK_TIME = (int(par['BREAK_TIME_FROM']), int(par['BREAK_TIME_TO']))

        par = self.config['POSITION_PARAMETERS']
        self.ICON_BROWSER_BUTTON = (int(par['ICON_BROWSER_BUTTON_X']), int(par['ICON_BROWSER_BUTTON_Y']))
        self.UPDATE_BUTTON_POSITION_COORDS = (int(par['update_button_position_coords_x']), int(par['update_button_position_coords_y']))
        self.ADV_BUTTON_POSITION_COORDS = (int(par['ADV_BUTTON_POSITION_COORDS_X']), int(par['ADV_BUTTON_POSITION_COORDS_Y']))
        self.CLOSE_BUTTON_POSITION_COORDS = (int(par['close_button_position_coords_x']), int(par['close_button_position_coords_y']))

        par = self.config['BROWSER_PARAMETERS']
        self.SEARCH_PAGE = int(par['SEARCH_PAGE'])
        self.SITE_PAGE = int(par['SITE_PAGE'])

    def write_config(self, fh='config.txt'):
        par = self.config['TIME_PARAMETERS']
        par['TIME_TO_WAIT_ON_SITE_FROM'] = str(self.TIME_TO_WAIT_ON_SITE[0])
        par['TIME_TO_WAIT_ON_SITE_TO'] = str(self.TIME_TO_WAIT_ON_SITE[1])
        par['BREAK_TIME_FROM'] = str(self.BREAK_TIME[0])
        par['BREAK_TIME_TO'] = str(self.BREAK_TIME[1])
        par['DELAY_TIME'] = str(self.DELAY_TIME)

        par = self.config['POSITION_PARAMETERS']
        par['ICON_BROWSER_BUTTON_X'] = str(self.ICON_BROWSER_BUTTON[0])
        par['ICON_BROWSER_BUTTON_Y'] = str(self.ICON_BROWSER_BUTTON[1])
        par['UPDATE_BUTTON_POSITION_COORDS_X'] = str(self.UPDATE_BUTTON_POSITION_COORDS[0])
        par['UPDATE_BUTTON_POSITION_COORDS_Y'] = str(self.UPDATE_BUTTON_POSITION_COORDS[1])
        par['ADV_BUTTON_POSITION_COORDS_X'] = str(self.ADV_BUTTON_POSITION_COORDS[0])
        par['ADV_BUTTON_POSITION_COORDS_Y'] = str(self.ADV_BUTTON_POSITION_COORDS[1])
        par['CLOSE_BUTTON_POSITION_COORDS_X'] = str(self.CLOSE_BUTTON_POSITION_COORDS[0])
        par['CLOSE_BUTTON_POSITION_COORDS_Y'] = str(self.CLOSE_BUTTON_POSITION_COORDS[1])

        par = self.config['BROWSER_PARAMETERS']
        par['SEARCH_PAGE'] = str(self.SEARCH_PAGE)
        par['SITE_PAGE'] = str(self.SITE_PAGE)

        with open(fh, 'w') as fh:
            self.config.write(fh)

    def click_browser_icon(self, ICON_BROWSER_BUTTON):
        """Метод кликает по иконке браузера на панели быстрого доступа.
           Можно использовать для открытия или закрытия браузера.

        ICON_BROWSER_BUTTON - tuple object, внутри которого для i=0 записана координата по X,
                                            а для i=1 по Y распоожения иконки браузера.

        >>>site1.click_browser_icon((300, 300))
        """
        pag.click(ICON_BROWSER_BUTTON)
        time.sleep(self.DELAY_TIME)

    def go_to_site(self, site_page):
        """Метод переходит в окно, номер которого передан в качестве аргумента.

        site_page - int object номер окна браузера

        >>>site1.go_to_site(1)
        >>>Переходим на 1 сайт
        """
        print('Переходим на %s сайт' %(site_page))
        pag.hotkey('ctrl', '%s' %(site_page, ))
        pag.sleep(self.DELAY_TIME)

    def adv_working(self, ADV_BUTTON_POSITION_COORDS, scrolling=True, logging=False):
        """Метод кликает по рекламе, координаты которой передаются в качестве аргумента.

        ADV_BUTTON_POSITION_COORDS - tuple object, внутри которого для i=0 записана координата по X,
                                                   а для i=1 по Y распоожения рекламы в окне.

        Доступны необязательные аргументы:
            scrolling - для того, чтобы скроллить открываемый рекламой сайт. True - по умолчанию
            logging - для того, чтобы записывать время клика в лог файл. True - по умолчанию

        >>>site1.adv_working((300, 300))
        >>>Работаем:
        """
        print('Работаем:')
        pag.moveTo(ADV_BUTTON_POSITION_COORDS)
        pag.click(ADV_BUTTON_POSITION_COORDS)
        if logging:
            self.log_to_file('Клик')
        time.sleep(self.DELAY_TIME)
        if scrolling:
            self.scrolling()

    def scrolling(self, X=300, Y=300, scroll_amount=(2, 5), sleep_between_scrolling=(1, 10), scroll_down=(500, 1000), scroll_up=(500, 1000)):
        """Метод скроллит сайт.

        Доступны необязательные аргументы:
            X - координата перемещения мышки. 300 - По умолчанию
            Y - координата перемещения мышки. 300 - По умолчанию
            scroll_amount - tuple(from, to) количество циклов скролла сайта, число выбирается случайно от from до to
                            (2, 5) - по умолчанию
            sleep_between_scrolling - tuple(from, to) сколько секунд ждять между скроллом, число выбирается случайно от from до to
                                      (1, 10) - по умолчанию
            scroll_down - tuple(from, to) на какое число пикселей скроллить вниз, число выбирается случайно от from до to
                          (500, 1000) - по умолчанию
            scroll_up - tuple(from, to) на какое число пикселей скроллить вверх, число выбирается случайно от from до to
                        (500, 1000) - по умолчанию

        >>>site1.adv_working((300, 300))
        >>>Работаем:
        """
        pag.moveTo(x=X, y=Y)
        scroll = random.randint(scroll_amount[0], scroll_amount[1])
        print('Скроллим сайт %s раз...' %(scroll,))
        for i in range(scroll):
            for j in range(random.randint(5, 10)): 
                pag.scroll(random.randint(50, 300))
            time.sleep(random.randint(sleep_between_scrolling[0], sleep_between_scrolling[1]))
            for j in range(random.randint(5, 10)):
                pag.scroll(-(random.randint(50, 200)))
            time.sleep(random.randint(sleep_between_scrolling[0], sleep_between_scrolling[1]))

    def wait(self, TIME_TO_WAIT_ON_SITE, console=True, logging=False, countdown=True, countdown_range=(30, 0, -1)):
        """Метод просто ждет переданное в качестве аргумента время.

        TIME_TO_WAIT_ON_SITE - tuple(from, to) 

        Доступны необязательные аргументы:
            console - для того, чтобы вывести в консоль время начала ожидания. True - по умолчанию
            logging - для того, чтобы записывать время клика в лог файл. True - по умолчанию
            countdown - для того, чтобы вывести в консоль обратный отсчет до конца ожидания. True - по умолчанию
            countdown_range - tuple(start, end, step) - параметры обратного отсчета. (30, 0, -1) - по умолчанию

        >>>site1.wait((300, 600))
        """
        rand_time = random.randint(TIME_TO_WAIT_ON_SITE[0], TIME_TO_WAIT_ON_SITE[1] - countdown_range[0])
        if logging:
            self.log_to_file('Ждём на сайте %s секунд' %(rand_time))
        if console:
            print('Начало ожидания: %s\n\tЖдём на сайте %s секунд' %(datetime.datetime.now().isoformat(timespec='seconds'), rand_time))
        time.sleep(rand_time)
        if countdown:
            print('До конца ожидания осталось:')
            for i in range(countdown_range[0], countdown_range[1], countdown_range[2]):
                print('\t%s' %(i))
                time.sleep(1)

    def site_closing(self, CLOSE_BUTTON_POSITION_COORDS):
        """Метод просто закрывает текущий сайт по кнопке закрытия, координаты которой переданы в качестве аргумента.

        CLOSE_BUTTON_POSITION_COORDS - tuple(X, Y) координаты иконки закрытия окна

        >>>site1.site_closing()
        >>>Закрываем сайт

        """
        print('Закрываем сайт')
        pag.moveTo(CLOSE_BUTTON_POSITION_COORDS[0], CLOSE_BUTTON_POSITION_COORDS[1])
        time.sleep(self.DELAY_TIME)
        pag.click(CLOSE_BUTTON_POSITION_COORDS[0], CLOSE_BUTTON_POSITION_COORDS[1])
        time.sleep(DELAY_TIME)

    def log_to_file(self, message):
        """Метод записывает message в лог файл под текущей датой.

        message - str сообщение для записи
        """
        fh = 'log_%s.txt' %(datetime.date.today().isoformat())
        try:
            with open(fh, 'a'): pass
        except FileExistsError:
            with open(fh, 'w'): pass
        with open(fh, 'a') as fh:
            fh.write('{0}:\t{1}'.format(datetime.datetime.now().isoformat(timespec='seconds'), message))

    def calibration(self, message, option, fh='config.txt', console=True):
        """Метод записывает координаты мыши в момент, когда программа просит это сделать.

        message - str сообщение, выводимое пользователю
        config_block_title - str Блок в конфиг файле, в котором находится соответствующий конфиг
        option - str Название конфига под который нужно записать координаты

        Доступны необязательные аргументы:
            fh - str название конфиг файла. config.txt - по умолчанию
            console - для того, чтобы вывести в консоль время начала ожидания. True - по умолчанию

        >>>site1.calibration('Наведите мышку на иконку браузера и нажмите Enter...', 'POSITION_PARAMETERS', 'ICON_BROWSER_BUTTON')
        >>>.
        >>>.
        >>>.
        >>>Ваши координаты 300, 300 успешно записаны в конфигурационный файл.
        >>>'Нажмите любую кнопку, чтобы закрыть окно.
        """
        with open(fh, 'r'): pass
        if console:
            ignore = input(message)
        coords = pag.position()
        exec('''self.{0} = (coords[0], coords[1])''')
        if console:
            for i in range(3):
                print('.')
                time.sleep(0.5)
            print('Конфиг обновлен, не забудьте записать его в файл.\n'.format(coords))
            ignore = input('Нажмите любую кнопку, чтобы закрыть окно.')

