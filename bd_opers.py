import pymysql
from initials import db_host, db_user, db_passwd, db_db

def main_bd():
    con = pymysql.connect(host=db_host, user=db_user,
                          passwd=db_passwd, db=db_db)

    with con:
        cur = con.cursor()
        cur.execute("SELECT VERSION()")

        version = cur.fetchone()

        print("Database version: {}".format(version[0]))

        cur.execute("CREATE TEMPORARY TABLE `tmp_table` select `sdo`.`sdo_plat_uslugi_spisok`.`id` AS `ID`,`sdo`.`sdo_plat_uslugi_spisok`.`id_plat_uslugi` AS "
                    "`PuID`,`sdo`.`sdo_plat_uslugi_sp`.`name_plat_usluga` AS `PuName`,`sdo`.`sdo_plat_uslugi_sp`.`price` AS "
                    "`PuPrice`,`sdo`.`sdo_plat_uslugi`.`summ_plat_uslugi` AS `PuSumm`,`sdo`.`sdo_plat_uslugi`.`fio_plat` AS "
                    "`PuFIOPlat`,from_unixtime(`sdo`.`sdo_plat_uslugi`.`d_zapoln`) AS `PuDate`,`sdo`.`sdo_plat_uslugi`.`id_trup` "
                    "AS `PuIDTrup`,cast(concat(lower(`sdo`.`sdo_trup4`.`fam`),' ',lower(`sdo`.`sdo_trup4`.`name`),' ',"
                    "lower(`sdo`.`sdo_trup4`.`otch`)) as char(200) charset utf8) AS `PuFIOTrup`,`sdo`.`sdo_otdel`.`name_otd` AS "
                    "`puOtd`,`sdo`.`sdo_plat_uslugi`.`adres_plat` AS `PuAdrPlat` from ((((`sdo`.`sdo_plat_uslugi_spisok` join "
                    "`sdo`.`sdo_plat_uslugi_sp` on((`sdo`.`sdo_plat_uslugi_spisok`.`id_plat_usluga_sp` = "
                    "`sdo`.`sdo_plat_uslugi_sp`.`id_sp`))) join `sdo`.`sdo_plat_uslugi` on((`sdo`.`sdo_plat_uslugi_spisok`.`id_plat_uslugi` "
                    "= `sdo`.`sdo_plat_uslugi`.`id_usluga`))) join `sdo`.`sdo_otdel` on((`sdo`.`sdo_plat_uslugi`.`id_otd` = "
                    "`sdo`.`sdo_otdel`.`id_otd`))) left join `sdo`.`sdo_trup4` on((`sdo`.`sdo_plat_uslugi`.`id_trup` = "
                    "`sdo`.`sdo_trup4`.`id_trup`))) where (`sdo`.`sdo_plat_uslugi`.`d_zapoln` between unix_timestamp((now() - "
                    "interval 6 month)) and unix_timestamp(now()))")

        cur.execute("SELECT `tmp_table`.`id`, `tmp_table`.`PuID`, `tmp_table`.`PuName`, `tmp_table`.`PuPrice`, `tmp_table`.`PuSumm`, "
                    "`tmp_table`.`PuFIOPlat`, `tmp_table`.`PuDate`, `tmp_table`.`PuIDTrup`, `tmp_table`.`PuFIOTrup`, "
                    "`tmp_table`.`puOtd`, `tmp_table`.`PuAdrPlat`, `sdo`.`bars_svidet`.`Svidet_Num`, "
                    "`sdo`.`bars_svidet`.`Status`, `sdo`.`bars_svidet`.`Kto_Vydal` FROM `tmp_table` left join "
                    "`sdo`.`bars_svidet` on `tmp_table`.`PuFIOTrup` = `sdo`.`bars_svidet`.`Na_Kogo` "
                    "WHERE (((`tmp_table`.`PuDate`) between str_to_date(concat(year(now() - interval 1 month),'-',"
                    "month(now() - interval 1 month),'-',26), '%Y-%m-%d') And str_to_date(concat(year(now()),'-',month(now()),"
                    "'-',26), '%Y-%m-%d'))) order by `tmp_table`.`PuID`, `tmp_table`.`PuDate`;")

        rows = cur.fetchall()

        for row in rows:
            '''print("{0} {1} {2} {3} {4} {5} {6} {7} {8} {9} {10}".format(row[0], row[1], row[2], row[3], row[4], row[5],
                                                                                  row[6], row[7], row[8], row[9], row[10]))'''
            print(f'{row[0]} {row[1]} {row[2]} {row[3]} {row[4]} {row[5]} {row[6]} {row[7]} {row[8]} {row[9]} {row[10]} '
                  f'{row[11]} {row[12]} {row[13]}')

