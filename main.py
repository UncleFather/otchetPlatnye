from initials_common import reports

from xlsx_opers import prepare_strings, save_xlsx
from bd_opers import bd_prepare, bd_report
from bars_opers import main_bars
from smtp_opers import send_mail
from txt_opers import log_write

from datetime import datetime as dt
from atexit import register
import sys


# Класс для обработки события выхода из программы
class ExitHooks(object):
    # Инициализируем конструктор объектов класса
    def __init__(self):
        self.exit_code = None
        self.exception = None

    # Описываем метод hook, возникающий при генерации исключения, в том числе и выхода из программы
    def hook(self):
        self._orig_exit = sys.exit
        sys.exit = self.exit
        sys.excepthook = self.exc_handler

    # Описываем метод exit, получающий код исключения
    def exit(self, code=0):
        self.exit_code = code
        self._orig_exit(code)

    # Описываем метод exc_handler, получающий описание исключения
    def exc_handler(self, exc_type, exc, *args):
        self.exception = exc


# Процедура обработки выхода из программы
def exit_proc():
    # Инициализируем текстовую переменную значением, возникающем при генерации исключения
    mes_txt = f'{"*" * 18} В процессе генерации отчета от {curr_date:%Y.%m.%d} возникли ошибки ' \
              f'(время окончания {dt.now():%H:%M:%S}) {"*" * 18}'
    # Если возникло исключение с кодом, отличным от нуля
    if hooks.exit_code is not None and hooks.exit_code != 0:
        # Добавляем к тексту сообщения код сгенерированного исключения
        mes_txt = f'{"!" * 8 } Возникло исключение с кодом {hooks.exit_code} {"!" * 8 }\n{mes_txt}'
    # Если возникло исключение с непустым описанием
    elif hooks.exception is not None:
        # Добавляем к тексту сообщения описание сгенерированного исключения
        mes_txt = f'{"!" * 8} Возникло исключение: {hooks.exception} {"!" * 8}\n{mes_txt}'
    # Если у исключения отсутствует описание и код либо отсутствует, либо равен нулю
    else:
        # Переписываем текст выводимого сообщения
        mes_txt = f'{"*" * 22} Успешное окончание генерации отчета от {curr_date:%Y.%m.%d} (время ' \
                  f'окончания {dt.now():%H:%M:%S}) {"*" * 22}'
    # Записываем сообщение в журнал
    log_write(mes_txt)

# Инициализируем переменную класса ExitHooks для получения кода сгенерированного исключения
hooks = ExitHooks()
# Вызываем метод получения сгенерированного исключения
hooks.hook()

# Инициализируем процедуру обработки выхода из программы, в том числе при возникновении ошибки
register(exit_proc)
# Инициализируем переменную с текущей датой
curr_date = dt.now()
# Инициализируем переменную, указывающую количество отступов для файла отчета
indention = 2
# Задаем имя файла отчета
xlsx_filename = f'Otchet_Date_{curr_date:%Y.%m.%d}.xlsx'
# Записываем время начала в журнал
log_write(f'{"*" * 30} Начало генерации отчета от {curr_date:%Y.%m.%d} время начала {curr_date:%H:%M:%S}) '
          f'{"*" * 30}')
# Выполняем запросы в МИС «Барс» на глубину days_depth дней с шагом days_step дней
log_write(f'Отправка запросов в МИС «Барс» и получение файлов выгрузок', indention)
main_bars(days_depth=45, days_step=2)
# Собираем полученные данные из xlsx файлов выгрузок в один массив strings_to_add
log_write(f'Процедура подготовки строк для добавления в БД', indention)
strings_to_add = prepare_strings()
# Добавляем в БД полученный массив с данными
log_write(f'Процедура добавления строк в БД', indention)
bd_prepare(strings_to_add)
# Для каждого отчета из массива reports
for item in reports:
    # Делаем запрос к БД и получаем строки с данными в массив strings_to_add
    log_write(f'Получаем отчет {item}', indention)
    strings_to_add = bd_report(item)
    # Сохраняем полученный массив на соответсвующий лист файла итогового отчета xlsx
    log_write(f'Сохраняем отчет {item} в файл {xlsx_filename}', indention)
    save_xlsx(xlsx_filename, item, strings_to_add)
# Отправляем полученный файл итогового отчета по электронной почте
log_write(f'Отправляем итоговый файл отчета {item}', indention)
send_mail(xlsx_filename)
exit(0)
