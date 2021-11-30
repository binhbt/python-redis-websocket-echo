import json

try:
    from collections import OrderedDict
except ImportError:
    OrderedDict = dict
OK = {
    'status': '200 OK',
    'code': 200,
}

ERR_UNKNOWN = {
    'status': '500 Internal Server Error',
    'code': 500,
    'title': 'Unknown Error'
}

ERR_AUTH_REQUIRED = {
    'status': '401 Unauthorized',
    'code': 901,
    'error_type': 'AuthException'
}
ERR_MISSING_API_KEY = {
    'status': '401 Unauthorized',
    'code': 401,
    'error_type': 'AuthException'
}
ERR_INVALID_PARAMETER = {
    'status': '400 Bad Request',
    'code': 885,
    'error_type': 'InvalidParameterException'
}

ERR_SERVER_UNKNOW = {
    'status': '500 Internal Server Error',
    'code': 500,
    'error_type': 'Internal server error'
}
ERR_TOKEN_INVALID = {
    'status': '401 Unauthorized',
    'code': 401,
    'error_type': 'AuthException'
}
class AppError(Exception):
    def __init__(self, error=ERR_UNKNOWN, description=None):
        self.error = error
        self.error['description'] = description

    @property
    def code(self):
        return self.error['code']

    # @property
    # def title(self):
    #     return self.error['title']
    @property
    def error_type(self):
        return self.error['error_type']

    @property
    def status(self):
        return self.error['status']

    @property
    def description(self):
        return self.error['description']

    @staticmethod
    def handle(exception, req, res, error=None):
        res.status = exception.status
        meta = OrderedDict()
        meta['code'] = exception.code
        # meta['message'] = exception.title
        meta['error_type'] = exception.error_type
        if exception.description:
            meta['error_message'] = exception.description
        res.body = json.dumps({'meta': meta})


class UnauthorizedError(AppError):
    def __init__(self, description=None):
        super().__init__(ERR_AUTH_REQUIRED)
        self.error['description'] = description


class MissingApiKey(AppError):
    def __init__(self, description=None):
        super().__init__(ERR_MISSING_API_KEY)
        self.error['description'] = description


class InvalidParameterError(AppError):
    def __init__(self, description=None):
        super().__init__(ERR_INVALID_PARAMETER)
        self.error['description'] = description

class ServerUnknowError(AppError):
    def __init__(self, description=None):
        super().__init__(ERR_SERVER_UNKNOW)
        self.error['description'] = description
class TokenInvalidError(AppError):
    def __init__(self, description=None):
        super().__init__(ERR_TOKEN_INVALID)
        self.error['description'] = description