from initials import file_paths, file_mask, needed, titles, etalon, reports

from txt_opers import writing_etalon

from datetime import datetime as dt, time
from openpyxl import Workbook as wkb, load_workbook as ld_wb
from pathlib import Path


def format_etalon_string(captions):
    etalon_str = ['']
    i = 0
    for item in captions:
        etalon_str[i] += "'" + item + "', "
        if len(etalon_str[i]) > 80 and captions.index(item) < len(captions) - 1:
            i += 1
            etalon_str.append(" " * 12)
    etalon_str[i] = etalon_str[i][:-2]
    new_line = '\n'
    return f'etalon = [{new_line.join(etalon_str)}]\n'


def remap_positions(captions):
    global needed_pos

    for i in range(len(captions)):
        tmp_var = captions[i]
        if tmp_var in needed:
            needed_pos[needed.index(tmp_var)] = i


def file_structure_check(file, row):
    global etalon

    captions = list(i.value for i in row)
    if etalon != captions:
        if set(needed).issubset(set(captions)):
            print(f'Некритичные изменения структуры файла выгрузки {file}')
            writing_etalon(format_etalon_string(captions))
            etalon = captions
        else:
            print(f'Внимание!!! Критичные изменения структуры файла выгрузки {file}')
            exit(0)

    remap_positions(captions)


def prepare_strings():
    global needed_pos
    needed_pos = [-1] * 10
    # Получаем список всех файлов выгрузок
    paths = Path(file_paths).glob(file_mask)

    curr_sheet = []
    # Перебираем все файлы в списке файлов выгрузок
    for file in paths:
        # Открываем текущий файл
        wb = ld_wb(filename=file)
        # Выбираем первый лист рабочей книги
        sheet = wb.worksheets[0]
        file_structure_check(file, sheet[2])

        # Читаем все строки листа
        for row in sheet.rows:
            # Нас интересуют только строки, где в первом столбце стоит целое число - номер трупа
            if type(row[needed_pos[0]].value) == int:
                curr_row = []
                # Перебираем только нужные нам ячейки из текущей строки
                for cell_num in needed_pos:
                    # Создаем временную переменную для хранения значения текущей ячейки
                    tmp_val = row[cell_num].value
                    # Если тип значения ячейки дата
                    if type(tmp_val) == dt:
                        # Если время в дате установлено 00:00:00
                        if tmp_val.time() == time(0, 0, 0):
                            # Конвертируем временную переменную в строку в формате ДД.ММ.ГГГГ для соответствия
                            # ранее введенным датам
                            tmp_val = tmp_val.strftime("%d.%m.%Y")
                        # Если время в дате не равно нулю
                        else:
                            # Конвертируем временную переменную в строку в формате ДД.ММ.ГГГГ ЧЧ:ММ для соответствия
                            # ранее введенным датам
                            tmp_val = tmp_val.strftime("%d.%m.%Y %H:%M")
                    #
                    curr_row.append(tmp_val)
                #
                curr_sheet.append(curr_row)
    # otchet_platnyedate, without_platnye_date, kosyak_podrobno
    return curr_sheet


def save_xlsx(xlsx_filename, report_name, strings_to_add):
    #rows = make_query()
    if report_name == reports[0]:
        wb_w = wkb()
        sheet_w = wb_w.worksheets[0]
        sheet_w.title = report_name

    else:
        wb_w = ld_wb(filename=xlsx_filename)
        sheet_w = wb_w.create_sheet(report_name)

    pos_titles = 1 if report_name == reports[1] else 0
    sheet_w.append(titles[pos_titles])
    for row in strings_to_add:
        sheet_w.append(row)

    wb_w.save(xlsx_filename)
