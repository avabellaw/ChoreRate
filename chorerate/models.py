'''Contains the database models'''
import os

import enum as python_enum
from datetime import datetime, timedelta

from flask_login import UserMixin
from sqlalchemy import Enum

from chorerate import db, login_manager

DEBUG = os.environ['DEBUG']


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


class Household(db.Model):
    '''Model for the household table'''
    __tablename__ = 'households'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)

    chores = db.relationship('Chore', backref='household')


class HouseholdMember(db.Model):
    '''Model for the household member table'''
    __tablename__ = 'household_members'
    id = db.Column(db.Integer, primary_key=True)
    household_id = db.Column(db.Integer,
                             db.ForeignKey('households.id'),
                             nullable=False)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'),
                        nullable=False)
    __table_args__ = (
        db.UniqueConstraint('household_id',
                            'user_id',
                            name='unique_household_member'),
    )


class Chore(db.Model):
    '''Model for the chore table'''
    __tablename__ = 'chores'
    id = db.Column(db.Integer, primary_key=True)
    household_id = db.Column(db.Integer,
                             db.ForeignKey('households.id'),
                             nullable=False)
    name = db.Column(db.String(50), nullable=False)
    frequency = db.Column(Enum(FrequencyEnum), nullable=False)
    times_per_frequency = db.Column(db.SmallInteger, nullable=False)
    duration_minutes = db.Column(db.SmallInteger, nullable=False)

    allocation = db.relationship('AllocatedChore',
                                 backref='chore',
                                 uselist=False)

    def __repr__(self):
        return f"<{self.name} {self.frequency} - {self.times_per_frequency}x>"


class ChoreRating(db.Model):
    '''Model for the chore rating table'''
    __tablename__ = 'chore_ratings'
    id = db.Column(db.Integer, primary_key=True)
    household_member_id = db.Column(db.Integer, db.ForeignKey('household_members.id'), nullable=False)
    chore_id = db.Column(db.Integer,
                         db.ForeignKey('chores.id'),
                         nullable=False)
    rating = db.Column(db.SmallInteger,
                       db.CheckConstraint('rating >= 1 AND rating <= 10'),
                       nullable=False)

    chore = db.relationship('Chore', backref='ratings')

    def __repr__(self):
        return f"<{self.user_id} rated '{self.chore_id}': {self.rating}>"


class AllocatedChore(db.Model):
    '''Model for the allocated chore table'''
    __tablename__ = 'allocated_chores'
    id = db.Column(db.Integer, primary_key=True)
    Household_member_id = db.Column(db.Integer, db.ForeignKey('household_members.id'), nullable=False)
    chore_id = db.Column(db.Integer, db.ForeignKey('chores.id'), nullable=False)
    due_date = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f"<{self.user_id} has been allocated '{self.chore_id}'>"


@login_manager.user_loader
def load_user(user_id):
    '''Loads the user for the login manager'''
    return User.query.get(int(user_id))
