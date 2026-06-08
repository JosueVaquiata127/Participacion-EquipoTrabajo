from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

login_Manager = LoginManager()
login_Manager.login_view = "auth.login"