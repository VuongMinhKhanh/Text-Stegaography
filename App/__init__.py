import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
from flask_login import LoginManager


app = Flask(__name__)
app.secret_key = "abcdefghijklmnopqrstuvwxyz"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:%s@localhost/blogdb?charset=utf8mb4" \
                                        % quote("Admin@123")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["PAGE_SIZE"] = 4
db = SQLAlchemy(app=app)
login = LoginManager(app=app)
app.config["KEY"] = 3
app.config["KEY_ASE"] = os.urandom(32)