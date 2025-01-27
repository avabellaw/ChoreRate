
from chorerate.models.chore import Chore
from chorerate.models.chore_rating import ChoreRating
from chorerate.helpers.household_helpers import current_household_member, current_household
from chorerate import db


def get_unrated_from_db():
    '''Get unrated chores for the current user'''
    current_member = current_household_member()
    current_member_id = current_member.id
    current_household_id = current_member.household_id

    # Subquery to find all chore IDs that the current user has rated
    rated_chore_ids_subquery = db.session.query(ChoreRating.chore_id).filter_by(household_member_id=current_member_id).subquery()

    # Find all unrated chores in the user's household
    unrated_chores = db.session.query(Chore).filter(
        Chore.household_id == current_household_id,
        ~Chore.id.in_(rated_chore_ids_subquery)
    ).all()

    return unrated_chores
