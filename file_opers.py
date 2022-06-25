from initials import archive_path, archive_name, file_paths, file_mask

from pathlib import Path
from os import path, remove
import zipfile

# Процедура архивирования и удаления xlsx файлов журналов выгрузок
def archive_files(files_list):
    # Создаем (или открываем, если он уже создан) архивный файл по указанному пути, указываем метод
    # сжатия ZIP_DEFLATED и степень сжатия 9
    zip_file = zipfile.ZipFile(file=archive_path + archive_name, mode='a', compression=zipfile.ZIP_DEFLATED,
                               compresslevel=9)
    # Для всех файлов из переданного в функцию списка
    for item in files_list:
        # Запаковываем текущий файл в архив без указания пути, указывая метод сжатия ZIP_DEFLATED
        # и степень сжатия 9
        zip_file.write(item, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9, arcname=path.basename(item))

    # Закрываем архивный файл
    zip_file.close()
    # Для всех файлов из переданного в функцию списка
    for item in files_list:
        # Удаляем текущий файл
        remove(item)

