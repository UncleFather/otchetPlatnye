import sys

from initials import db_host, db_user, db_passwd, db_db

from txt_opers import log_write

import pymysql


# Функция подключения к БД MysQL
def bd_connect():
    return pymysql.connect(host=db_host, user=db_user, passwd=db_passwd, db=db_db)


# Функция подготовки базы данных к экспорту отчетов (добавление записей из фалов выгрузок xlsx и
# удаление дублирующихся записей)
def bd_prepare(val=''):
    # Инициализируем переменную, указывающую количество отступов для файла отчета
    indention = 4
    # Устанавливаем соединение с БД
    con = bd_connect()
    log_write(f'Соединение с базой данных {db_db} установлено', indention)

    with con:
        # Создаем курсор
        cur = con.cursor()

        # При необходимости получить версию СУБД, раскомментируем следующие строки
        '''# Выполняем запрос версии СУБД
        cur.execute("SELECT VERSION()")
        # Получаем первый результат
        version = cur.fetchone()
        # Выводим на печать
        print("Database version: {}".format(version[0]))'''

        # Создаем в памяти временную таблицу tmp_table из таблицы bars_svidet
        cur.execute("CREATE TEMPORARY TABLE `tmp_table` "
                    "SELECT * "
                    "FROM "
                    "`sdo`.`bars_svidet`")
        # Инициализируем переменную для хранения исходного количества строк в таблице bars_svidet
        initial_rows_count = cur.rowcount
        log_write(f'Временная таблица «tmp_table» создана', indention)

        # Формируем строку запроса для добавления данных в таблицу
        sql = "INSERT INTO `tmp_table`(" \
              "`Svidet_Num`, " \
              "`Status`, " \
              "`Condition`, " \
              "`Na_Kogo`, " \
              "`Kto_Vydal`, " \
              "`Data_Vydachi`, " \
              "`Date_Time_Death`, " \
              "`Date_Time_Birth`, " \
              "`Our_Issue`, " \
              "`Svidet_Form`) " \
              "values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

        # Пытаемся выполнить запросы к БД
        try:
            log_write(f'Выполняем запросы по добавлению данных в таблицу «bars_svidet»', indention)
            # Добавляем во временную таблицу tmp_table строки из xlsx файлов выгрузок,
            # переданные при вызове функции
            cur.executemany(sql, val)
            # Очищаем таблицу bars_svidet
            cur.execute("DELETE FROM `sdo`.`bars_svidet`;")
            # Записываем в таблицу bars_svidet только неповторяющиеся строки из временной таблицы tmp_table
            cur.execute("INSERT INTO `sdo`.`bars_svidet` ("
                        "SELECT * "
                        "FROM "
                        "`tmp_table` "
                        "GROUP BY "
                        "`tmp_table`.`Svidet_Num`, "
                        "`tmp_table`.`Status`, "
                        "`tmp_table`.`Condition`, "
                        "`tmp_table`.`Na_Kogo`, "
                        "`tmp_table`.`Kto_Vydal`, "
                        "`tmp_table`.`Data_Vydachi`, "
                        "`tmp_table`.`Date_Time_Death`, "
                        "`tmp_table`.`Date_Time_Birth`, "
                        "`tmp_table`.`Our_Issue`, "
                        "`tmp_table`.`Svidet_Form`);"
                        )
            # Выполняем транзакцию
            con.commit()
            log_write(f'В таблицу «bars_svidet» добавлено {cur.rowcount - initial_rows_count} строк', indention)
            # Печатаем количество строк, добавленных в таблицу bars_svidet
            # print(cur.rowcount, "records inserted!")

        # Если на этапе выполнения какого-либо из запросов транзакции возникла ошибка
        except Exception as err:
            # Откатываем изменения
            con.rollback()
            # Печатаем ошибку
            print(err)
            log_write(f'При выполнении транзакции возникла ошибка {err}. Изменения в БД не применены. Работа '
                      f'программы будет прервана', indention)
            # Генерируем выход из программы
            sys.exit(-1)

        # Удаляем временную таблицу tmp_table
        cur.execute("DROP TEMPORARY TABLE `tmp_table`;")
        log_write(f'Временная таблица удалена. Новые строки успешно добавлены в базу данных.', indention)

# Функция выполнения отчетов
def bd_report(query_name):
    # Инициализируем переменную, указывающую количество отступов для файла отчета
    indention = 4
    # Устанавливаем соединение с БД
    con = bd_connect()
    log_write(f'Соединение с базой данных {db_db} установлено', indention)

    with con:
        # Создаем курсор
        cur = con.cursor()
        # Выполняем запрос к БД, соответсвующий имени требуемого отчета (otchet_platnyedate,
        # without_platnye_date, kosyak_podrobno)
        cur.execute(f"SELECT "
                        f"* "
                    f"FROM "
                        f"`sdo`.`{query_name}`;")
        log_write(f'Запрос отчета {query_name} успешно выполнен', indention)

        # Возвращаем все строки выполненного запроса
        return cur.fetchall()
