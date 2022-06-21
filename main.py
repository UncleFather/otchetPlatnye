from datetime import datetime as dt, timedelta as tdl, time
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from openpyxl import Workbook as wb, load_workbook as ld_wb
from pathlib import Path
from selenium.webdriver.common.action_chains import ActionChains


# Функция формирования отчета с текущей датой
def send_form(curr_date):
    # Парсим форму, находим поле ввода даты начала отчета
    datefield_B = driver.find_element(By.ID, "_mainContainer").find_element(By.NAME, "DATE_B").find_element(
        By.CLASS_NAME, "input-ctrl")
    # Очищаем поле
    datefield_B.clear()
    # Инициализируем поле (иначе не получится ввести дату)
    datefield_B.click()
    # Вводим дату начала отчета, ранее текущей на два дня
    datefield_B.send_keys(f'{curr_date - tdl(days=2):%d%m%Y}')

    # Парсим форму, находим поле ввода даты окончания отчета
    datefield_E = driver.find_element(By.ID, "_mainContainer").find_element(By.NAME, "DATE_E").find_element(
        By.CLASS_NAME, "input-ctrl")
    # Очищаем поле
    datefield_E.clear()
    # Инициализируем поле (иначе не получится ввести дату)
    datefield_E.click()
    # Вводим дату окончания отчета, равную текущей на два дня
    datefield_E.send_keys(f'{curr_date:%d%m%Y}')

    # Находим на форме кнопку формирования отчета и кликаем по ней
    driver.find_element(By.ID, "_mainContainer").find_element(By.CSS_SELECTOR, ".btnc").click()

    # Ждем 30 секунд
    sleep(30)

    # Находим на форме кнопку выгрузки отчета в xlsx файл и кликаем по ней
    driver.find_element(By.ID, "_mainContainer").find_element(By.CLASS_NAME, 'excel-button').click()

    # Ждем 20 секунд
    sleep(20)


# Устанавливаем константы с учетными данными
username = "ADMIN435"
password = "Xj,FlvbyGfcc123"
# Инициализируем драйвер Google Chrome
driver = webdriver.Chrome("chromedriver")

# Переходим на страницу входа на сайт
driver.get("http://10.31.6.59/inst")
# Устанавливаем размер окна открывшегося экземпляра браузера
driver.set_window_size(1561, 1060)

# Парсим страничку входа. Находим поле для ввода имени пользователя и записываем в него имя
driver.find_element(By.NAME, "DBLogin").find_element(By.CLASS_NAME, "input-ctrl").send_keys(username)
# Находим поле для ввода пароля и записываем в него пароль
driver.find_element(By.NAME, "DBPassword").find_element(By.CLASS_NAME, "input-ctrl").send_keys(password)
# Находим кнопку отправки и нажимаем ее
driver.find_element(By.CLASS_NAME, "bt").click()

# Ждем 3 секунды
sleep(3)
# Подтверждаем организацию и кабинет (находим кнопку и кликаем по ней)
driver.find_element(By.CLASS_NAME, "bt").click()

# Ждем 3 секунды
sleep(3)
# Парсим страничку, находим нужные пункты меню и кликаем по ним
driver.find_element(By.LINK_TEXT, 'Учет').click()
driver.find_element(By.LINK_TEXT, 'Учет медицинских свидетельств').click()
driver.find_element(By.LINK_TEXT, 'Журнал выданных свидетельств').click()

# Ждем 2 секунды
sleep(2)

# Получаем сегодняшнюю дату
curr_date = dt.now()
# Получаем дату ранее текущей на 45 дней
delta_date = curr_date - tdl(days=45)
# Перебираем все диапазоны внутри заданных дат
while curr_date >= delta_date:
    # Вызываем функцию формирования отчета с текущей датой
    send_form(curr_date)
    # Уменьшаем значение текущей даты на два дня (так как более широкий промежуток может привести к ошибке в Барсе)
    curr_date = curr_date - tdl(days=2)

# Получаем отсортированный список всех файлов выгрузок так, чтобы первым в списке был 'Журнал выданных свидетельств.xlsx',
# так как именно на него настроен импорт в Access
paths = sorted(Path('C:\\Users\\Manaeff\\Downloads\\').glob('Журнал выданных свидетельств*.xlsx'), reverse=True)

# paths = ['C:\\Users\\Manaeff\\Downloads\\Журнал выданных свидетельств.xlsx', 'C:\\Users\\Manaeff\\Downloads\\Журнал выданных свидетельств (1).xlsx']
# print(paths)
# wb_w = ld_wb(filename = 'C:\\Users\\Manaeff\\Downloads\\Лист Microsoft Excel.xlsx')
# sheet_w = wb_w.worksheets[0]
# В первый файл (сделаем его файлом вывода) списка будем дописывать все данные
filepath = paths[0]
# Создаем объект "Workbook" (Рабочая книга)
wb_w = wb()
# Выбираем первый лист рабочей книги
sheet_w = wb_w.worksheets[0]

# Инициализируем счетчик строк в файле вывода
curr_row = 1
# Перебираем все файлы в списке файлов выгрузок
for file in paths:
    # Открываем текущий файл
    wb = ld_wb(filename=file)
    # Выбираем первый лист рабочей книги
    sheet = wb.worksheets[0]
    # Читаем все строки листа
    for v in sheet.rows:
        # Нас инетерсуют только строки, где в первом столце стоит целое число - номер трупа
        # либо строка первого файла из списка, где в первом столбце стоит значение 'Номер свидетельства' для того,
        # чтобы сформировать заголовки столбцов в файле вывода
        if type(v[0].value) == int or (file == filepath and v[0].value == 'Номер свидетельства'):
            # Инициализируем счетчик столбцов в текущей строке
            curr_column = 1
            # Перебираем все ячейки в текущей строке
            for x in v:
                # Создаем временную переменную для хранения значения текущей ячейки
                tmp_val = x.value
                # Если тип значения ячейки дата
                if type(tmp_val) == dt:
                    # Если время в дате установлено 00:00:00
                    if (tmp_val).time() == time(0, 0, 0):
                        # Конвертируем временную переменную в строку в формате ДД.ММ.ГГГГ для Access
                        tmp_val = tmp_val.strftime("%d.%m.%Y")
                    # Если время в дате не равно нулю
                    else:
                        # Конвертируем временную переменную в строку в формате ДД.ММ.ГГГГ ЧЧ:ММ для Access
                        tmp_val = tmp_val.strftime("%d.%m.%Y %H:%M")
                # Записываем значение в ячейку листа рабочей книги файла вывода
                sheet_w.cell(row=curr_row, column=curr_column).value = tmp_val
                # Переходим на следующую колонку
                curr_column += 1
            # Переходим на следующую строку
            curr_row += 1
    # Записываем файл вывода
    wb_w.save(filepath)
