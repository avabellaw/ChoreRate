'''Contains the routes for the application'''
from flask import render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_user, login_required, logout_user, current_user

from werkzeug.security import generate_password_hash, check_password_hash

from chorerate import app, db
from chorerate.models import User, Chore, ChoreRating, FrequencyEnum


@app.route('/')
@login_required
def homepage():
    '''View for the homepage'''
    return render_template('index.html')


@app.route('/rate')
@login_required
def rate():
    '''View for the rate page'''
    return render_template('rate-chores.html')


@app.route('/rate/get-unrated')
@login_required
def get_unrated():
    user_id = current_user.id
    rated = ChoreRating.query.filter_by(user_id=user_id).all()
    unrated = Chore.query.filter(~Chore.id.in_(rated)).all()
    return jsonify([{'name': chore.name,
                     'frequency': chore.frequency.value,
                     'times_per_frequency': chore.times_per_frequency}
                    for chore in unrated])


@app.route('/manage', methods=['GET', 'POST'])
@login_required
def manage():
    if request.method == 'POST':
        name = request.form['chore-name']
        frequency = request.form['chore-frequency']
        frequency_enum = FrequencyEnum(frequency)
        times_per_frequency = request.form['chore-times']
        new_chore = Chore(name=name, frequency=frequency_enum,
                          times_per_frequency=times_per_frequency)
        db.session.add(new_chore)
        db.session.commit()
        flash(f"Chore {name} added successfully!", 'success')
        return redirect(url_for('manage'))
    chores = Chore.query.all()
    return render_template('manage.html', chores=chores)


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
