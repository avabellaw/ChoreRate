'''Contains the routes for the application'''
import json

from flask import render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_user, login_required, logout_user, current_user

from werkzeug.security import generate_password_hash, check_password_hash

from chorerate import app, db
from chorerate.models import User, Chore, ChoreRating, FrequencyEnum

from chorerate.helpers import get_unrated_from_db

@app.route('/')
@login_required
def homepage():
    '''View for the homepage'''
    return render_template('index.html')


@app.route('/rate', methods=['GET', 'POST'])
@login_required
def rate():
    '''View for the rate page'''
    if request.method == 'POST':
        data = json.loads(request.data.decode('utf-8'))
        rating, chord_id = map(int, data.values())

        existing_rating = db.session.query(ChoreRating).filter_by(user_id=current_user.id, chore_id=chord_id).first()

        if existing_rating:
            existing_rating.rating = rating
        else:
            new_rating = ChoreRating(user_id=current_user.id,
                                     chore_id=chord_id,
                                     rating=rating)

            db.session.add(new_rating)
        db.session.commit()

        return jsonify({'message': 'success'})

    if len(get_unrated_from_db()) == 0:
        rated_chores_rows = db.session.query(Chore, ChoreRating).join(ChoreRating).filter(ChoreRating.user_id == current_user.id).all()
        rated_chores = [{'id': chore.id,
                         'name': chore.name,
                         'frequency': chore.frequency.value,
                         'times_per_frequency': chore.times_per_frequency,
                         'rating': rating.rating}
                        for chore, rating in rated_chores_rows]
        return render_template('rate-chores.html', rated_chores=rated_chores)

    return render_template('rate-chores.html')


@app.route('/rate/get-unrated')
@login_required
def get_unrated():
    '''Get unrated chores for the current user for the rate chores page'''
    unrated = get_unrated_from_db()
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
    return render_template('manage.html', chores=chores)


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

        db.session.commit()
        flash(f"Chore #{chore_id} - '{chore.name.lower()}' \
            updated successfully!", 'success')
        return redirect(url_for('manage'))

    chore = Chore.query.get(chore_id)
    return render_template('edit-chore.html', chore=chore)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
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
            flash('User created successfully!', 'success')
            return redirect(url_for('login'))

        flash('Username already exists.', 'danger')
        render_template('register.html')

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    '''Login route, redirect to homepage'''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            flash(f"Welcome {user.username}!", 'success')
            login_user(user)
            return redirect(url_for('homepage'))
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    '''Logout route, redirects to login'''
    flash("You have been logged out", 'info')
    logout_user()
    return redirect(url_for('login'))
