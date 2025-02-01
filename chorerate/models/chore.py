from datetime import datetime, timedelta

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
    last_scheduled = db.Column(db.Date, nullable=True)
    date_completed = db.Column(db.Date, nullable=True)

    allocation = db.relationship('AllocatedChore',
                                 backref='chore',
                                 uselist=False)

    def num_scheduled_since_allocation(self, last_ran_chore_allocation):
        '''
            Returns the number of times the chore has been scheduled since the
            last chore allocation was run
        '''

        if last_ran_chore_allocation is None:
            return 0
        match (self.frequency):
            case FrequencyEnum.DAILY:
                return (datetime.now().date()
                        - last_ran_chore_allocation).days
            case FrequencyEnum.WEEKLY:
                return (datetime.now().date()
                        - last_ran_chore_allocation).days // 7
            case FrequencyEnum.MONTHLY:
                return (datetime.now().date()
                        - last_ran_chore_allocation).days // 28

    def initialize_last_scheduled(self):
        if self.last_scheduled is None:
            self.set_last_scheduled_today()
            self.last_scheduled = self.get_next_due()

    def get_next_due(self):
        today = datetime.now().date()
        match (self.frequency):
            case FrequencyEnum.DAILY:
                return max(self.last_scheduled + timedelta(days=1), today)
            case FrequencyEnum.WEEKLY:
                return max(self.last_scheduled + timedelta(weeks=1), today)
            case FrequencyEnum.MONTHLY:
                return max(self.last_scheduled + timedelta(weeks=4), today)

    def is_completed(self):
        if self.date_completed is None:
            return False
        return self.date_completed == datetime.now().date()

    def is_overdue(self):
        return self.get_next_due() < datetime.now().date()

    def set_last_scheduled_today(self):
        self.last_scheduled = datetime.now().date()

    def __repr__(self):
        return f"<{self.name} {self.frequency} - {self.times_per_frequency}x>"
