from chorerate import db, login_manager
from flask_login import UserMixin


class User(db.Model, UserMixin):
    '''Model for the user table'''
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)


@login_manager.user_loader
def load_user(user_id):
    '''Loads the user for the login manager'''
    return User.query.get(int(user_id))
