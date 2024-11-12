'''Contains the database models'''
import enum as python_enum

from flask_login import UserMixin
from sqlalchemy import Enum

from chorerate import db, login_manager


class Frequency(python_enum.Enum):
    '''Enum for the frequency of a chore'''
    DAILY = 'daily'
    WEEKLY = 'weekly'
    MONTHLY = 'monthly'


class User(db.Model, UserMixin):
    '''Model for the user table'''
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)


class Chore(db.Model):
    '''Model for the chore table'''
    __tablename__ = 'chores'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    frequency = db.Column(Enum(Frequency), nullable=False)
    times_per_frequency = db.Column(db.SmallInteger, nullable=False)

    def __repr__(self):
        return f"<{self.name} {self.frequency} - {self.times_per_frequency}x>"


@login_manager.user_loader
def load_user(user_id):
    '''Loads the user for the login manager'''
    return User.query.get(int(user_id))
