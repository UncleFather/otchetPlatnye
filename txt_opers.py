def writing_etalon(etalon_str):
    path_ini = 'initials.py'
    handler = open(path_ini, 'a+', encoding='utf8')
    handler.seek(0)
    is_etalon = False
    list_ini = list(handler)
    handler.truncate(0)
    for i in range(len(list_ini)):
        if list_ini[i][0:10] == 'etalon = [' or is_etalon:
            is_etalon = True
        else:
            handler.write(list_ini[i])

        if is_etalon and ']' in list_ini[i]:
            handler.write(etalon_str)
            is_etalon = False
    handler.close()
