from initials import archive_path, archive_name

from txt_opers import log_write
from datetime import datetime as dt

from os import path, remove
from zipfile import ZipFile, ZIP_DEFLATED


# Процедура архивирования и удаления xlsx файлов журналов выгрузок
def archive_files(files_list):
    # Инициализируем переменную, указывающую количество отступов для файла отчета
    indention = 6
    # Создаем (или открываем, если он уже создан) архивный файл по указанному пути, указываем метод
    # сжатия ZIP_DEFLATED и степень сжатия 9
    zip_file = ZipFile(file=f'{archive_path}{archive_name}_{dt.now():%Y.%m.%d}.zip', mode='a',
                               compression=ZIP_DEFLATED, compresslevel=9)
    log_write(f'Проинициализирован файл архива для файлов выгрузок', indention)
    # Для всех файлов из переданного в функцию списка
    for item in files_list:
        # Запаковываем текущий файл в архив без указания пути, указывая метод сжатия ZIP_DEFLATED
        # и степень сжатия 9
        zip_file.write(item, compress_type=ZIP_DEFLATED, compresslevel=9, arcname=path.basename(item))
        log_write(f'Файл выгрузки {path.basename(item)} успешно запакован в архив', indention)

    # Закрываем архивный файл
    zip_file.close()
    # Для всех файлов из переданного в функцию списка
    log_write(f'Процедура удаления файлов...', indention)
    indention = 8
    for item in files_list:
        # Удаляем текущий файл
        log_write(f'Файл выгрузки {path.basename(item)} удален', indention)
        remove(item)

