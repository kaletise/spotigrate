import time
import traceback

import default
import module

import app.application
import build
import default.config
import storage.database
import utils.config
import utils.logger
import utils.utils
import web.server


MODULE_ERROR = (
    f'Unable to import the %s module. It seems like it is not '
    f'installed in your system. Please run "pip3 install -r '
    f'{utils.utils.get_current_directory()}requirements.txt" or '
    f'contact your system administrator for more information.'
)


class Main:
    def __init__(self):
        self.app = None
        try:
            self._init()
        except Exception as exception:
            logger = self._get_current_error_logger()
            logger(
                f'Unable to start web application: {exception}'
            )
            logger(
                f'Application crashed: {traceback.format_exc()}'
            )

    def _init(self):
        init_time = time.perf_counter()

        self.config = self._load_config()
        self.logger = self._load_logger()

        self.logger.info(
            f'Starting spotigrate/{build.VERSION} on '
            f'{utils.utils.get_platform()}...'
        )

        if self.config.first_init:
            return self.logger.info(
                'Further configuration is required before using Spotigrate. '
                'Please fill out the newly created configuration file '
                'config.json and run Spotigrate again'
            )

        database_time = time.perf_counter()
        self.database = self._load_database()
        self.logger.info(
            f'Connecting to database {self.database.host}...'
        )
        if not storage.database.loaded:
            return self.logger.error(MODULE_ERROR % 'pymongo')
        connected = self._test_database()
        database_complete_time = time.perf_counter()
        if connected:
            self.logger.info(
                f'Connected to database {self.database.host} in '
                f'{database_complete_time - database_time:0.4f} seconds'
            )

        app_time = time.perf_counter()
        self.logger.info(
            'Loading application...'
        )
        self.application = app.application.Application(
            config=self.config, database=self.database, logger=self.logger
        )
        app_complete_time = time.perf_counter()
        self.logger.info(
            f'Application loaded in '
            f'{app_complete_time - app_time:0.4f} seconds'
        )

        webserver_time = time.perf_counter()
        self.logger.info(
            'Loading webserver...'
        )
        if not web.server.loaded:
            return self.logger.error(MODULE_ERROR % 'flask')
        self.webserver = self._load_webserver()
        if connected:
            self.webserver.register_event('*', self.application.handler)
        else:
            self.webserver.register_event(
                '*', lambda request: self.application.error(
                    request, 'NO_DATABASE_CONNECTION'
                )
            )

        webserver_complete_time = time.perf_counter()
        self.logger.info(
            f'Webserver loaded in '
            f'{webserver_complete_time - webserver_time:0.4f} seconds'
        )

        init_complete_time = time.perf_counter()
        self.logger.info(
            f'Application started in '
            f'{init_complete_time - init_time:0.4f} seconds'
        )
        self.app = self.webserver.app

        # Monkey patching
        self.app.master = self

    def _load_config(self):
        return utils.config.Config(
            'config.json', default=default.config.DEFAULT
        )

    def _load_logger(self):
        return utils.logger.Logger(
            enabled=self.config.get('LOGGER_ENABLE'),
            level=self.config.get('LOGGER_LEVEL'),
            file=self.config.get('LOGGER_FILE')
        )

    def _load_database(self):
        return storage.database.MongoDatabase(
            host=self.config.get('DATABASE_HOST')
        )

    def _test_database(self):
        attempt = 0
        connected = False
        while attempt < 3:
            attempt += 1
            connection = self.database.connect()
            if isinstance(connection, str):
                if attempt != 3:
                    self.logger.warning(
                        f'Unable to connect to database '
                        f'{self.database.host}. Trying again in '
                        f'5 seconds...'
                    )
                    time.sleep(5)
                    connection = self.database.connect()
                else:
                    self.logger.error(
                        f'Unable to connect to database '
                        f'{self.database.host} in 3 attempts, giving up...'
                    )
            else:
                connected = True
                connection.close()
                break
        return connected

    def _load_webserver(self):
        return web.server.WebServer('spotigrate')

    def _get_current_error_logger(self):
        try:
            return self.logger.error
        except Exception:
            return print


try:
    application = Main().app
except KeyboardInterrupt:
    application = None
    print('Exiting...')
except Exception:
    application = None
    print('Application crashed')
