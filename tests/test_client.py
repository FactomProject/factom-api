from factom.client import BaseAPI


def test_init():
    c = BaseAPI(ec_address='EC_ADDR', fa_address='FA_ADDR',
                host='http://somehost/', version='v2', username='user',
                password='pass', certfile='/cert.pem')

    assert c.ec_address == 'EC_ADDR'
    assert c.fa_address == 'FA_ADDR'
    assert c.host == 'http://somehost/'
    assert 'Authorization' in c.session.headers
    assert c.session.verify == '/cert.pem'


def test_url():
    c = BaseAPI(host='http://somehost', version='v3')

    assert c.url == 'http://somehost/v3'
