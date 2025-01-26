'''Helper functions'''

from flask_login import current_user
from chorerate import db, cache
from chorerate.models import Chore, ChoreRating, Household, RegistrationLink, \
    HouseholdMember

from datetime import datetime
from flask import flash, redirect, url_for


def get_household():
    '''Get the household for the current user using cache'''

    household_cache = cache.get(f'household_{current_user.id}')

    # If cache is empty, get household_member from db and set cache
    if not household_cache:
        household_member = get_household_member()
        household_cache = Household.query.get(household_member.household_id)
        cache.set(f'household_{current_user.id}', household_cache)

    return household_cache


def get_household_member():
    '''Get the household member for the current user using cache'''
    household_member_cache = cache.get(f'household_member_{current_user.id}')

    # If cache is empty, get from db and set cache
    if not household_member_cache:
        household_member_cache = HouseholdMember.query.filter_by(
            user_id=current_user.id).first()
        cache.set(f'household_member_{current_user.id}',
                  household_member_cache)

    return household_member_cache


def get_unrated_from_db():
    '''Get unrated chores for the current user'''
    current_member_id = get_current_household_member().id
    rated = db.session.query(ChoreRating.chore_id).filter_by(household_member_id=current_member_id)
    unrated = db.session.query(Chore).filter(~Chore.id.in_(rated)).all()

    return unrated


def add_user_to_household_by_token(user, token):
    '''Add a user to a household using a token'''
    registration_link = RegistrationLink.query.filter_by(
        token=token).first()

    if registration_link:
        # If already apart of household, redirect to homepage
        if HouseholdMember.query.filter_by(
                user_id=user.id).first():
            flash('You are already a member of a household.', 'danger')
            return redirect(url_for('homepage'))

        # If token has expired, redirect to homepage
        if registration_link.expires_at < datetime.now():
            flash('Registration link has expired.', 'danger')
            return redirect(url_for('homepage'))

        new_household_member = HouseholdMember(
            household_id=registration_link.household_id,
            user_id=user.id
        )

        household_name = Household.query.get(
            registration_link.household_id
        ).name

        db.session.add(new_household_member)
        db.session.commit()
        flash(f"Welcome {user.username}, you've been added to"
              + f" household '{household_name}'!", 'success')
        return redirect(url_for('homepage'))


def get_current_household_member():
    '''Get the household member object for a user'''
    return HouseholdMember.query.filter_by(user_id=current_user.id).first()