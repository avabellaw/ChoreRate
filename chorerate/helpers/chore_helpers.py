
from chorerate.models.chore import Chore
from chorerate.models.chore_rating import ChoreRating
from chorerate.helpers.household_helpers import current_household_member
from chorerate import db


def get_unrated_from_db():
    '''Get unrated chores for the current user'''
    current_member_id = current_household_member().id
    rated = db.session.query(ChoreRating.chore_id).filter_by(
        household_member_id=current_member_id)
    unrated = db.session.query(Chore).filter(~Chore.id.in_(rated)).all()

    return unrated
