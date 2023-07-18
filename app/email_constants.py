import smtplib
import ssl

from email_configuration import *

sender = SENDER_EMAIL
receivers = RECEIVER_EMAIL
message = MESSAGE
context = ssl.create_default_context()


def send_email(too_email=None, email_body=""):
    if too_email is None:
        too_email = []
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls(context=context)
        server.login(sender, PASSWORD)
        server.sendmail(sender, too_email, email_body)
