from flask import render_template, request, redirect, \
                  url_for, flash, session, Blueprint
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from chorerate import app, db
from chorerate.models import User

from chorerate import helpers

bp = Blueprint('auth', __name__)


@bp.route('/register', methods=['GET', 'POST'])
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
