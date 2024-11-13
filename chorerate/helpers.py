'''Helper functions'''

from flask_login import current_user
from chorerate import db
from chorerate.models import Chore, ChoreRating


def get_unrated_from_db():
    '''Get unrated chores for the current user'''
    user_id = current_user.id
    rated = db.session.query(ChoreRating.chore_id).filter_by(user_id=user_id)
    unrated = db.session.query(Chore).filter(~Chore.id.in_(rated)).all()

    return unrated
