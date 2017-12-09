from binascii import hexlify


def _hex(val):
    try:
        val = val.encode('utf8')
    except AttributeError:
        pass
    return hexlify(val).decode('ascii')


def hex(val):
    if isinstance(val, list):
        return [_hex(v) for v in val]
    return _hex(val)
