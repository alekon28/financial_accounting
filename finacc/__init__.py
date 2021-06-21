from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/sasha/PycharmProjects/financial_accounting/database/main.db'
db = SQLAlchemy(app)
lm = LoginManager(app)

from finacc import models, routes

db.create_all()