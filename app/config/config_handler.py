import os

# Constants
APP_CONFIG_PATH = "APP_CONFIG_PATH"
SECRET_KEY = "SECRET_KEY"
SQLALCHEMY_DATABASE_URI = "SQLALCHEMY_DATABASE_URI"


class ConfigHandler(object):

    REQUIRED_ENV_VARIABLES = [
        SECRET_KEY,
        SQLALCHEMY_DATABASE_URI
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
            return

        ConfigHandler.found_config_path = True

    @staticmethod
    def validate_config_file_vars(app):
        for var in ConfigHandler.REQUIRED_ENV_VARIABLES:
            if not app.config.get(var):
                app.log.error("Missing {} from external config file.".format(var))
                os.abort()
