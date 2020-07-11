# Import Flask for flask app object
from flask import Flask
from config import Config
from flask_login import LoginManager
from pymongo import MongoClient

# Create flask app object
app = Flask(__name__)
app.config.from_object(Config)

# Create Login manager
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'warning'

# Create client for Mongodb
client = MongoClient()
# connect to local host
client = MongoClient('localhost', 27017)

# Import all views
import opportunity.views