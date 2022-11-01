from initials_common import smtp_server, smtp_port, smtp_user, smtp_password, smtp_from, smtp_to, smtp_to_name

from txt_opers import log_write

from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders
from datetime import datetime as dt


# Функция отправки писем с вложением xlsx файла по smtp
def send_mail(attachment, isTls=True):
    # Инициализируем переменную, указывающую количество отступов для файла отчета
    indention = 4
    # Формируем служебные заголовки отправляемого письма
    msg = MIMEMultipart()
    msg['From'] = smtp_from
    # Подготавливаем строку получателей для передачи в служебный заголовок «To»
    recipients = ", ".join(smtp_to)
    msg['To'] = recipients
    msg['Date'] = formatdate(localtime=True)

    # Получаем текущую дату
    today = dt.now()
    # Формируем текст для темы письма
    text = f'Отчет по платным с {dt(today.year, today.month + 1, 26):%d.%m.%Y} ' \
           f'по {today:25.%m.%Y} по всем отделениям'

    msg['Subject'] = text

    # Формируем текст для тела письма
    text = f'Здравствуйте, {smtp_to_name}!\n\n' \
           f'{text} во вложении к письму.\n\n' \
           f'{"*" * 40}\n' \
           f'{" " * 13}Best regards!\n' \
           f'{"*" * 40}'
    log_write(f'Созданы заголовки письма', indention)
    msg.attach(MIMEText(text))

    # Формируем письмо
    part = MIMEBase('application', "octet-stream")
    # Присоединяем указанный в вызове функции файл к письму в качестве вложения
    part.set_payload(open(attachment, "rb").read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename={attachment}')
    msg.attach(part)
    log_write(f'Присоединен файл итогового отчета {attachment} в качестве вложения', indention)

    # Создаем объект smtp подключения
    smtp = SMTP(smtp_server, smtp_port)
    log_write(f'Подключаемся к серверу {smtp_server}', indention)
    if isTls:
        smtp.starttls()
    # Подключаемся к smtp серверу, со своими учетными данными
    smtp.login(smtp_user, smtp_password)
    log_write(f'Идентифицируемся с именем {smtp_user}', indention)
    # Выполняем отправку письма
    smtp.sendmail(smtp_from, smtp_to, msg.as_string())
    log_write(f'Письмо успешно отправлено адресату {smtp_to_name}', indention)
    # Закрываем объект smtp подключения
    smtp.quit()
