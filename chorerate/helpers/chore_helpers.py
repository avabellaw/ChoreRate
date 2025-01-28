
from chorerate.models.chore import Chore
from chorerate.models.chore_rating import ChoreRating
from chorerate import db


def get_unrated_chores_from_db(household_member):
    '''Get unrated chores for the given household member'''
    household_member_id = household_member.id
    current_household_id = household_member.household_id
    
    # Subquery to find all chore IDs that the current user has rated
    rated_chore_ids_subquery = db.session.query(
        ChoreRating.chore_id).filter_by(
            household_member_id=household_member_id).subquery()

    # Find all unrated chores in the user's household
    unrated_chores = db.session.query(Chore).filter(
        Chore.household_id == current_household_id,
        ~Chore.id.in_(rated_chore_ids_subquery.select())
    ).all()

    return unrated_chores
