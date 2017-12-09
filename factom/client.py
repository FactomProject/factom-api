import random
import string
import time
import uuid
from urllib.parse import urljoin

from .exceptions import handle_error_response
from .session import FactomAPISession
from .utils import hex


class BaseAPI(object):

    def __init__(self, ec_address=None, fa_address=None, host=None,
                 version='v2', username=None, password=None, certfile=None):
        self.ec_address = ec_address
        self.fa_address = fa_address
        self.version = version
        if host:
            self.host = host

        self.session = FactomAPISession()
        if username and password:
            self.session.init_basic_auth(username, password)

        if certfile:
            self.session.init_tls(certfile)

    @property
    def url(self):
        return urljoin(self.host, self.version)

    def _xact_name(self):
        return 'TX_{}'.format(''.join(random.choices(
            string.ascii_uppercase + string.digits, k=6)))

    def _request(self, method, params=None, id=0):
        data = {
            'jsonrpc': '2.0',
            'id': id,
            'method': method,
        }
        if params:
            data['params'] = params

        resp = self.session.request('POST', self.url, json=data)

        if resp.status_code >= 400:
            handle_error_response(resp)

        return resp.json()['result']


class Factomd(BaseAPI):
    host = 'http://localhost:8088'

    def commit_chain(self, message):
        return self._request('commit-chain', {
            'message': message
        })

    def commit_entry(self, message):
        return self._request('commit-entry', {
            'message': message
        })

    def entry_credit_balance(self, ec_address=None):
        return self._request('entry-credit-balance', {
            'address': ec_address or self.ec_address
        })

    def entry_credit_rate(self):
        return self._request('entry-credit-rate')

    def factoid_balance(self, fa_address=None):
        return self._request('factoid-balance', {
            'address': fa_address or self.fa_address
        })

    def factoid_submit(self, transaction):
        return self._request('factoid-submit', {
            'transaction': transaction
        })

    def reveal_chain(self, entry):
        return self._request('reveal-chain', {
            'entry': entry
        })

    def reveal_entry(self, entry):
        return self._request('reveal-entry', {
            'entry': entry
        })


class FactomWalletd(BaseAPI):
    host = 'http://localhost:8089'

    def add_ec_output(self, name, amount, ec_address=None):
        return self._request('add-ec-output', {
            'tx-name': name,
            'amount': amount,
            'address': ec_address or self.ec_address
        })

    def add_fee(self, name, fa_address=None):
        return self._request('add-fee', {
            'tx-name': name,
            'address': fa_address or self.fa_address
        })

    def add_input(self, name, amount, fa_address=None):
        return self._request('add-input', {
            'tx-name': name,
            'amount': amount,
            'address': fa_address or self.fa_address
        })

    def add_output(self, name, amount, fa_address):
        return self._request('add-output', {
            'tx-name': name,
            'amount': amount,
            'address': fa_address
        })

    def compose_transaction(self, name):
        return self._request('compose-transaction', {
            'tx-name': name
        })

    def new_transaction(self, name=None):
        return self._request('new-transaction', {
            'tx-name': name or self._xact_name()
        })

    def sign_transaction(self, name):
        return self._request('sign-transaction', {
            'tx-name': name
        })

    def sub_fee(self, name, fa_address):
        return self._request('sub-fee', {
            'tx-name': name,
            'address': fa_address
        })

    # Convenience methods

    def create_chain(self, factomd, ext_ids, content, ec_address=None):
        calls = self._request('compose-chain', {
            'chain': {
                'firstentry': {
                    'extids': hex(ext_ids),
                    'content': hex(content)
                },
            },
            'ecpub': ec_address or self.ec_address
        })
        factomd.commit_chain(calls['commit']['params']['message'])
        time.sleep(2)
        return factomd.reveal_chain(calls['reveal']['params']['entry'])

    def create_entry(self, factomd, chain_id, ext_ids, content,
                     ec_address=None):
        calls = self._request('compose-entry', {
            'entry': {
                'chainid': chain_id,
                'extids': hex(ext_ids),
                'content': hex(content)
            },
            'ecpub': ec_address or self.ec_address
        })
        factomd.commit_entry(calls['commit']['params']['message'])
        time.sleep(2)
        return factomd.reveal_entry(calls['reveal']['params']['entry'])

    def xact_fact_to_ec(self, factomd, amount, fa_address=None,
                        ec_address=None):
        name = self._xact_name()
        self.new_transaction(name)
        self.add_input(name, amount, fa_address)
        self.add_ec_output(name, amount, ec_address)
        self.add_fee(name, fa_address)
        self.sign_transaction(name)
        call = self.compose_transaction(name)
        return factomd.factoid_submit(call['params']['transaction'])

    def xact_fact_to_fact(self, factomd, amount, fa_to, fa_from=None):
        name = self._xact_name()
        self.new_transaction(name)
        self.add_input(name, amount, fa_from)
        self.add_output(name, amount, fa_to)
        self.add_fee(name, fa_from)
        self.sign_transaction(name)
        call = self.compose_transaction(name)
        return factomd.factoid_submit(call['params']['transaction'])
