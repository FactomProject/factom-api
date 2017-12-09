from base64 import b64encode
from requests import Session


class FactomAPISession(Session):

    def __init__(self, *args, **kwargs):
        """
        Creates a new CoreAPISession instance.
        """
        super().__init__(*args, **kwargs)

        from . import __version__
        self.headers.update({
            'User-Agent': 'factom-api/{0}'.format(__version__),
            'Accept-Charset': 'utf-8',
            'Content-Type': 'text/plain',
        })

    def init_basic_auth(self, username, password):
        credentials = b64encode('{}:{}'.format(username, password))
        self.headers.update({
            'Authorization': 'Basic {}'.format(credentials)
        })

    def init_tls(self, certfile):
        self.cert = certfile


__all__ = ['FactomAPISession']
