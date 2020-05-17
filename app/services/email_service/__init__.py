import threading

from app import app
from app.services.utils.constants_utility import ConstantsUtility


def async_email(**kwargs):
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    import smtplib

    MAIL_SERVER = app.config["MAIL_SERVER"]
    MAIL_SERVER_PORT = app.config["MAIL_SERVER_PORT"]
    mail_sender = app.config["DEFAULT_SENDER_EMAIL"]
    mail_sender_password = app.config["DEFAULT_SENDER_EMAIL_PASSWORD"]

    msg = MIMEMultipart()
    msg[ConstantsUtility.EMAIL_FROM] = mail_sender
    msg[ConstantsUtility.EMAIL_TO] = kwargs[ConstantsUtility.KWARGS_ADDRESS]
    msg[ConstantsUtility.MIME_SUBJECT] = kwargs[ConstantsUtility.KWARGS_SUBJECT]
    if kwargs.get(ConstantsUtility.KWARGS_IS_HTML_TEXT, False) is False:
        msg.attach(MIMEText(kwargs[ConstantsUtility.KWARGS_TEXT], ConstantsUtility.EMAIL_MIME_TYPE_PLAIN))
    else:
        msg.attach(MIMEText(kwargs[ConstantsUtility.KWARGS_TEXT], ConstantsUtility.EMAIL_MIME_TYPE_HTML))

    server = smtplib.SMTP(MAIL_SERVER, MAIL_SERVER_PORT)
    server.starttls()
    server.login(mail_sender, mail_sender_password)

    server.sendmail(mail_sender, kwargs[ConstantsUtility.KWARGS_ADDRESS], msg.as_string())
    server.quit()


def email(address, subject, text, is_html_text=False):
    kwargs = {
        ConstantsUtility.KWARGS_ADDRESS: address,
        ConstantsUtility.KWARGS_SUBJECT: subject,
        ConstantsUtility.KWARGS_TEXT: text,
        ConstantsUtility.KWARGS_IS_HTML_TEXT: is_html_text
    }

    sender = threading.Thread(target=async_email, kwargs=kwargs)
    sender.start()
