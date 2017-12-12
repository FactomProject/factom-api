from base64 import b64encode
from requests import Session


class FactomAPISession(Session):

    def __init__(self, *args, **kwargs):
        """
        Creates a new CoreAPISession instance.
        """
        super(FactomAPISession, self).__init__(*args, **kwargs)

        self.headers.update({
            'Accept-Charset': 'utf-8',
            'Content-Type': 'text/plain',
        })

    def init_basic_auth(self, username, password):
        credentials = b64encode('{}:{}'.format(username, password).encode())
        self.headers.update({
            'Authorization': 'Basic {}'.format(credentials.decode())
        })

    def init_tls(self, certfile):
        self.verify = certfile


__all__ = ['FactomAPISession']
