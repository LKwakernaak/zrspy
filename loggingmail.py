from smtplib import SMTP_SSL
import ssl
from getpass import getpass
import configparser
import logging
from logging.handlers import SMTPHandler
from email.message import EmailMessage
from email.mime.text import MIMEText

from datamodel import engine, parse_appointments, find_keys

mail_logger = logging.getLogger()

config = configparser.ConfigParser()
config.read('config.ini')
sender_email = config['DEFAULT']['Email']
username = config['DEFAULT']['Username']
password = config['DEFAULT']['Password']

port = 465
smtp_server = "smtp.gmail.com"
receiver_email = "lennardkwakernaak@gmail.com", sender_email
subject = "No reply: ZRSpy changelog"

credentials = (username, password)

mail_handler = SMTPHandler(smtp_server, sender_email, [receiver_email], subject, credentials, ())
mail_handler.setLevel(logging.INFO)
mail_logger.addHandler(mail_handler)

if __name__ == "__main__":
    mail_logger.info("testing")

def sendmail(receiver_email, message):
    print("SENDING MAIL")
    with SMTP_SSL(smtp_server) as server:
        server.ehlo()
        server.login(sender_email, password)
        server.send_message(message)
        # server.sendmail(sender_email, receiver_email, body)
        print(message)

def send_maillog(changelog):
    message = EmailMessage()
    message.set_content(MIMEText(changelog, 'html'))
    message['Subject'] = subject
    message['From'] = sender_email
    for adress in [receiver_email]:
        message['To'] = adress
        sendmail(adress, message)


if __name__ == '__main__':
    send_maillog('test')

# with SMTP_SSL(smtp_server) as server:
#     # server.ehlo()
#     # server.starttls(context=context)
#     server.ehlo()
#     server.login(sender_email, password)
#     # server.sendmail(sender_email, receiver_email, body)
#     print(body)