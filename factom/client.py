import random
import string
import time
try:
    from urllib.parse import urlparse, urljoin  # noqa
except ImportError:
    from urlparse import urlparse, urljoin  # noqa

from .exceptions import handle_error_response
from .session import FactomAPISession


NULL_BLOCK = '0000000000000000000000000000000000000000000000000000000000000000'


class BaseAPI(object):

    def __init__(self, ec_address=None, fct_address=None, host=None,
                 version='v2', username=None, password=None, certfile=None):
        """
        Instantiate a new API client.

        Args:
            ec_address (str): A default entry credit address to use for
                transactions. Credits will be spent from this address
                with the exception of the `fct_to_ec()` shortcut.
            fct_address (str): A default factoid address to use for
                transactions. Factoids will be spent from this address.
            host (str): Hostname, including http(s)://, of the factomd
                or factom-walletd instance to query.
            version (str): API version to use. This should remain 'v2'.
            username (str): RPC username for protected APIs.
            password (str): RPC password for protected APIs.
            certfile (str): Path to certificate file to verify for TLS
                connections (mostly untested).
        """
        self.ec_address = ec_address
        self.fct_address = fct_address
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

    def admin_block(self, keymr):
        """
        Retrieve a specified admin block given its merkle root key.
        """
        return self._request('admin-block', {
            'keymr': keymr
        })

    def admin_block_by_height(self, height):
        """
        Retrieves administrative blocks for any given height.
        The admin block contains data related to the identities within
        the factom system and the decisions the system makes as it
        builds the blockchain. The abentries(admin block entries) in
        the JSON response can be of various types, the most common is a
        directory block signature(DBSig). A majority of the federated
        servers sign every directory block, meaning every block after
        m5 will contain 5 DBSigs in each admin block.
        """
        return self._request('ablock-by-height', {
            'height': height
        })

    def anchors(self, hash: str = None, height: int = None):
        """
        Retrieve the set of anchors for a given object hash or directory block height.
        """
        if hash is None:
            assert height is not None, 'No hash provided, height must not be none'
            assert height >= 0, 'Height must be >= 0'
            params = {'height': height}
        else:
            assert height is None, 'Hash provided, height must be None'
            params = {'hash': hash}

        return self._request('anchors', params)

    def chain_head(self, chain_id):
        return self._request('chain-head', {
            'chainid': chain_id
        })

    def commit_chain(self, message):
        return self._request('commit-chain', {
            'message': message
        })

    def commit_entry(self, message):
        return self._request('commit-entry', {
            'message': message
        })

    def current_minute(self):
        """
        The current-minute API call returns:
        leaderheight: returns the current block height.
        directoryblockheight: returns the last saved height.
        minute: returns the current minute number for the open entry
            block.
        currentblockstarttime: returns the start time for the current
            block.
        currentminutestarttime: returns the start time for the current
            minute.
        currenttime: returns the current nodes understanding of current
            time.
        directoryblockinseconds: returns the number of seconds per
            block.
        stalldetected: returns if factomd thinks it has stalled.
        faulttimeout: returns the number of seconds before leader node
            is fault
        ed for failing to provide a necessary message.
        roundtimeout: returns the number of seconds between rounds of an
        election during a fault.
        """
        return self._request('current-minute')

    def directory_block_by_height(self, height):
        """
        Retrieve a directory block given only its height.
        """
        return self._request('dblock-by-height', {
            'height': height
        })

    def directory_block_by_keymr(self, keymr):
        """
        Every directory block has a KeyMR (Key Merkle Root), which can
        be used to retrieve it. The response will contain information
        that can be used to navigate through all transactions (entry
        and factoid) within that block. The header of the directory
        block will contain information regarding the previous directory
        block keyMR, directory block height, and the timestamp.
        """
        return self._request('directory-block', {
            'keymr': keymr
        })

    def directory_block_head(self):
        """
        The directory block head is the last known directory block by
        factom, or in other words, the most recently recorded block.
        This can be used to grab the latest block and the information
        required to traverse the entire blockchain.
        """
        return self._request('directory-block-head')

    def entry(self, hash):
        """
        Get an Entry from factomd specified by the Entry Hash.
        """
        resp = self._request('entry', { 'hash': hash })
        resp['extids'] = [bytes.fromhex(x) for x in resp['extids']]
        resp['content'] = bytes.fromhex(resp['content'])
        return resp

    def entry_block(self, keymr):
        """
        Retrieve a specified entry block given its merkle root key. The
        entry block contains 0 to many entries
        """
        return self._request('entry-block', {
            'keymr': keymr
        })

    def entry_credit_balance(self, ec_address=None):
        """
        Return its current balance for a specific entry credit address.
        """
        return self._request('entry-credit-balance', {
            'address': ec_address or self.ec_address
        })

    def entry_credit_block(self, keymr):
        """
        Retrieve a specified entrycredit block given its merkle root
        key. The numbers are minute markers.
        """
        return self._request('entrycredit-block', {
            'keymr': keymr
        })

    def entry_credit_block_by_height(self, height):
        """
        Retrieve the entry credit block for any given height.
        These blocks contain entry credit transaction information.
        """
        return self._request('ecblock-by-height', {
            'height': height
        })

    def entry_credit_rate(self):
        """
        Returns the number of Factoshis (Factoids *10^-8) that purchase
        a single Entry Credit.
        The minimum factoid fees are also determined by this rate,
        along with how complex the factoid transaction is.
        """
        return self._request('entry-credit-rate')

    def factoid_balance(self, fct_address=None):
        """
        Returns the number of Factoshis (Factoids *10^-8)
        that are currently available at the address specified.
        """
        return self._request('factoid-balance', {
            'address': fct_address or self.fct_address
        })

    def factoid_block_by_height(self, height):
        """
        Retrieve the factoid block for any given height. These blocks
        contain factoid transaction information.
        """
        return self._request('fblock-by-height', {
            'height': height
        })

    def factoid_block_by_keymr(self, keymr):
        """
        Retrieve a specified factoid block given its merkle root key.
        """
        return self._request('factoid-block', {
            'keymr': keymr
        })

    def factoid_submit(self, transaction):
        """
        The factoid-submit API takes a specifically formatted message
        encoded in hex that includes signatures.If you have a
        factom-walletd instance running, you can construct this
        factoid-submit API call with compose-transaction which takes
        easier to construct arguments.
        """
        return self._request('factoid-submit', {
            'transaction': transaction
        })

    def heights(self):
        """
        Returns various heights that allows you to view the state of the
        blockchain. The heights returned provide a lot of information
        regarding the state of factomd, but not all are needed by most
        applications. The heights also indicate the most recent block,
        which could not be complete, and still being built. The heights
        mean as follows:

        directoryblockheight : The current directory block height of
        the local factomd node.
        leaderheight : The current block being worked on by the leaders
        in the network. This block is not yet complete, but all
        transactions submitted will go into this block (depending on
        network conditions, the transaction may be delayed into the
        next block)
        entryblockheight : The height at which the factomd node has all
        the entry blocks. Directory blocks are obtained first, entry
        blocks could be lagging behind the directory block when syncing.
        entryheight : The height at which the local factomd node has
        all the entries. If you added entries at a block height above
        this, they will not be able to be retrieved by the local
        factomd until it syncs further.
        """
        return self._request('heights')

    def multiple_entry_credit_balances(self, ec_address_list):
        """
         Used to query the acknowledged and saved balances for a list
         of entry credit addresses.

         Args:
            ec_address_list(list): A list of entry credit addresses
        """
        return self._request('multiple-ec-balances', {
            'addresses': ec_address_list
        })

    def multiple_factoid_balances(self, fct_address_list):
        """
        Used to query the acknowledged and saved balances in factoshis
        (a factoshi is 10^8 factoids) not factoids(FCT) for a list of
        FCT addresses.
        Args:
            fct_address_list(list): A list of factoid addresses
        """
        return self._request('multiple-fct-balances', {
            'addresses': fct_address_list
        })

    def pending_entries(self):
        """
        Returns an array of the entries that have been submitted but
        have not been recorded into the blockchain.
        """
        return self._request('pending-entries')

    def pending_transactions(self):
        """
        Returns an array of factoid transactions that have not yet been
        recorded in the blockchain,
        but are known to the system.
        """
        return self._request('pending-transactions')

    def properties(self):
        """
        Retrieve current properties of the Factom system, including the
        software and the API versions.
        """
        return self._request('properties')

    def raw_data(self, hash):
        """
        Retrieve an entry or transaction in raw format, the data is a
        hex encoded string.
        """
        return self._request('raw-data', {
            'hash': hash
        })

    def receipt(self, hash, include_raw_entry: bool = False):
        """
        Retrieve a receipt providing cryptographically verifiable proof
        that information was recorded in the factom blockchain and that
        this was subsequently anchored in the bitcoin blockchain.
        """
        return self._request('receipt', {
            'hash': hash,
            'includerawentry': include_raw_entry,
        })

    def reveal_chain(self, entry):
        return self._request('reveal-chain', {
            'entry': entry
        })

    def reveal_entry(self, entry):
        return self._request('reveal-entry', {
            'entry': entry
        })

    def send_raw_message(self, message):
        """
        Send a raw hex encoded binary message to the Factom network.
        This is mostly just for debugging and testing.
        """
        return self._request('send-raw-message', {
            'message': message
        })

    def transaction(self, hash):
        """
        Retrieve details of a factoid transaction using a transaction
        hash (or corresponding transaction id).
        """
        return self._request('transaction', {
            'hash': hash
        })

    # Convenience methods

    def read_chain(self, chain_id, include_entry_context=False):
        """
        Shortcut method to read an entire chain.

        Args:
            chain_id (str): Chain ID to read.
            include_entry_context (bool): Whether to include extra information like
                entry hash, timestamp, and block height

        Returns:
            list[dict]: A list of entry dictionaries in reverse
                chronologial order.
        """
        entries = []
        keymr = self.chain_head(chain_id)['chainhead']
        while keymr != NULL_BLOCK:
            block = self.entry_block(keymr)
            for entry_pointer in reversed(block['entrylist']):
                entry = self.entry(entry_pointer['entryhash'])
                if include_entry_context:
                    entry['entryhash'] = entry_pointer['entryhash']
                    entry['timestamp'] = entry_pointer['timestamp']
                    entry['dbheight'] = block['header']['dbheight']
                entries.append(entry)
            keymr = block['header']['prevkeymr']
        return entries


