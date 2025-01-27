from chorerate import db


class Household(db.Model):
    '''Model for the household table'''
    __tablename__ = 'households'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    last_run_chore_allocation = db.Column(db.DateTime, nullable=True)

    chores = db.relationship('Chore', backref='household')
    members = db.relationship('HouseholdMember', backref='household')
