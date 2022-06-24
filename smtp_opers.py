from initials import smtp_server, smtp_port, smtp_user, smtp_password, smtp_from, smtp_to, smtp_to_name

import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders
from datetime import datetime as dt


def send_mail(attachment, isTls=True):
    msg = MIMEMultipart()
    msg['From'] = smtp_from
    msg['To'] = smtp_to
    msg['Date'] = formatdate(localtime=True)

    today = dt.now()
    text = f'Отчет по платным с {dt(today.year, today.month + 1, 26):%d.%m.%Y} ' \
           f'по {today:25.%m.%Y} по всем отделениям'

    msg['Subject'] = text

    text = f'Здравствуйте, {smtp_to_name}!\n\n' \
           f'{text} во вложении к письму.\n\n' \
           f'{"*" * 40}\n' \
           f'{" " * 13}Best regards!\n' \
           f'{"*" * 40}'

    msg.attach(MIMEText(text))

    part = MIMEBase('application', "octet-stream")
    part.set_payload(open(attachment, "rb").read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename={attachment}')
    msg.attach(part)

    #context = ssl.SSLContext(ssl.PROTOCOL_SSLv3)
    #SSL connection only working on Python 3+
    smtp = smtplib.SMTP(smtp_server, smtp_port)
    if isTls:
        smtp.starttls()
    smtp.login(smtp_user, smtp_password)
    smtp.sendmail(smtp_from, smtp_to, msg.as_string())
    smtp.quit()
