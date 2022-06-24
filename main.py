from initials import reports

from xlsx_opers import prepare_strings, save_xlsx
from bd_opers import bd_prepare, bd_report
from bars_opers import main_bars
from smtp_opers import send_mail

from datetime import datetime as dt


xlsx_filename = f'Otchet_Date_{dt.now():%Y.%m.%d}.xlsx'

#main_bars(days_depth=45, days_step=2)
strings_to_add = prepare_strings()
bd_prepare(strings_to_add)
for item in reports:
    strings_to_add = bd_report(item)
    save_xlsx(xlsx_filename, item, strings_to_add)
send_mail(xlsx_filename)