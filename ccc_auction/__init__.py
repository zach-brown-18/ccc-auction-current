from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from whitenoise import WhiteNoise

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bafcdaac27ca2fbcc30e6e3543810b11'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///auction.db'
app.static_folder = 'static'
app.wsgi_app = WhiteNoise(app.wsgi_app, root='static/')
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

from ccc_auction import routes