from project_dash.email_sender import IEmailSender


class MockEmailSender(IEmailSender):
    def send_email(self, _receiver: str, _subject: str, _body: str):
        return _receiver