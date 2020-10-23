import pytest
from requests import Request

from factom.session import FactomAPISession


@pytest.fixture
def fake_request():
    return Request('GET', 'http://someurl/')


def test_request_headers(fake_request):
    s = FactomAPISession()
    r = s.prepare_request(fake_request)

    assert r.headers['Accept-Charset'] == 'utf-8'
    assert r.headers['Content-Type'] == 'text/plain'


def test_basic_auth(fake_request):
    s = FactomAPISession()
    s.init_basic_auth('user', 'pass')
    r = s.prepare_request(fake_request)

    assert r.headers['Authorization'] == 'Basic dXNlcjpwYXNz'
