import pytest
try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

from . import assert_jsonrpc_calls, responses  # noqa

from factom.client import Factomd, FactomWalletd


FA_1 = 'FA2jK2HcLnRdS94dEcU27rF3meoJfpUcZPSinpb7AwQvPRY6RL1Q'
FA_2 = 'FA39PymAz9pqBPTQkupT7g72THwbM2XyRrUpodvBJHKWGLjpJAd5'
EC_1 = 'EC1rs7S56bWgTXN8XvaqhFenzRoHiUpHV2dYvwS7cJpqfb9HaRhi'
TX = '0201603fdde75301000183e430646f3e8750c550e4582eca5047546ffef89c13a175985e320232bacac81cc4288386500cf8b115fc135b45b9f11e2aff638591cb382e238b4d31e4a3de4912a69740ff01718b5edd2914acc2e4677f336c1a32736e5e9bde13663e6413894f57ec272e2866a77c4d8b128266f0431170d65f2aa742b71b6d9674e690d16af344353af7ef5792f4dee744012afce1465897a8f7d509a951aca7c12ca60df03119c78df607'  # noqa
CHAIN_ID = '1726b29c0b0576e4451f348922551152b044d864690786117fde360845508c63'
ENTRY_1 = '7a6d60d93b0284b1a8827313db23d47f5894b409593c3751302ceedf44169c45'
ENTRY_2 = '8d9eba64b972c217aae1d434926e8f855f9b88f7e061156f7ed5482fc52c7f52'
COMMIT_CHAIN_MSG = '00016040044481ff5d4299149cc84ed78cf4a4375d70ec506a5d79f229df9e9872302c3f8e7658384848597c35f8add855cce0fe3878c6fdff1b48003aaf6193ad7fbbd100ad1e7a6d60d93b0284b1a8827313db23d47f5894b409593c3751302ceedf44169c450b0cf8b115fc135b45b9f11e2aff638591cb382e238b4d31e4a3de4912a69740ffa39a8544c36048b2f1a63873abc0e8a8ac3fc709d222270509a6d295ea6d4db4b8833c64d48e8d189b0aaf4ff518b906c3208b5e761527c1433f5d14c638830f'  # noqa
REVEAL_CHAIN_MSG = '001726b29c0b0576e4451f348922551152b044d864690786117fde360845508c63000b0005636861696e00026964636861696e5f636f6e74656e74'  # noqa
COMMIT_ENTRY_MSG = '000160400778608d9eba64b972c217aae1d434926e8f855f9b88f7e061156f7ed5482fc52c7f52010cf8b115fc135b45b9f11e2aff638591cb382e238b4d31e4a3de4912a69740ffd0472bbe1e345f6a2435a85c8d071fab7cbd6554d323689f418f6a5fb97d4d0c5fbf41109853a9d7b6b9fdb802eb558d95bce64d5574af7b89c4c3e7ce6af70b'  # noqa
REVEAL_ENTRY_MSG = '001726b29c0b0576e4451f348922551152b044d864690786117fde360845508c63000b0005656e74727900026964656e7472795f636f6e74656e74'  # noqa
ENTRY_KEYMR = '8d87077d6d35f225c74e7a7cbcd9538cdb5642f5541ba77fc815f3b57ac10eb6'  # noqa


@pytest.fixture
def factomd():
    return Factomd(ec_address=EC_1, fct_address=FA_1)


@pytest.fixture
def walletd():
    with patch.object(FactomWalletd, '_xact_name', return_value='TX_5XK1IX'):
        yield FactomWalletd(ec_address=EC_1, fct_address=FA_1)


def test_fct_to_ec(responses, factomd, walletd):  # noqa
    res = walletd.fct_to_ec(factomd, 50000)

    assert res == {
        'message': 'Successfully submitted the transaction',
        'txid': 'baedcf21a3308eca617c1a54a0b001aa732986e7eae9eb2e219000f5ebbcaf03'  # noqa
    }
    assert_jsonrpc_calls(responses, [
        ('new-transaction', {'tx-name': 'TX_5XK1IX'}),
        ('add-input', {
            'tx-name': 'TX_5XK1IX',
            'address': FA_1,
            'amount': 50000
        }),
        ('add-ec-output', {
            'tx-name': 'TX_5XK1IX',
            'address': EC_1,
            'amount': 50000
        }),
        ('add-fee', {'tx-name': 'TX_5XK1IX', 'address': FA_1}),
        ('sign-transaction', {'tx-name': 'TX_5XK1IX'}),
        ('compose-transaction', {'tx-name': 'TX_5XK1IX'}),
        ('factoid-submit', {'transaction': TX})
    ])


def test_fct_to_fct(responses, factomd, walletd):  # noqa
    res = walletd.fct_to_fct(factomd, 50000, FA_2)

    assert res == {
        'message': 'Successfully submitted the transaction',
        'txid': 'baedcf21a3308eca617c1a54a0b001aa732986e7eae9eb2e219000f5ebbcaf03'  # noqa
    }
    assert_jsonrpc_calls(responses, [
        ('new-transaction', {'tx-name': 'TX_5XK1IX'}),
        ('add-input', {
            'tx-name': 'TX_5XK1IX',
            'address': FA_1,
            'amount': 50000
        }),
        ('add-output', {
            'tx-name': 'TX_5XK1IX',
            'address': FA_2,
            'amount': 50000
        }),
        ('add-fee', {'tx-name': 'TX_5XK1IX', 'address': FA_1}),
        ('sign-transaction', {'tx-name': 'TX_5XK1IX'}),
        ('compose-transaction', {'tx-name': 'TX_5XK1IX'}),
        ('factoid-submit', {'transaction': TX})
    ])


def test_new_chain(responses, factomd, walletd):  # noqa
    res = walletd.new_chain(factomd, ['chain', 'id'], 'chain_content')

    assert res == {
        'chainid': CHAIN_ID,
        'entryhash': ENTRY_1,
        'message': 'Entry Reveal Success'
    }
    assert_jsonrpc_calls(responses, [
        ('compose-chain', {
            'chain': {
                'firstentry': {
                    'extids': ['636861696e', '6964'],
                    'content': '636861696e5f636f6e74656e74'
                }
            },
            'ecpub': EC_1
        }),
        ('commit-chain', {'message': COMMIT_CHAIN_MSG}),
        ('reveal-chain', {'entry': REVEAL_CHAIN_MSG})
    ])


def test_new_entry(responses, factomd, walletd):  # noqa
    res = walletd.new_entry(factomd, CHAIN_ID, ['entry', 'id'],
                            'entry_content')

    assert res == {
        'chainid': CHAIN_ID,
        'entryhash': ENTRY_2,
        'message': 'Entry Reveal Success'
    }
    assert_jsonrpc_calls(responses, [
        ('compose-entry', {
            'entry': {
                'chainid': CHAIN_ID,
                'extids': ['656e747279', '6964'],
                'content': '656e7472795f636f6e74656e74'
            },
            'ecpub': EC_1
        }),
        ('commit-entry', {'message': COMMIT_ENTRY_MSG}),
        ('reveal-entry', {'entry': REVEAL_ENTRY_MSG})
    ])


def test_read_chain(responses, factomd, walletd):  # noqa
    res = factomd.read_chain(CHAIN_ID)

    assert res == [{
        'chainid': CHAIN_ID,
        'extids': ['chain', 'id'],
        'content': 'chain_content'
    }]
    assert_jsonrpc_calls(responses, [
        ('chain-head', {'chainid': CHAIN_ID}),
        ('entry-block', {'keymr': ENTRY_KEYMR}),
        ('entry', {'hash': ENTRY_1})
    ])
