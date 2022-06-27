# Python
## Получение объединенного отчета по платным услугам
__Назначение:__
    ___Получение выгрузок отчетов из МИС «Барс», сборка их в единый массив, добавление этого массива
    в базу данных локальной МИС (MySQL), получение объединенных отчетов и отправка их по электронной почте.___
### Список модулей:
+ __initials_common.py__ - 
    Инициализационный модуль, для хранения учетных данных, адресов и глобальных переменных, используемых в прочих модулях
+ __main.py__ -
    Основной модуль
+ __bars_opers.py__ - 
    Модуль для выполнения операций в МИС «Барс» через экземпляр браузера
+ __bd_opers.py__ - 
    Модуль для выполнения запросов к СУБД MySQL локальной МИС
+ __file_opers.py__ -
    Модуль для выполнения операций с файлами (архивация, удаление)
+ __smtp_opers.py__ -
    Модуль для отправки электронной почты через smtp-сервер
+ __xlsx_opers.py__ -
    Модуль для обработки файлов MS Excel
+ __xlsx_prerare_for_access.py__ -
    Вспомогательный модуль для сборки xlsx файлов выгрузок в единый файл (не используется)
+ __chromedriver.exe__ -
    Web - драйвер браузера GoogleChrome
+ __log_report.txt__ -
    Журнал выполнения программы
+ __Otchet_Date_YYYY.MM.DD.xlsx__ -
    Сформированный фалй с итоговыми отчетами
