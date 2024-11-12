'''Contains the routes for the application'''
from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user

from werkzeug.security import generate_password_hash, check_password_hash

from chorerate import app, db
from chorerate.models import User


@app.route('/')
@login_required
def homepage():
    '''View for the homepage'''
    return render_template('index.html')


@app.route('/manage')
@login_required
def manage():
    return render_template('manage.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm-password']

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('register.html', username=username)

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, password=hashed_password)
        existing_user = User.query.filter_by(username=new_user.username).first()
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
