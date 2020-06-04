from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bafcdaac27ca2fbcc30e6e3543810b11'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///auction.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from ccc_auction import routes