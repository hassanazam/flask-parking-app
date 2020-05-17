from flask import Flask
from flask_jwt import JWT
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import logging
from app.config.config_handler import ConfigHandler

# get App instance
app = Flask(__name__)

# Set logger
app.log = logging.getLogger('ParkingApp')

# Load config into app object
ConfigHandler(app)

# Initialize DB instance
db = SQLAlchemy(app)

# Initialize Migrate instance for tracking model changes
Migrate(app, db)

from app.controllers import authentication

# importing the models to make sure they are known to Flask-Migrate
from app.models import user, parking_area, parking_slot, booking, role

# import apis
from app.apis import user_apis, parking_area_apis, parking_slot_apis