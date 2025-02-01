from flask import render_template, redirect, url_for, Blueprint
from flask_login import login_required, current_user
from datetime import date
from chorerate import db

# Models
from chorerate.models.household_member import HouseholdMember
from chorerate.models.allocated_chore import AllocatedChore
from chorerate.models.chore import Chore

bp = Blueprint('home', __name__)


@bp.route('/')
@login_required
def homepage():
    '''View for the homepage'''
    household_member = db.session.query(HouseholdMember)\
        .filter_by(user_id=current_user.id).first()

    if not household_member:
        return redirect(url_for('household.create_household'))

    member_id = household_member.id
    chores = db.session.query(Chore, AllocatedChore)\
        .join(AllocatedChore)\
        .filter(AllocatedChore.household_member_id == member_id).all()

    unique_chores = []
    for chore, _ in chores:
        if chore not in unique_chores:
            unique_chores.append(chore)

    todays_chores = [(chore, allocation) for chore, allocation in chores
                     if allocation.chore.get_next_due() <= date.today()]
    return render_template('index.html',
                           chores=chores,
                           unique_chores=unique_chores,
                           todays_chores=todays_chores)
