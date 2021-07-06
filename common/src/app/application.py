import base64
import json
import traceback

import flask


class API:
    methods = {}

    @staticmethod
    def method():
        def _method(func):
            API.methods[func.__qualname__.lower()] = func
            return func
        return _method


class Module:
    modules = {}

    @staticmethod
    def module(name):
        def _module(_class):
            Module.modules[name] = _class
            return _class
        return _module


class Application:
    def __init__(self, **kwargs):
        self.classes = {}

        for key, value in kwargs.items():
            self.classes[key] = value
            setattr(self, key, value)

        self.methods = API.methods
        self.modules = Module.modules

        self.running = True

        if self.config.get('PRODUCTION'):
            self.client = self.config.get('PRODUCTION_CLIENT')
        else:
            self.client = self.config.get('DEVELOPMENT_CLIENT')

        self.authorization = 'Basic ' + base64.b64encode(
            self.config.get('SPOTIFY_APP_ID').encode() + b':' +
            self.config.get('SPOTIFY_APP_SECRET').encode()
        ).decode()

        self.db = self.database.connect()[self.config.get('DATABASE_NAME')]

        for name, module in self.modules.items():
            module.start(self)

    def handler(self, request):
        try:
            handler = API.methods.get(request.path.lower())
            if handler:
                response = json.dumps(handler(self, request))
                self.logger.debug(
                    f'Request: {request.path} ({json.dumps(request.data)}); '
                    f'Response: {response}'
                )
                return flask.Response(
                    response,
                    mimetype='application/json'
                )
        except Exception:
            exception = traceback.format_exc()
            self.logger.error(f'Error during {request.path}: ' + exception)
        return flask.Response(
            json.dumps({'status': 0}),
            mimetype='application/json'
        )

    def error(self, request, cause=None):
        if cause == 'NO_DATABASE_CONNECTION':
            return 'NO_DATABASE_CONNECTION'
        return 'error'
