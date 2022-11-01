from initials import mis_url, mis_username, mis_password, mis_days_depth, mis_days_step

from txt_opers import log_write

from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime as dt, timedelta as tdl


# Функция формирования отчета с текущей датой
def send_form(driver, curr_date):
    delta_date = curr_date - tdl(days=mis_days_step)
    # Инициализируем переменную, указывающую количество отступов для файла отчета
    indention = 6
    # Парсим форму, находим поле ввода даты начала отчета
    datefield_B = driver.find_element(By.ID, "_mainContainer").find_element(By.NAME, "DATE_B").find_element(
        By.CLASS_NAME, "input-ctrl")
    # Очищаем поле
    datefield_B.clear()
    # Инициализируем поле (иначе не получится ввести дату)
    datefield_B.click()
    # Вводим дату начала отчета, ранее текущей на два дня
    datefield_B.send_keys(f'{delta_date:%d%m%Y}')
    log_write(f'Установлена дата начала отчета {delta_date:%d.%m.%Y}', indention)

    # Парсим форму, находим поле ввода даты окончания отчета
    datefield_E = driver.find_element(By.ID, "_mainContainer").find_element(By.NAME, "DATE_E").find_element(
        By.CLASS_NAME, "input-ctrl")
    # Очищаем поле
    datefield_E.clear()
    # Инициализируем поле (иначе не получится ввести дату)
    datefield_E.click()
    # Вводим дату окончания отчета, равную текущей
    datefield_E.send_keys(f'{curr_date:%d%m%Y}')
    log_write(f'Установлена дата окончания отчета {curr_date:%d.%m.%Y}', indention)

    '''
    # Закомментировано в связи с оптимизацией запросов к МИС «Барс»
    # Находим на форме кнопку формирования отчета и кликаем по ней
    driver.find_element(By.ID, "_mainContainer").find_element(By.CSS_SELECTOR, ".btnc").click()
    log_write(f'Запущено формирование отчета', indention)

    # Ждем 30 секунд
    sleep(30)'''

    # Находим на форме кнопку выгрузки отчета в xlsx файл и кликаем по ней
    driver.find_element(By.ID, "_mainContainer").find_element(By.CLASS_NAME, 'excel-button').click()
    log_write(f'Скачиваем отчет', indention)

    # Ждем 20 секунд
    sleep(20)

    # Возвращаем новую дату начала следующего отчета
    return delta_date


def main_bars():
    # Инициализируем переменную, указывающую количество отступов для файла отчета
    indention = 4
    # Устанавливаем константы с учетными данными
    username = mis_username
    password = mis_password
    # Инициализируем драйвер Google Chrome
    driver = webdriver.Chrome("chromedriver")
    log_write(f'Открыт экземпляр Google Chrome', indention)
    # Переходим на страницу входа на сайт
    driver.get(mis_url)
    log_write(f'Выполнен переход на страницу входа на сайт', indention)
    # Устанавливаем размер окна открывшегося экземпляра браузера
    driver.set_window_size(1561, 1060)

    # Парсим страничку входа. Находим поле для ввода имени пользователя и записываем в него имя
    #driver.find_element(By.NAME, "DBLogin").find_element(By.CLASS_NAME, "input-ctrl").send_keys(username)
    driver.find_element(By.NAME, "DBLogin").find_elements(By.XPATH, "//input[@cmpparse='Edit']")[0].send_keys(username)
    log_write(f'Введено имя пользователя', indention)
    # Находим поле для ввода пароля и записываем в него пароль
    #driver.find_element(By.NAME, "DBPassword").find_element(By.CLASS_NAME, "input-ctrl").send_keys(password)
    driver.find_element(By.NAME, "DBPassword").find_elements(By.XPATH, "//input[@cmpparse='Edit']")[1].send_keys(
        password)
    log_write(f'Введен пароль пользователя', indention)
    # Находим кнопку отправки и нажимаем ее
    #driver.find_element(By.CLASS_NAME, "bt").click()
    driver.find_element(By.CLASS_NAME, "btn_caption").click()
    log_write(f'Инициирован процесс авторизации в МИС «Барс»', indention)

    # Ждем 3 секунды
    sleep(3)
    # Подтверждаем организацию и кабинет (находим кнопку и кликаем по ней)
    #driver.find_element(By.CLASS_NAME, "bt").click()
    driver.find_element(By.CLASS_NAME, "btn_caption").click()
    log_write(f'Подтвержден кабинет и ЛПУ', indention)

    # Ждем 4 секунды
    sleep(4)

    # Парсим страничку, на предмет нахождения на ней всплывающих сообщений и закрываем их
    try:
        driver.find_element(By.LINK_TEXT, 'Закрыть все').click()
    except Exception:
        indention = 6
        log_write(f'ВНИМАНИЕ!!! Новые сообщения в МИС «Барс»', indention)
        indention = 4

    # Парсим страничку, находим нужные пункты меню и кликаем по ним
    driver.find_element(By.LINK_TEXT, 'Учет').click()
    log_write(f'Выбран пункт меню «Учет»', indention)
    driver.find_element(By.LINK_TEXT, 'Учет медицинских свидетельств').click()
    log_write(f'Выбран пункт меню «Учет медицинских свидетельств»', indention)
    driver.find_element(By.LINK_TEXT, 'Журнал выданных свидетельств').click()
    log_write(f'Выбран пункт меню «Журнал выданных свидетельств»', indention)

    # Ждем 4 секунды
    sleep(4)

    # Получаем сегодняшнюю дату
    curr_date = dt.now()
    # Получаем дату ранее текущей на 45 дней
    delta_date = curr_date - tdl(days=mis_days_depth)
    # Перебираем все диапазоны внутри заданных дат
    while curr_date >= delta_date:
        # Вызываем функцию формирования отчета с текущей датой
        log_write(f'Процедура формирования файла выгрузки с {(curr_date - tdl(days=mis_days_step)):%d.%m.%Y} '
                  f'по {curr_date:%d.%m.%Y}', indention)
        # Из функции получаем новое значение начальной даты для следующего отчета
        curr_date = send_form(driver, curr_date)

