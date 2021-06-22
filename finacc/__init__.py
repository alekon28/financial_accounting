from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)
app.secret_key = "LkdrmcPb0O"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/diana/projects/financial_accounting/database/main.db'
db = SQLAlchemy(app)
lm = LoginManager(app)

from finacc import models, routes

db.create_all()