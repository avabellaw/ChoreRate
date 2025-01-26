'''Contains the routes for the application'''
import json
from datetime import date, datetime

from flask import render_template, redirect, url_for, request, flash, jsonify, session
from flask_login import login_user, login_required, logout_user, current_user

from werkzeug.security import generate_password_hash, check_password_hash

from chorerate import app, db
from chorerate.models import User, Chore, ChoreRating, AllocatedChore, \
    FrequencyEnum, Household, HouseholdMember, \
    RegistrationLink

from chorerate import helpers

import secrets


@app.route('/')
@login_required
def homepage():
    '''View for the homepage'''
    household_member = db.session.query(HouseholdMember)\
        .filter_by(user_id=current_user.id).first()

    if not household_member:
        return redirect(url_for('create_household'))

    chores = db.session.query(Chore, AllocatedChore)\
        .join(AllocatedChore)\
        .filter(AllocatedChore.Household_member_id == household_member.id).all()

    unique_chores = []
    for chore, _ in chores:
        if chore not in unique_chores:
            unique_chores.append(chore)

    todays_chores = [(chore, allocation) for chore, allocation in chores
                     if allocation.due_date == date.today()]
    return render_template('index.html',
                           chores=chores,
                           unique_chores=unique_chores,
                           todays_chores=todays_chores)


@app.route('/create-household', methods=['GET', 'POST'])
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
        return redirect(url_for('homepage'))
    return render_template('household/create-household.html')


@app.route('/add-household-members', methods=['GET', 'POST'])
@login_required
def manage_household_members():
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
                return redirect(url_for('manage_household_members'))
            if user in household.members:
                flash(f"User '{username}' is already a member "
                      + "of household '{household.name}'.", 'danger')
                return redirect(url_for('manage_household_members'))

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


@app.route('/get-registration-link', methods=['POST'])
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
                'register',
                token=registration_link_record.token,
                _external=True)
            return jsonify({'success': True,
                            'registration_link': registration_link})

    token = secrets.token_urlsafe(16)

    new_link = RegistrationLink(token=token, household_id=household_id)
    db.session.add(new_link)
    db.session.commit()

    # Take to user registration page
    registration_link = url_for('register', token=token, _external=True)

    return jsonify({'success': True, 'registration_link': registration_link})


@app.route('/rate', methods=['GET', 'POST'])
@login_required
def rate():
    '''View for the rate page'''
    if request.method == 'POST':
        data = json.loads(request.data.decode('utf-8'))
        rating, chord_id = map(int, data.values())

        existing_rating = db.session.query(ChoreRating).filter_by(
            user_id=current_user.id, chore_id=chord_id).first()

        if existing_rating:
            existing_rating.rating = rating
        else:
            new_rating = ChoreRating(user_id=current_user.id,
                                     chore_id=chord_id,
                                     rating=rating)

            db.session.add(new_rating)
        db.session.commit()

        return jsonify({'message': 'success'})

    if len(helpers.get_unrated_from_db()) == 0:
        rated_chores_rows = db.session.query(Chore, ChoreRating).join(
            ChoreRating).filter(ChoreRating.user_id == current_user.id).all()
        rated_chores = [{'id': chore.id,
                         'name': chore.name,
                         'rating': rating.rating,
                         'duration_minutes': chore.duration_minutes}
                        for chore, rating in rated_chores_rows]
        return render_template('edit-ratings.html', rated_chores=rated_chores)

    return render_template('rate-chores.html')


@app.route('/rate/get-unrated')
@login_required
def get_unrated():
    '''Get unrated chores for the current user for the rate chores page'''
    unrated = helpers.get_unrated_from_db()
    return jsonify([{'id': chore.id,
                     'name': chore.name,
                     'frequency': chore.frequency.value,
                     'times_per_frequency': chore.times_per_frequency}
                    for chore in unrated])


@app.route('/manage', methods=['GET', 'POST'])
@login_required
def manage():
    '''Add chores and view all chores to edit'''
    if request.method == 'POST':
        name = request.form['chore-name']
        frequency = request.form['chore-frequency']
        frequency_enum = FrequencyEnum(frequency)
        times_per_frequency = request.form['chore-times']
        duration_minutes = request.form['chore-duration']
        new_chore = Chore(name=name, frequency=frequency_enum,
                          times_per_frequency=times_per_frequency,
                          duration_minutes=duration_minutes)
        db.session.add(new_chore)
        db.session.commit()
        flash(f"Chore #{new_chore.id} - '{name.lower()}' \
            added successfully!", 'success')
        return redirect(url_for('manage'))
    chores = Chore.query.all()
    allocations = AllocatedChore.query.filter_by(user_id=current_user.id).all()
    return render_template('manage.html',
                           chores=chores,
                           allocations=allocations)


@app.route('/manage/edit-chore/<int:chore_id>', methods=['GET', 'POST'])
@login_required
def edit_chore(chore_id):
    if request.method == 'POST':
        chore_id = request.form['chore-id']
        chore = Chore.query.get(chore_id)
        chore.name = request.form['chore-name']
        chore.frequency = FrequencyEnum(request.form['chore-frequency'])
        chore.times_per_frequency = request.form['chore-times']
        chore.duration_minutes = request.form['chore-duration']

        allocation_user_id = request.form['allocation']

        allocated_user = AllocatedChore.query.filter_by(
            chore_id=chore_id).first()

        allocated_user.user_id = allocation_user_id

        db.session.commit()
        flash(f"Chore #{chore_id} - '{chore.name.lower()}' \
            updated successfully!", 'success')
        return redirect(url_for('manage'))

    chore = Chore.query.get(chore_id)
    users = User.query.all()
    return render_template('edit-chore.html', chore=chore, users=users)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        token = session.pop('registration_token', None)

        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm-password']

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('register.html', username=username)

        hashed_password = generate_password_hash(
            password, method='pbkdf2:sha256')
        new_user = User(username=username, password=hashed_password)
        existing_user = User.query.filter_by(
            username=new_user.username).first()

        if not existing_user:
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)

            if token:
                return helpers.add_user_to_household_by_token(new_user, token)
            else:
                flash(f"Welcome {new_user.username}!", 'success')
            return redirect(url_for('homepage'))
        else:
            flash('Username already exists.', 'danger')

    token = request.args.get('token')

    if token:
        if current_user.is_authenticated:
            return helpers.add_user_to_household_by_token(current_user, token)

        session['registration_token'] = token

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    '''Login route, redirect to homepage'''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                flash(f"Welcome {user.username}!", 'success')
                login_user(user)

                return redirect(url_for('homepage'))
            else:
                flash('Incorrect password.', 'danger')
        else:
            flash('User does not exist.', 'danger')

        return redirect(url_for('login'))
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    '''Logout route, redirects to login'''
    flash("You have been logged out", 'info')
    logout_user()
    return redirect(url_for('login'))
