from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config


# Instantiate Objects
flask_app = Flask(__name__)
flask_app.config.from_object(Config)

db = SQLAlchemy(flask_app)
migrate = Migrate(flask_app, db)

login = LoginManager(flask_app)



from app import routes, models
