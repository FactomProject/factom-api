import json
import pytest
import responses as responses_


def assert_jsonrpc_calls(resp_mock, calls):
    assert len(calls) == len(resp_mock.calls), "Unexpected call count"
    for call, expected in zip(resp_mock.calls, calls):
        data = json.loads(call.request.body.decode())
        assert expected == (data['method'], data['params'])


# flake8: noqa
FACTOMD_RESPONSES = {
    'chain-head': {
        'chainhead': '8d87077d6d35f225c74e7a7cbcd9538cdb5642f5541ba77fc815f3b57ac10eb6',
        'chaininprocesslist': False
    },
    'commit-chain': {
        'chainidhash': 'ff5d4299149cc84ed78cf4a4375d70ec506a5d79f229df9e9872302c3f8e7658',
        'entryhash': '7a6d60d93b0284b1a8827313db23d47f5894b409593c3751302ceedf44169c45',
        'message': 'Chain Commit Success',
        'txid': 'ca0e81e93b3f44790aad767221b7edf9c03b6edd50dec7cbcb40d04a779d780b'
    },
    'commit-entry': {
        'entryhash': '8d9eba64b972c217aae1d434926e8f855f9b88f7e061156f7ed5482fc52c7f52',
        'message': 'Entry Commit Success',
        'txid': 'c0ac46ebbb268621bbfaa0f9fcb88705041db8418b7dfd3476f120661244af3a'
    },
    'entry': {
        'chainid': '1726b29c0b0576e4451f348922551152b044d864690786117fde360845508c63',
        'content': '636861696e5f636f6e74656e74',
        'extids': ['636861696e', '6964']
    },
    'entry-block': {
        'entrylist': [
            {
                'entryhash': '7a6d60d93b0284b1a8827313db23d47f5894b409593c3751302ceedf44169c45',
                'timestamp': 1512902940
            }
        ],
        'header': {
            'blocksequencenumber': 0,
            'chainid': '1726b29c0b0576e4451f348922551152b044d864690786117fde360845508c63',
            'dbheight': 537,
            'prevkeymr': '0000000000000000000000000000000000000000000000000000000000000000',
            'timestamp': 1512902460
        }
    },
    'entry-credit-balance': {
        'balance': 100
    },
    'entry-credit-rate': {
        'rate': 1000
    },
    'factoid-balance': {
        'balance': 2000000000000
    },
    'factoid-submit': {
        'message': 'Successfully submitted the transaction',
        'txid': 'baedcf21a3308eca617c1a54a0b001aa732986e7eae9eb2e219000f5ebbcaf03'
    },
    'reveal-chain': {
        'chainid': '1726b29c0b0576e4451f348922551152b044d864690786117fde360845508c63',
        'entryhash': '7a6d60d93b0284b1a8827313db23d47f5894b409593c3751302ceedf44169c45',
        'message': 'Entry Reveal Success'
    },
    'reveal-entry': {
        'chainid': '1726b29c0b0576e4451f348922551152b044d864690786117fde360845508c63',
        'entryhash': '8d9eba64b972c217aae1d434926e8f855f9b88f7e061156f7ed5482fc52c7f52',
        'message': 'Entry Reveal Success'
    }
}


