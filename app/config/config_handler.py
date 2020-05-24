import os

# Constants
APP_CONFIG_PATH = "APP_CONFIG_PATH"
SECRET_KEY = "SECRET_KEY"
SQLALCHEMY_DATABASE_URI = "SQLALCHEMY_DATABASE_URI"
APP_ENV = "APP_ENV"
PARKING_NUMBER_MAX_LENGTH = "PARKING_NUMBER_MAX_LENGTH"
MAIL_SERVER = "MAIL_SERVER"
MAIL_SERVER_PORT = "MAIL_SERVER_PORT"
DEFAULT_SENDER_EMAIL = "DEFAULT_SENDER_EMAIL"
DEFAULT_SENDER_EMAIL_PASSWORD = "DEFAULT_SENDER_EMAIL_PASSWORD"


class ConfigHandler(object):

    REQUIRED_CONFIG_PARAMETERS = [
        SECRET_KEY,
        SQLALCHEMY_DATABASE_URI,
        APP_ENV,
        PARKING_NUMBER_MAX_LENGTH,
        MAIL_SERVER,
        MAIL_SERVER_PORT,
        DEFAULT_SENDER_EMAIL,
        DEFAULT_SENDER_EMAIL_PASSWORD
    ]

    found_config_path = False

    def __init__(self, app):
        self.validate_env_variables()
        self.set_app_config(app)
        self.validate_config_file_vars(app)

    @staticmethod
    def set_app_config(app):
        if ConfigHandler.found_config_path:
            app.config.from_envvar(APP_CONFIG_PATH)
        else:
            # Try to load config file from project root
            app.config.from_pyfile((os.path.join(app.instance_path, 'app_config_default.py')))

    @staticmethod
    def validate_env_variables():
        app_env = os.environ.get(APP_CONFIG_PATH)
        if not app_env:
            print("APP_CONFIG_PATH environment variable not found!")
            print(" Trying to load config file from project root directory ... ")
            # os.abort()
            return

        ConfigHandler.found_config_path = True

    @staticmethod
    def validate_config_file_vars(app):
        for var in ConfigHandler.REQUIRED_CONFIG_PARAMETERS:
            if not app.config.get(var):
                app.log.error("Missing {} from external config file.".format(var))
                os.abort()
