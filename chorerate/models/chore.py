from chorerate import db
from sqlalchemy import Enum
from . import FrequencyEnum


class Chore(db.Model):
    '''Model for the chore table'''
    __tablename__ = 'chores'
    id = db.Column(db.Integer, primary_key=True)
    household_id = db.Column(db.Integer,
                             db.ForeignKey('households.id'),
                             nullable=False)
    name = db.Column(db.String(50), nullable=False)
    frequency = db.Column(Enum(FrequencyEnum), nullable=False)
    times_per_frequency = db.Column(db.SmallInteger, nullable=False)
    duration_minutes = db.Column(db.SmallInteger, nullable=False)
    last_scheduled = db.Column(db.DateTime, nullable=True)

    allocation = db.relationship('AllocatedChore',
                                 backref='chore',
                                 uselist=False)

    def __repr__(self):
        return f"<{self.name} {self.frequency} - {self.times_per_frequency}x>"
