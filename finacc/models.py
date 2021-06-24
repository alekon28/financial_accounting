from flask_login import UserMixin
from finacc import db, lm
from sqlalchemy import CheckConstraint
from dataclasses import dataclass
from datetime import datetime


@dataclass
class User(db.Model, UserMixin):
    id: int
    username: str
    email: str
    password: str

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    projects = db.relationship('Project', backref='User', lazy=True)


@dataclass
class Project(db.Model):
    id: int
    user_id: int
    name: str

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(120), unique=True, nullable=False)
    transaction = db.relationship('Transaction', backref='Project', lazy=True)


@dataclass
class Transaction(db.Model):
    id: int
    project_id: int
    name: str
    freq_type: str
    trans_type: str
    date: datetime
    value: int
    comment: str

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.String(80), db.ForeignKey('project.id'), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    freq_type = db.Column(db.String(120), nullable=False)
    trans_type = db.Column(db.String(120), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now())
    value = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(1024), nullable=False)
    CheckConstraint("freq_type = 'random' or freq_type = 'regular' or freq_type = 'savings'", name='freq_type_c')
    CheckConstraint("trans_type = 'income' or trans_type = 'expense'", name='trans_type_c')


@lm.user_loader
def load_user(user_id):
    return User.query.get(user_id)
