import json

import pytest
from requests import Response

from factom.exceptions import InvalidRequest, handle_error_response


def _response(content):
    r = Response()
    r._content = json.dumps(content).encode()
    return r


def test_handle_error_response():
    r = _response({'error': {
        'code': -32600,
        'message': "Invalid request",
        'data': 'field: field invalid'
    }})

    with pytest.raises(InvalidRequest) as exc_info:
        handle_error_response(r)

    e = exc_info.value
    assert str(e) == '-32600: Invalid request'
    assert e.data == 'field: field invalid'
    assert e.response == r
