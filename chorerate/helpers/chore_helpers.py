
from chorerate.models.chore import Chore
from chorerate.models.chore_rating import ChoreRating
from chorerate.models.allocated_chore import AllocatedChore
from chorerate.models.household_member import HouseholdMember
from chorerate import db


def get_unrated_chores_for_member(household_member):
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


def get_unrated_chores_for_household(household):
    '''
        Get unrated chores for the given household

        Returns: A dictionary of unrated chores by member ID key
    '''
    household_id = household.id
    unrated_chores_by_member = {}

    # Subquery to find all rated chores in the household
    rated_chores_subquery = db.session.query(
        ChoreRating.chore_id,
        ChoreRating.household_member_id
    ).join(HouseholdMember).filter(
        HouseholdMember.household_id == household_id
    ).subquery()

    # Find all unrated chores for each member
    for member in household.members:
        unrated_chores = db.session.query(Chore).filter(
            Chore.household_id == household_id,
            ~Chore.id.in_(
                db.session.query(rated_chores_subquery.c.chore_id).filter(
                    rated_chores_subquery.c.household_member_id == member.id
                )
            )
        ).all()
        if unrated_chores:
            unrated_chores_by_member[member.id] = unrated_chores

    return unrated_chores_by_member


def delete_chore(chore_id):
    '''Deletes a chore and its associated ratings and allocations'''
    chore = Chore.query.get(chore_id)
    chore_ratings = ChoreRating.query.filter_by(chore_id=chore_id).all()
    chore_allocations = AllocatedChore.query.filter_by(chore_id=chore_id).all()

    db.session.delete(chore, chore_ratings, chore_allocations)
    db.session.commit()
