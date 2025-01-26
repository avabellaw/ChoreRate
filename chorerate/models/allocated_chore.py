from chorerate import db


class AllocatedChore(db.Model):
    '''Model for the allocated chore table'''
    __tablename__ = 'allocated_chores'
    id = db.Column(db.Integer, primary_key=True)
    household_member_id = db.Column(db.Integer,
                                    db.ForeignKey('household_members.id'),
                                    nullable=False)
    chore_id = db.Column(db.Integer,
                         db.ForeignKey('chores.id'),
                         nullable=False)

    due_date = db.Column(db.DateTime, nullable=True)

    household_member = db.relationship('HouseholdMember',
                                       backref='allocated_chores')

    table_args = (
        db.UniqueConstraint('household_member_id',
                            'chore_id',
                            name='unique_allocated_chore'),
    )

    def __repr__(self):
        return f"<{self.user_id} has been allocated '{self.chore_id}'>"
