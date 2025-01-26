'''Helper functions'''

from flask_login import current_user
from chorerate import db
from chorerate.models import Chore, ChoreRating, Household, RegistrationLink, \
    HouseholdMember

from datetime import datetime
from flask import flash, redirect, url_for


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