import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from ..env import HOST_ZOHO, PORT_ZOHO, USER_ZOHO, PASS_ZOHO


class Mail(object):
    host_server = HOST_ZOHO
    port_server = PORT_ZOHO
    user_server = USER_ZOHO
    password_server = PASS_ZOHO

    def __init__(self):
        pass

    def send_email(self, to: str, reply_to: str, subject: str, message: str):
        # configura o servidor SMTP
        s = smtplib.SMTP(host=self.host_server, port=self.port_server)
        s.starttls()
        s.login(self.user_server, self.password_server)

        msg = MIMEMultipart()  # cria mensagem

        # configura os parâmetros da mensagem
        msg['From'] = self.user_server
        msg['To'] = to
        msg['Reply-To'] = reply_to
        msg['Subject'] = subject

        # adiciona no corpo da mensagem
        msg.attach(MIMEText(message, 'plain'))

        # envia a mensagem através do servidor
        s.send_message(msg)

        del msg
