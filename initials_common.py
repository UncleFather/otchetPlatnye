# ************* MIS Bars Connection *************
mis_username = "user"
mis_password = "PasSWorD"
mis_url = "http://11.11.11.11/path"

# ************* DataBase Connection *************
db_host = 'sql_server'
db_user = 'sql_user'
db_passwd = 'sql_pass'
db_db = 'db_name'

# ************* Mail settings *************
smtp_server = 'smtp_address'
smtp_port = 'port'
smtp_user = 'user@domain'
smtp_password = 'smtp_password'
smtp_from = '"Sender" <address@domain>'
smtp_to = 'recepient@domain'
smtp_to_name = 'Сергей Петрович'

# ************* xlsx Operations *************
file_paths = 'C:\\Users\\User\\Downloads\\'
file_mask = 'Журнал выданных свидетельств*.xlsx'
needed = ['Номер свидетельства', 'Статус', 'Состояние', 'На кого выдано', 'Выдавший сотрудник', 'Дата выдачи',
          'Дата и время смерти', 'Дата и время рождения', 'Выдано в нашем ЛПУ', 'Форма свидетельства']
titles = [['ID услуги', 'ID услуг по трупу', 'Услуга', 'Цена', 'Сумма по трупу', 'Плательщик', 'Дата платежа',
                'Номер трупа', 'ФИО трупа', 'Отделение', 'Адрес плательщика', 'Номер свидетельства', 'Статус',
                'Выдавший сотрудник'],
          ['Дата выдачи', 'Номер свидетельства', 'На кого выдано', 'Статус', 'Отделение', 'Выдавший сотрудник']]
etalon = ['Номер свидетельства', 'Тип свидетельства', 'Статус', 'Состояние', 'На кого выдано', 'Выдавший сотрудник',
           'Дата выдачи', 'Дата и время смерти', 'Дата и время рождения', 'Выдано в нашем ЛПУ', 'Дата внесения в МИС',
           'Форма свидетельства', 'Дубликат']
reports = ['otchet_platnyedate', 'without_platnye_date', 'kosyak_podrobno']

# ************* File Operations *************
archive_path = 'C:\\Users\\User\\Downloads\\Archives\\'
archive_name = 'journal_archive.zip'