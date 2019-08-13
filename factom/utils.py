from typing import Union


def hex_from_bytes_or_string(x: Union[bytes, str]):
    return x if type(x) is str else x.hex()
