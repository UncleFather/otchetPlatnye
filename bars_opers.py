from initials import mis_url, mis_username, mis_password

from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime as dt, timedelta as tdl


# Функция формирования отчета с текущей датой
def send_form(driver, curr_date):
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


def main_bars(days_depth=45, days_step=2):
    # Устанавливаем константы с учетными данными
    username = mis_username
    password = mis_password
    # Инициализируем драйвер Google Chrome
    driver = webdriver.Chrome("chromedriver")
    # Переходим на страницу входа на сайт
    driver.get(mis_url)
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

    # Парсим страничку, на предмет нахождения на ней всплывающих сообщений и закрываем их
    try:
        driver.find_element(By.LINK_TEXT, 'Закрыть все').click()
    except Exception:
        pass

    # Парсим страничку, находим нужные пункты меню и кликаем по ним
    driver.find_element(By.LINK_TEXT, 'Учет').click()
    driver.find_element(By.LINK_TEXT, 'Учет медицинских свидетельств').click()
    driver.find_element(By.LINK_TEXT, 'Журнал выданных свидетельств').click()

    # Ждем 2 секунды
    sleep(2)

    # Получаем сегодняшнюю дату
    curr_date = dt.now()
    # Получаем дату ранее текущей на 45 дней
    delta_date = curr_date - tdl(days=days_depth)
    # Перебираем все диапазоны внутри заданных дат
    while curr_date >= delta_date:
        # Вызываем функцию формирования отчета с текущей датой
        send_form(driver, curr_date)
        # Уменьшаем значение текущей даты на два дня (так как более широкий промежуток может привести к ошибке в Барсе)
        curr_date = curr_date - tdl(days=days_step)
