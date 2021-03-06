from initials_common import txt_log_path, txt_log_name, txt_inifile

from datetime import datetime as dt


# Функция замены переменной «etalon» в инициализационном файле
def writing_etalon(etalon_str):
    # Инициализируем переменную, указывающую количество отступов для файла отчета
    indention = 8
    # Открываем файл с инициализационными данными для чтения и добавления данных
    handler = open(txt_inifile, 'a+', encoding='utf8')
    log_write(f'Открыт инициализационный файл {txt_inifile} для записи переменной «etalon»', indention)
    # Помещаем указатель в начало файла, так как файл открыт в режиме добавления данных
    handler.seek(0)
    # Инициализируем переменную, показывающую считывается ли в настоящий момент времени переменная «etalon»
    is_etalon = False
    # Записываем прочитанный инициализационный файл в переменную для дальнейшей обработки
    list_ini = list(handler)
    # Очищаем исходный инициализационный файл
    handler.truncate(0)
    log_write(f'Инициализационный файл очищен и подготовлен для записи', indention)
    # Для каждой строки файла выполняем цикл
    log_write(f'Запись переменных в инициализационный файл', indention)
    mes_txt = ''
    for i in range(len(list_ini)):
        # Если строка начинается с символов 'etalon = [' или уже идет работа с переменной «etalon»
        if list_ini[i][0:10] == 'etalon = [' or is_etalon:
            # Показываем, что идет работа с переменной «etalon»
            is_etalon = True
        # Если работаем со строкой, не содержащей какую-либо часть переменной «etalon»
        else:
            # Записываем в инициализационный файл текущую строку
            handler.write(list_ini[i])
            mes_txt += f'{i}, '

        # Если велась работа с переменной «etalon» и мы обнаружили закрывающую скобку, означающую окончание
        # переменной
        if is_etalon and ']' in list_ini[i]:
            # Записываем переданное в вызове функции текстовое представление новой переменной «etalon»
            # в инициализационный файл
            handler.write(etalon_str)
            log_write(f'Новое значение переменной «etalon» успешно записано', indention)
            # Показываем, что работа с переменной «etalon» завершена
            is_etalon = False
    log_write(f'Строки ({mes_txt}) успешно записаны', indention)
    # Закрываем инициализационный файл
    handler.close()
    log_write(f'Обновленный инициализационный файл сохранен успешно', indention)


# Процедура записи журнала выполнения программы
def log_write(mes_txt, indention=0):
    # Открываем файл журнала событий в режиме добавления
    handler = open(txt_log_path + txt_log_name, 'a', encoding='utf8')
    # Записываем в файл сообщение с отступом, переданными при вызове процедуры
    # Добавляем время, в случае, если отступ не равен нулю
    curr_time = "" if indention == 0 else f'({dt.now():%H:%M:%S})'
    handler.write(f'{" " * indention}{mes_txt} {curr_time}\n')
    # Закрываем файл журнала событий
    handler.close()