class FactomWalletd(BaseAPI):
    host = 'http://localhost:8089'

    def add_ec_output(self, name, amount, ec_address=None):
        return self._request('add-ec-output', {
            'tx-name': name,
            'amount': amount,
            'address': ec_address or self.ec_address
        })

    def add_fee(self, name, fct_address=None):
        return self._request('add-fee', {
            'tx-name': name,
            'address': fct_address or self.fct_address
        })

    def add_input(self, name, amount, fct_address=None):
        return self._request('add-input', {
            'tx-name': name,
            'amount': amount,
            'address': fct_address or self.fct_address
        })

    def add_output(self, name, amount, fct_address):
        return self._request('add-output', {
            'tx-name': name,
            'amount': amount,
            'address': fct_address
        })

    def address(self, address):
        """
        Retrieve the public and private parts of a Factoid or Entry
        Credit address stored in the wallet.
        """
        return self._request('address', {
            'address': address
        })

    def all_addresses(self):
        """
        Retrieve all of the Factoid and Entry Credit addresses stored
        in the wallet.
        """
        return self._request('all-addresses')

    def compose_transaction(self, name):
        return self._request('compose-transaction', {
            'tx-name': name
        })

    def delete_transaction(self, name):
        """
        Deletes a working transaction in the wallet. The full
        transaction will be returned, and then deleted.
        """
        return self._request('delete-transaction', {
            'tx-name': name
        })

    def generate_entry_credit_address(self):
        """
        Create a new Entry Credit Address and store it in the wallet.
        """
        return self._request('generate-ec-address')

    def generate_factoid_address(self):
        """
        Create a new Factoid Address and store it in the wallet.
        """
        return self._request('generate-factoid-address')

    def get_height(self):
        """
        Get the current hight of blocks that have been cached by the
        wallet while syncing.
        """
        return self._request('get-height')

    def import_addresses(self, secret_key):
        """
        Import Factoid and/or Entry Credit address secret keys into the
        wallet.
        """
        return self._request('import-addresses', {
            'addresses': [
                {'secret': secret_key
                 }]
        })

    def import_koinify(self, words):
        """
        Import a Koinify crowd sale address into the wallet.
        """
        return self._request('import-koinify', {
            'words': words
        })

    def new_transaction(self, name=None):
        return self._request('new-transaction', {
            'tx-name': name or self._xact_name()
        })

    def properties(self):
        """
        Retrieve current properties of factom-walletd, including the
        wallet and wallet API versions.
        """
        return self._request('properties')

    def sign_transaction(self, name, force = False):
        return self._request('sign-transaction', {
            'tx-name': name,
            'force': force,
        })

    def sub_fee(self, name, fct_address):
        return self._request('sub-fee', {
            'tx-name': name,
            'address': fct_address
        })

    def temporary_transactions(self):
        """
        Lists all the current working transactions in the wallet. These
        are transactions that are not yet sent.
        """
        return self._request('tmp-transactions')

    def transactions_by_range(self, startblock, endblock):
        """
        This will retrieve all transactions within a given block height
        range.
        """
        return self._request('transactions', {
            'start': startblock,
            'end': endblock
        })

    def transactions_by_txid(self, txid):
        """
        This will retrieve a transaction by the given TxID. This call
        is the fastest way to retrieve a transaction, but it will not
        display the height of the transaction. If a height is in the
        response, it will bE 0. To retrieve the height of a transaction,
         use the By Address method.
        """
        return self._request('transactions', {
            'txid': txid
        })

    def transactions_by_address(self, fct_address):
        """
        Retrieves all transactions that involve a particular address.
        """
        return self._request('transactions', {
            'address': fct_address
        })

    def wallet_backup(self):
        """
        Return the wallet seed and all addresses in the wallet for
        backup and offline storage.
        """
        return self._request('wallet-backup')

    def wallet_balances(self):
        """
        The wallet-balances API is used to query the acknowledged and
        saved balances for all addresses in the currently running
        factom-walletd. The saved balance is the last saved to the
        database and the acknowledged or ack balance is the balance
        after processing any in-flight transactions known to the Factom
        node responding to the API call. The factoid address balance
        will be returned in factoshis (a factoshi is 10^8 factoids) not
        factoids(FCT) and the entry credit balance will be returned in
        entry credits.

        If walletd and factomd are not both running this call will not
        work.

        If factomd is not loaded up all the way to last saved block it
        will return:
        result:{Factomd Error:Factomd is not fully booted, please wait
        and try again.}

        If an address is not in the correct format the call will return:
        result:{Factomd Error:There was an error decoding an address}

        If an address does not have a public and private address known
        to the wallet it will not be included in the balance.

        "fctaccountbalances" are the total of all factoid account
        balances returned in factoshis.

        "ecaccountbalances" are the total of all entry credit account
        balances returned in entry credits.
        """
        return self._request('wallet-balances')

    def new_chain(self, factomd, ext_ids, content, ec_address=None):
        """
        Shortcut method to create a new chain and initial entry.

        Args:
            factomd (Factomd): The `Factomd` instance where the creation
                message will be submitted.
            ext_ids (list[str]): A list of external IDs, unencoded.
            content (str): Entry content, unencoded.
            ec_address (str): Entry credit address to pay with. If not
                provided `self.ec_address` will be used.

        Returns:
            dict: API result from the final `reveal_chain()` call.
        """
        calls = self._request('compose-chain', {
            'chain': {
                'firstentry': {
                    'extids': [hex(x) for x in ext_ids],
                    'content': hex(content)
                },
            },
            'ecpub': ec_address or self.ec_address
        })
        factomd.commit_chain(calls['commit']['params']['message'])
        time.sleep(2)
        return factomd.reveal_chain(calls['reveal']['params']['entry'])

    def new_entry(self, factomd, chain_id, ext_ids, content, ec_address=None):
        """
        Shortcut method to create a new entry.

        Args:
            factomd (Factomd): The `Factomd` instance where the creation
                message will be submitted.
            chain_id (str): Chain ID where entry will be appended.
            ext_ids (list[str]): A list of external IDs, unencoded.
            content (str): Entry content, unencoded.
            ec_address (str): Entry credit address to pay with. If not
                provided `self.ec_address` will be used.

        Returns:
            dict: API result from the final `reveal_chain()` call.
        """
        calls = self._request('compose-entry', {
            'entry': {
                'chainid': chain_id,
                'extids': [hex(x) for x in ext_ids],
                'content': hex(content)
            },
            'ecpub': ec_address or self.ec_address
        })
        factomd.commit_entry(calls['commit']['params']['message'])
        time.sleep(2)
        return factomd.reveal_entry(calls['reveal']['params']['entry'])

    def fct_to_ec(self, factomd, amount, fct_address=None, ec_address=None):
        """
        Shortcut method to create a factoid to entry credit transaction.

        factomd (Factomd): The `Factomd` instance where the signed
            transaction will be submitted.
        amount (int): Amount of fct to submit for conversion. You'll
        likely want to first query the exchange rate via
            `Factomd.entry_credit_rate()`.
        fct_address (str): Factoid address to pay with. If not provided
            `self.fct_address` will be used.
        ec_address (str): Entry credit address to receive credits. If
        not provided `self.ec_address` will be used.

        Returns:
            dict: API result from the final `factoid_submit()` call.
        """
        name = self._xact_name()
        self.new_transaction(name)
        self.add_input(name, amount, fct_address)
        self.add_ec_output(name, amount, ec_address)
        self.add_fee(name, fct_address)
        self.sign_transaction(name)
        call = self.compose_transaction(name)
        return factomd.factoid_submit(call['params']['transaction'])

    def fct_to_fct(self, factomd, amount, fct_to, fct_from=None):
        """
        Shortcut method to create a factoid to factoid.

        factomd (Factomd): The `Factomd` instance where the signed
            transaction will be submitted.
        amount (int): Amount of fct to submit for conversion. You'll
        likely want to first query the exchange rate via
            `Factomd.entry_credit_rate()`.
        fct_to (str): Output factoid address.
        fct_from (str): Input factoid address. If not provided
            `self.fct_address` will be used.

        Returns:
            dict: API result from the final `factoid_submit()` call.
        """
        name = self._xact_name()
        self.new_transaction(name)
        self.add_input(name, amount, fct_from)
        self.add_output(name, amount, fct_to)
        self.add_fee(name, fct_from)
        self.sign_transaction(name)
        call = self.compose_transaction(name)
        return factomd.factoid_submit(call['params']['transaction'])
