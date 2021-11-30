from pub.util.token_utils import decode_auth_token
from flask import request
from werkzeug.wrappers import Request
from pub.config import APP_AUTH
from pub.err.errs import *

class AuthMiddleWare(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        print('envi')
        print(environ)
        print('respon')
        print(start_response)
        req = Request(environ, shallow=True)

        path = req.path
        print("route")
        print(path)
        if not APP_AUTH['TOKEN_ON']:
            return self.app(environ, start_response)
        if "/send" in path:
            return self.app(environ, start_response)
        if "/api/v1/devices/validate" in path:
            return self.app(environ, start_response)

        print("Authorization---req.headers: %s", req.headers)
        if "X-API-KEY" in req.headers:
            request_api_key = req.headers["X-API-KEY"]
            if request_api_key is not None:
                isok, resp = decode_auth_token(request_api_key)
                if not isok:
                    raise UnauthorizedError(resp)
                else:
                    req.context['auth_user'] = request_api_key
            else:
                req.context['auth_user'] = None
        else:
            raise MissingApiKey('Your request did not include an x-api-key')

        return self.app(environ, start_response)