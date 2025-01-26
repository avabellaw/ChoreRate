from flask import Blueprint, render_template, request, \
    redirect, url_for, flash, jsonify
from flask_login import login_required
from datetime import datetime
from chorerate import db, app

# Models
from chorerate.models.chore import Chore
from chorerate.models.allocated_chore import AllocatedChore
from chorerate.models.chore_rating import ChoreRating
from chorerate.models import FrequencyEnum

from chorerate import helpers
import json

bp = Blueprint('chore', __name__)


@bp.route('/rate', methods=['GET', 'POST'])
@login_required
def rate():
    '''View for the rate page'''
    current_member = helpers.current_household_member()

    if request.method == 'POST':
        data = json.loads(request.data.decode('utf-8'))
        rating, chord_id = map(int, data.values())

        existing_rating = db.session.query(ChoreRating).filter_by(
            household_member_id=current_member.id, chore_id=chord_id).first()

        if existing_rating:
            existing_rating.rating = rating
        else:
            new_rating = ChoreRating(
                household_member_id=current_member.id,
                chore_id=chord_id,
                rating=rating)

            db.session.add(new_rating)
        db.session.commit()

        return jsonify({'message': 'success'})

    household = helpers.current_household()
    unrated_chores = helpers.get_unrated_from_db()

    # If all chores have been rated, redirect to edit ratings
    # Unless there are no chores in the household.
    if len(unrated_chores) == 0 and not len(household.chores) == 0:
        rated_chores_rows = db.session.query(Chore, ChoreRating).join(
            ChoreRating).filter(
                ChoreRating.household_member_id == current_member.id).all()

        rated_chores = [{'id': chore.id,
                         'name': chore.name,
                         'rating': rating.rating,
                         'duration_minutes': chore.duration_minutes}
                        for chore, rating in rated_chores_rows]
        return render_template('chores/edit-ratings.html',
                               rated_chores=rated_chores)

    return render_template('chores/rate-chores.html')


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
        household_id = helpers.current_household().id
        new_chore = Chore(household_id=household_id,
                          name=name,
                          frequency=frequency_enum,
                          times_per_frequency=times_per_frequency,
                          duration_minutes=duration_minutes)
        db.session.add(new_chore)
        db.session.commit()
        flash(f"Chore #{new_chore.id} - '{name.lower()}' \
            added successfully!", 'success')
        return redirect(url_for('manage'))
    chores = Chore.query.all()
    member_id = helpers.current_household_member().id
    allocations = AllocatedChore.query.filter_by(
        household_member_id=member_id).all()
    return render_template('chores/manage.html',
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

        allocation_member_id = request.form['allocation']

        if allocation_member_id:
            allocated_user = AllocatedChore.query.filter_by(
                chore_id=chore_id).first()

            if not allocated_user:
                allocated_user = AllocatedChore(
                    household_member_id=allocation_member_id,
                    chore_id=chore_id,
                    due_date=datetime.now().date())  # Remove later
                db.session.add(allocated_user)

            allocated_user.household_member_id = allocation_member_id

        db.session.commit()
        flash(f"Chore #{chore_id} - '{chore.name.lower()}' \
            updated successfully!", 'success')
        return redirect(url_for('manage'))

    chore = Chore.query.get(chore_id)
    members = helpers.current_household().members
    return render_template('chores/edit-chore.html',
                           chore=chore,
                           members=members)