# flake8: noqa
WALLETD_RESPONSES = {
    'add-ec-output': {
        'ecoutputs': [
            {
                'address': 'EC1rs7S56bWgTXN8XvaqhFenzRoHiUpHV2dYvwS7cJpqfb9HaRhi',
                'amount': 50000
            }
        ],
        'feesrequired': 12000,
        'inputs': [
            {
                'address': 'FA2jK2HcLnRdS94dEcU27rF3meoJfpUcZPSinpb7AwQvPRY6RL1Q',
                'amount': 50000
            }
        ],
        'name': 'TX_5XK1IX',
        'outputs': None,
        'signed': False,
        'timestamp': 1512899995,
        'totalecoutputs': 50000,
        'totalinputs': 50000,
        'totaloutputs': 0,
        'txid': 'ae25de26e1db736936e5b0ee6d8e8f87915ffd8cbb2c1b753278974c5a23174b'
    },
    'add-fee': {
        'ecoutputs': [
            {
                'address': 'EC1rs7S56bWgTXN8XvaqhFenzRoHiUpHV2dYvwS7cJpqfb9HaRhi',
                'amount': 50000
            }
        ],
        'feespaid': 12000,
        'feesrequired': 12000,
        'inputs': [
            {
                'address': 'FA2jK2HcLnRdS94dEcU27rF3meoJfpUcZPSinpb7AwQvPRY6RL1Q',
                'amount': 62000
            }
        ],
        'name': 'TX_5XK1IX',
        'outputs': None,
        'signed': False,
        'timestamp': 1512899995,
        'totalecoutputs': 50000,
        'totalinputs': 62000,
        'totaloutputs': 0,
        'txid': 'baedcf21a3308eca617c1a54a0b001aa732986e7eae9eb2e219000f5ebbcaf03'
    },
    'add-input': {
        'ecoutputs': None,
        'feespaid': 50000,
        'feesrequired': 2000,
        'inputs': [
            {
                'address': 'FA2jK2HcLnRdS94dEcU27rF3meoJfpUcZPSinpb7AwQvPRY6RL1Q',
                'amount': 50000
            }
        ],
        'name': 'TX_5XK1IX',
        'outputs': None,
        'signed': False,
        'timestamp': 1512899995,
        'totalecoutputs': 0,
        'totalinputs': 50000,
        'totaloutputs': 0,
        'txid': '7a7e5782dc5e26e242dee09aeccf77e9ce0531e3a17c95fba822fd35679a41eb'
    },
    'add-output': {
        'ecoutputs': None,
        'feesrequired': 12000,
        'inputs': [
            {
                'address': 'FA2jK2HcLnRdS94dEcU27rF3meoJfpUcZPSinpb7AwQvPRY6RL1Q',
                'amount': 50000
            }
        ],
        'name': 'TX_5XK1IX',
        'outputs': [
            {
                'address': 'FA39PymAz9pqBPTQkupT7g72THwbM2XyRrUpodvBJHKWGLjpJAd5',
                'amount': 50000
            }
        ],
        'signed': False,
        'timestamp': 1512900560,
        'totalecoutputs': 0,
        'totalinputs': 50000,
        'totaloutputs': 50000,
        'txid': '2ed27042eba5553516812fdfe581c53e0800efd0dfaee1f9019076c57e194abe'
    },
    'compose-chain': {
        'commit': {
            'id': 76,
            'jsonrpc': '2.0',
            'method': 'commit-chain',
            'params': {'message': '00016040044481ff5d4299149cc84ed78cf4a4375d70ec506a5d79f229df9e9872302c3f8e7658384848597c35f8add855cce0fe3878c6fdff1b48003aaf6193ad7fbbd100ad1e7a6d60d93b0284b1a8827313db23d47f5894b409593c3751302ceedf44169c450b0cf8b115fc135b45b9f11e2aff638591cb382e238b4d31e4a3de4912a69740ffa39a8544c36048b2f1a63873abc0e8a8ac3fc709d222270509a6d295ea6d4db4b8833c64d48e8d189b0aaf4ff518b906c3208b5e761527c1433f5d14c638830f'}
        },
        'reveal': {
            'id': 77,
            'jsonrpc': '2.0',
            'method': 'reveal-chain',
            'params': {'entry': '001726b29c0b0576e4451f348922551152b044d864690786117fde360845508c63000b0005636861696e00026964636861696e5f636f6e74656e74'}
        }
    },
    'compose-entry': {
        'commit': {
            'id': 80,
            'jsonrpc': '2.0',
            'method': 'commit-entry',
            'params': {'message': '000160400778608d9eba64b972c217aae1d434926e8f855f9b88f7e061156f7ed5482fc52c7f52010cf8b115fc135b45b9f11e2aff638591cb382e238b4d31e4a3de4912a69740ffd0472bbe1e345f6a2435a85c8d071fab7cbd6554d323689f418f6a5fb97d4d0c5fbf41109853a9d7b6b9fdb802eb558d95bce64d5574af7b89c4c3e7ce6af70b'}
        },
        'reveal': {
            'id': 81,
            'jsonrpc': '2.0',
            'method': 'reveal-entry',
            'params': {'entry': '001726b29c0b0576e4451f348922551152b044d864690786117fde360845508c63000b0005656e74727900026964656e7472795f636f6e74656e74'}
        }
    },
    'compose-transaction': {
        'id': 2,
        'jsonrpc': '2.0',
        'method': 'factoid-submit',
        'params': {
            'transaction': '0201603fdde75301000183e430646f3e8750c550e4582eca5047546ffef89c13a175985e320232bacac81cc4288386500cf8b115fc135b45b9f11e2aff638591cb382e238b4d31e4a3de4912a69740ff01718b5edd2914acc2e4677f336c1a32736e5e9bde13663e6413894f57ec272e2866a77c4d8b128266f0431170d65f2aa742b71b6d9674e690d16af344353af7ef5792f4dee744012afce1465897a8f7d509a951aca7c12ca60df03119c78df607'
        }
    },
    'new-transaction': {
        'ecoutputs': None,
        'feesrequired': 1000,
        'inputs': None,
        'name': 'TX_5XK1IX',
        'outputs': None,
        'signed': False,
        'timestamp': 1512899995,
        'totalecoutputs': 0,
        'totalinputs': 0,
        'totaloutputs': 0,
        'txid': 'a3357318ed4eb8da89544b6a55023cef38f208c5601650f802b99932b77d963f'
    },
    'sign-transaction': {
        'ecoutputs': [
            {
                'address': 'EC1rs7S56bWgTXN8XvaqhFenzRoHiUpHV2dYvwS7cJpqfb9HaRhi',
                'amount': 50000
            }
        ],
        'feespaid': 12000,
        'feesrequired': 12000,
        'inputs': [
            {
                'address': 'FA2jK2HcLnRdS94dEcU27rF3meoJfpUcZPSinpb7AwQvPRY6RL1Q',
                'amount': 62000
            }
        ],
        'name': 'TX_5XK1IX',
        'outputs': None,
        'signed': True,
        'timestamp': 1512899995,
        'totalecoutputs': 50000,
        'totalinputs': 62000,
        'totaloutputs': 0,
        'txid': 'baedcf21a3308eca617c1a54a0b001aa732986e7eae9eb2e219000f5ebbcaf03'
    }
}


def _callback(choices):
    def _handle(request):
        method = json.loads(request.body.decode())['method']
        return (200, {}, json.dumps({
            'jsonrpc': '2.0',
            'id': 0,
            'result': choices[method]
        }))
    return _handle


@pytest.fixture()
def responses():
    with responses_.RequestsMock(assert_all_requests_are_fired=False) as resp_mock:  # noqa
        resp_mock.add_callback('POST', 'http://localhost:8088/v2',
                               callback=_callback(FACTOMD_RESPONSES))
        resp_mock.add_callback('POST', 'http://localhost:8089/v2',
                               callback=_callback(WALLETD_RESPONSES))
        yield resp_mock
