from flask import Flask
from flask_jwt import JWT
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import logging
from app.config.config_handler import ConfigHandler
from app.controllers.authentication import AuthenticationController


# get App instance
app = Flask(__name__)

# Set logger
app.log = logging.getLogger('ParkingApp')

# Load config into app object
ConfigHandler(app)

# Initialize DB instance
db = SQLAlchemy(app)

# Initialize Migrate instance for tracking model changes
migrate = Migrate(app, db)

# Initialize Flask JWT instance
jwt = JWT(app, AuthenticationController.authenticate, AuthenticationController.get_authenticated_user)
