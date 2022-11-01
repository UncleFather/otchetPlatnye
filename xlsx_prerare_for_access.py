from initials_common import file_paths, file_mask

from datetime import datetime as dt, time
from openpyxl import Workbook as wkb, load_workbook as ld_wb
from pathlib import Path


def main_xlsx_prepare():
    # Получаем отсортированный список всех файлов выгрузок так, чтобы первым в списке был 'Журнал выданных
    # свидетельств.xlsx', так как именно на него настроен импорт в Access
    paths = sorted(Path(file_paths).glob(file_mask), reverse=True)

    # В первый файл (сделаем его файлом вывода) списка будем дописывать все данные
    filepath = paths[0]
    # Создаем объект "Workbook" (Рабочая книга)
    wb_w = wkb()
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
            # Нас интересуют только строки, где в первом столбце стоит целое число - номер трупа
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
