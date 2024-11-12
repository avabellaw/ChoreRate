'''Contains the database models'''
import enum as python_enum

from flask_login import UserMixin
from sqlalchemy import Enum

from chorerate import db, login_manager


class FrequencyEnum(python_enum.Enum):
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
    frequency = db.Column(Enum(FrequencyEnum), nullable=False)
    times_per_frequency = db.Column(db.SmallInteger, nullable=False)

    def __repr__(self):
        return f"<{self.name} {self.frequency} - {self.times_per_frequency}x>"
    

class ChoreRating(db.Model):
    '''Model for the chore rating table'''
    __tablename__ = 'chore_ratings'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    chore_id = db.Column(db.Integer,
                         db.ForeignKey('chores.id'),
                         nullable=False)
    rating = db.Column(db.SmallInteger,
                       db.CheckConstraint('rating >= 1 AND rating <= 10'),
                       nullable=False)

    def __repr__(self):
        return f"<{self.user_id} rated '{self.chore_id}': {self.rating}>"


@login_manager.user_loader
def load_user(user_id):
    '''Loads the user for the login manager'''
    return User.query.get(int(user_id))
