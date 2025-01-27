from chorerate import db
from datetime import datetime


class Household(db.Model):
    '''Model for the household table'''
    __tablename__ = 'households'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    last_run_chore_allocation = db.Column(db.Date, nullable=True)

    chores = db.relationship('Chore', backref='household')
    members = db.relationship('HouseholdMember', backref='household')

    def chore_allocation_complete(self):
        ''' Ran after completing chore allocation'''

        # Update the last run date
        self.last_run_chore_allocation = datetime.now().date()
        db.session.commit()
