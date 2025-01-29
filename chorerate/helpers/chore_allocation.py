from chorerate import db

from chorerate.models.household_member import HouseholdMember
from chorerate.models.chore import Chore
from chorerate.models.chore_rating import ChoreRating
from chorerate.models.allocated_chore import AllocatedChore
from chorerate.models.household import Household
from chorerate.models import FrequencyEnum

from . import chore_helpers as chore_helper

from chorerate.exceptions import ChoreAllocationException

import numpy as np
from scipy.optimize import linprog


def get_normalized_ratings(chores, members):
    normalized_ratings = {chore.id: {} for chore in chores}

    for member in members:
        ratings = ChoreRating.query.filter_by(
            household_member_id=member.id).all()

        if not ratings:
            continue

        mean_rating = np.mean([rating.rating for rating in ratings])
        std_rating = np.std([rating.rating for rating in ratings])

        for rating in ratings:
            if std_rating == 0:
                normalized_value = 0
            else:
                normalized_value = (rating.rating - mean_rating) / std_rating
            normalized_ratings[rating.chore_id][member.id] = normalized_value

    return normalized_ratings


def get_chore_frequency(chore):
    if chore.frequency == FrequencyEnum.DAILY:
        return 1
    elif chore.frequency == FrequencyEnum.WEEKLY:
        return 7
    elif chore.frequency == FrequencyEnum.MONTHLY:
        return 28


def calculate_chore_duration_factors(chores):
    return {chore.id: chore.duration_minutes / get_chore_frequency(chore)
            for chore in chores}


def get_normalized_ratings_for_member(normalized_ratings, member_id):
    member_ratings = {chore_id: ratings.get(member_id, None)
                      for chore_id, ratings in normalized_ratings.items()}
    return member_ratings


def allocate_chores(household_id):
    '''
        Calculate the optimal chore allocation for a given household
        using linear programming
    '''

    household = Household.query.get(household_id)
    unrated_chores = chore_helper.get_unrated_chores_for_household(household)

    if unrated_chores:
        users_with_unrated = len(unrated_chores)
        if users_with_unrated == 1:
            # Use iterator and next() to get the first key in the dictionary
            member_id = next(iter(unrated_chores))
            member = HouseholdMember.query.get(member_id)
            message = f'{member.user.username} has unrated chores'
        else:
            message = f'{users_with_unrated} members have unrated chores'

        raise ChoreAllocationException(message)

    members = HouseholdMember.query.filter_by(household_id=household_id).all()
    chores = Chore.query.filter_by(household_id=household_id).all()

    num_chores = len(chores)
    num_members = len(members)

    normalized_ratings = get_normalized_ratings(chores, members)
    chore_duration_factors = calculate_chore_duration_factors(chores)

    # Create the coefficient matrix for the objective function
    c = []
    penalty = 10  # Penalty for least-rated chores
    for chore in chores:
        for member in members:
            rating = normalized_ratings[chore.id][member.id]
            duration_factor = chore_duration_factors[chore.id]
            user_ratings = get_normalized_ratings_for_member(
                normalized_ratings, member.id)
            if rating == min(user_ratings.values()):  # Least-rated chore
                c.append(-rating * duration_factor + penalty)
            else:
                c.append(-rating * duration_factor)

    # Create equality constraint matrix (Ax = b)
    A_eq = np.zeros((num_chores, num_chores * num_members))
    for i in range(num_chores):
        for j in range(num_members):
            A_eq[i, i * num_members + j] = 1

    b_eq = np.ones(num_chores)

    # Create inequality constraint matrix (Ax <= b)
    A_ub = np.zeros((num_members, num_chores * num_members))
    for j in range(num_members):
        for i in range(num_chores):
            A_ub[j, i * num_members + j] = chore_duration_factors[chores[i].id]

    b_ub = [sum(chore_duration_factors[chore.id]
                for chore in chores) / num_members] * num_members

    # Define the bounds for each variable (binary 0 or 1)
    bounds = [(0, 1) for _ in range(num_chores * num_members)]

    # Solve the linear programming problem
    res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq,
                  b_eq=b_eq, bounds=bounds, method='highs')

    # Extract the results
    assignments = np.reshape(res.x, (num_chores, num_members))

    for i, chore in enumerate(chores):
        chore.initialize_last_scheduled()
        for j, member in enumerate(members):
            # Binary problem; close to 1 indicate assignment
            if assignments[i, j] > 0.5:
                existing_assignment = AllocatedChore.query.filter_by(
                    chore_id=chore.id).first()
                # If assignment for chore already exists
                if existing_assignment:
                    # Update assignment if different member
                    if existing_assignment.household_member_id != member.id:
                        existing_assignment.household_member_id = member.id
                        db.session.commit()

                    # Continue whether assignment is updated or not
                    continue

                assignment = AllocatedChore(chore_id=chore.id,
                                            household_member_id=member.id)
                db.session.add(assignment)

    # Commit the changes to the database
    db.session.commit()
    Household.query.get(household_id).chore_allocation_complete()
