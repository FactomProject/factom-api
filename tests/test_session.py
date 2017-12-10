import pytest
from requests import Request

from factom.session import FactomAPISession


@pytest.fixture
def request():
    return Request('GET', 'http://someurl/')


def test_request_headers(request):
    s = FactomAPISession()
    r = s.prepare_request(request)

    assert r.headers['User-Agent'].startswith('factom-api/')
    assert r.headers['Accept-Charset'] == 'utf-8'
    assert r.headers['Content-Type'] == 'text/plain'


def test_basic_auth(request):
    s = FactomAPISession()
    s.init_basic_auth('user', 'pass')
    r = s.prepare_request(request)

    assert r.headers['Authorization'] == 'Basic dXNlcjpwYXNz'
