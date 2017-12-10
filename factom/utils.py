from binascii import hexlify, unhexlify


def _hex(val):
    try:
        val = val.encode()
    except AttributeError:
        pass
    return hexlify(val).decode()


def hex(val):
    if isinstance(val, list):
        return [_hex(v) for v in val]
    return _hex(val)


def _unhex(val):
    return unhexlify(val).decode()


def unhex(val):
    if isinstance(val, list):
        return [_unhex(v) for v in val]
    return _unhex(val)
