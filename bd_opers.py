from initials import db_host, db_user, db_passwd, db_db

import pymysql


def bd_connect():
    return pymysql.connect(host=db_host, user=db_user, passwd=db_passwd, db=db_db)


def bd_prepare(val=''):
    con = bd_connect()

    with con:
        cur = con.cursor()
        '''cur.execute("SELECT VERSION()")

        version = cur.fetchone()

        print("Database version: {}".format(version[0]))'''

        cur.execute("CREATE TEMPORARY TABLE `tmp_table` "
                    "SELECT * "
                    "FROM "
                    "`sdo`.`bars_svidet`")

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

        try:
            # inserting the values into the table
            cur.executemany(sql, val)
            cur.execute("DELETE FROM `sdo`.`bars_svidet`;")
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
            # commit the transaction
            con.commit()
            # print(cur.rowcount, "records inserted!")

        except Exception as err:
            con.rollback()
            print(err)

        cur.execute("DROP TEMPORARY TABLE `tmp_table`;")


def bd_report(query_name):
    con = bd_connect()

    with con:
        cur = con.cursor()
        # otchet_platnyedate, without_platnye_date, kosyak_podrobno
        cur.execute(f"SELECT "
                        f"* "
                    f"FROM "
                        f"`sdo`.`{query_name}`;")

        return cur.fetchall()
