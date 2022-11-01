from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)

# SQLAlchemy configuration for database that passes argument called app (as mentioned above)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' # 3 /'s for route redirectory

# Secret key required to encrypt user passwords and input
app.config['SECRET_KEY'] = "695f4d33049851be2b077d9ffe1d8cf2"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login' # redirects user to login page if the user isn't logged in
login_manager.login_message_category = 'info' # displays message in a neat colour category
app.config['MAIL_SERVER'] = 'mail.glasse.co.nz'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USERNAME'] = 'mark@glasse.co.nz'
app.config['MAIL_PASSWORD'] = 'MarGla55'

mail = Mail(app)

from main_app import routes
