def handle_error_response(resp):
    codes = {
        -1: FactomAPIError,
        -32008: BlockNotFound,
        -32009: MissingChainHead,
        -32010: ReceiptCreationError,
        -32011: RepeatedCommit,
        -32600: InvalidRequest,
        -32601: MethodNotFound,
        -32602: InvalidParams,
        -32603: InternalError,
        -32700: ParseError,
    }

    error = resp.json().get('error', {})
    message = error.get('message')
    code = error.get('code', -1)
    data = error.get('data', {})

    raise codes[code](message=message, code=code, data=data, response=resp)


class FactomAPIError(Exception):
    response = None
    data = {}
    code = -1
    message = "An unknown error occurred"

    def __init__(self, message=None, code=None, data={}, response=None):
        self.response = response
        if message:
            self.message = message
        if code:
            self.code = code
        if data:
            self.data = data

    def __str__(self):
        if self.code:
            return '{}: {}'.format(self.code, self.message)
        return self.message


class BlockNotFound(FactomAPIError):
    pass


class MissingChainHead(FactomAPIError):
    pass


class ReceiptCreationError(FactomAPIError):
    pass


class RepeatedCommit(FactomAPIError):
    pass


class InvalidRequest(FactomAPIError):
    pass


class MethodNotFound(FactomAPIError):
    pass


class InvalidParams(FactomAPIError):
    pass


class InternalError(FactomAPIError):
    pass


class ParseError(FactomAPIError):
    pass
