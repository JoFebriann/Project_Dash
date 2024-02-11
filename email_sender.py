from email.message import EmailMessage
from kink import di, inject
from abc import ABC, abstractmethod

import smtplib
import ssl

import project_dash.config


class IEmailSender(ABC):
    @abstractmethod
    def send_email(self, _receiver: str, _subject: str, _body: str):
        pass


@inject
class EmailSender(IEmailSender):
    def send_email(self, _receiver: str, _subject: str, _body: str):
        em = EmailMessage()
        em['From'] = di["sender"]
        em['To'] = _receiver

        # Set the subject and body of the email
        em['Subject'] = _subject
        em.set_content(_body)

        # Add SSL (layer of security)
        context = ssl.create_default_context()

        # Log in and send the email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(di["sender"], di["password"])
            smtp.sendmail(di["sender"], _receiver, em.as_string())