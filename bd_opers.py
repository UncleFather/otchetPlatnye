from initials import db_host, db_user, db_passwd, db_db

import pymysql


# Функция подключения к БД MysQL
def bd_connect():
    return pymysql.connect(host=db_host, user=db_user, passwd=db_passwd, db=db_db)


# Функция подготовки базы данных к экспорту отчетов (добавление записей из фалов выгрузок xlsx и
# удаление дублирующихся записей)
def bd_prepare(val=''):
    # Устанавливаем соединение с БД
    con = bd_connect()

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
            # Печатаем количество строк, добавленных в таблицу bars_svidet
            # print(cur.rowcount, "records inserted!")

        # Если на этапе выполнения какого-либо из запросов транзакции возникла ошибка
        except Exception as err:
            # Откатываем изменения
            con.rollback()
            # Печатаем ошибку
            print(err)

        # Удаляем временную таблицу tmp_table
        cur.execute("DROP TEMPORARY TABLE `tmp_table`;")

# Функция выполнения отчетов
def bd_report(query_name):
    # Устанавливаем соединение с БД
    con = bd_connect()

    with con:
        # Создаем курсор
        cur = con.cursor()
        # Выполняем запрос к БД, соответсвующий имени требуемого отчета (otchet_platnyedate,
        # without_platnye_date, kosyak_podrobno)
        cur.execute(f"SELECT "
                        f"* "
                    f"FROM "
                        f"`sdo`.`{query_name}`;")

        # Возвращаем все строки выполненного запроса
        return cur.fetchall()
