# Import Flask for flask app object
from flask import Flask
from config import Config
from dbmodels.manager import client

# Create flask app object
app = Flask(__name__)
app.config.from_object(Config)

# Create Login manager
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'warning'

# Import all views
import opportunity.views