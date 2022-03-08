from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

# Secret key required to encrypt user passwords and input
app.config['SECRET_KEY'] = "695f4d33049851be2b077d9ffe1d8cf2"

# SQLAlchemy configuration for database that passes argument called app (as mentioned above)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' # 3 /'s for route redirectory
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from main_app import routes
