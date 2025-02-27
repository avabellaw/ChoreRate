from flask import render_template, request, redirect, \
    url_for, flash, jsonify, Blueprint
from flask_login import login_required, current_user
from chorerate import db

# Models
from chorerate.models.household import Household
from chorerate.models.household_member import HouseholdMember
from chorerate.models.registration_link import RegistrationLink
from chorerate.models.user import User

from chorerate.helpers.household_helpers import current_household
from chorerate.helpers.chore_allocation import allocate_chores

from chorerate.exceptions import ChoreAllocationException

import traceback

import secrets

bp = Blueprint('household', __name__)


@bp.route('/confirm-chore-allocation', methods=['GET', 'POST'])
@login_required
def run_chore_allocation():
    '''View to the run chore allocation'''

    if request.method == 'POST':
        try:
            allocate_chores(current_household().id)
            flash('Chores allocated successfully!', 'success')
            return redirect(url_for('chore.manage'))
        except ChoreAllocationException as e:
            flash(str(e), 'danger')
        except Exception:
            flash('Something went wrong allocating chores.', 'error')
            print(traceback.format_exc())

    household = current_household()
    return render_template('household/confirm-chore-allocation.html',
                           household=household)


@bp.route('/create-household', methods=['GET', 'POST'])
@login_required
def create_household():
    '''View for the create household page'''

    if request.method == 'POST':
        # Create a new household
        household_name = request.form['household-name']
        new_household = Household(name=household_name)
        db.session.add(new_household)
        db.session.commit()

        # Add the current user to the household as a household member
        new_household_member = HouseholdMember(household_id=new_household.id,
                                               user_id=current_user.id)
        db.session.add(new_household_member)
        db.session.commit()

        flash(f"Household '{household_name}' created successfully!", 'success')
        return redirect(url_for('home.homepage'))
    return render_template('household/create-household.html')


@bp.route('/add-household-members', methods=['GET', 'POST'])
@login_required
def manage_members():
    '''View for the add household members page'''
    household = db.session.query(Household)\
        .join(HouseholdMember)\
        .filter(HouseholdMember.user_id == current_user.id).first()

    if request.method == 'POST':
        username = request.form['username']

        user = User.query.filter_by(username=username).first()

        if user:
            if user == current_user:
                flash("You cannot add yourself to your own household.",
                      'danger')
                return redirect(url_for('household.manage_members'))
            if user in household.members:
                flash(f"User '{username}' is already a member "
                      + "of household '{household.name}'.", 'danger')
                return redirect(url_for('household.manage_members'))

            household_member = HouseholdMember(household_id=household.id,
                                               user_id=user.id)
            db.session.add(household_member)
            db.session.commit()
            flash(f"User '{username}' added to household '{
                  household.name}' successfully!", 'success')
        else:
            flash(f"User '{username}' does not exist.", 'danger')

    members = household.members

    return render_template('household/manage-household-members.html',
                           household_id=household.id,
                           members=members)


@bp.route('/get-registration-link', methods=['POST'])
@login_required
def get_registration_link():
    '''Create a registration link for the household'''
    data = request.get_json()
    household_id = data['household_id']

    registration_link_record = RegistrationLink.query.filter_by(
        household_id=household_id).first()

    if registration_link_record:
        if registration_link_record.has_expired():
            # Link has expired, continue to generate a new one
            db.session.delete(registration_link_record)
            db.session.commit()
        else:
            # Return existing link
            registration_link = url_for(
                'auth.register',
                token=registration_link_record.token,
                _external=True)
            return jsonify({'success': True,
                            'registration_link': registration_link})

    token = secrets.token_urlsafe(16)

    new_link = RegistrationLink(token=token, household_id=household_id)
    db.session.add(new_link)
    db.session.commit()

    # Take to user registration page
    registration_link = url_for('auth.register', token=token, _external=True)

    return jsonify({'success': True, 'registration_link': registration_link})
