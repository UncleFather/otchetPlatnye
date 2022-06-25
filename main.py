from initials import reports

from xlsx_opers import prepare_strings, save_xlsx
from bd_opers import bd_prepare, bd_report
from bars_opers import main_bars
from smtp_opers import send_mail

from datetime import datetime as dt


# Задаем имя файла отчета
xlsx_filename = f'Otchet_Date_{dt.now():%Y.%m.%d}.xlsx'

# Выполняем запросы в МИС «Барс» на глубину days_depth дней с шагом days_step дней
#main_bars(days_depth=45, days_step=2)
# Собираем полученные данные из xlsx файлов выгрузок в один массив strings_to_add
strings_to_add = prepare_strings()
# Добавляем в БД полученный массив с данными
bd_prepare(strings_to_add)
# Для каждого отчета из массива reports
for item in reports:
    # Делаем запрос к БД и получаем строки с данными в массив strings_to_add
    strings_to_add = bd_report(item)
    # Сохраняем полученный массив на соответсвующий лист файла итогового отчета xlsx
    save_xlsx(xlsx_filename, item, strings_to_add)
# Отправляем полученный файл итогового отчета по электронной почте
send_mail(xlsx_filename)