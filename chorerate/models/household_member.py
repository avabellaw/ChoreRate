from chorerate import db


class HouseholdMember(db.Model):
    '''Model for the household member table'''
    __tablename__ = 'household_members'
    id = db.Column(db.Integer, primary_key=True)
    household_id = db.Column(db.Integer,
                             db.ForeignKey('households.id'),
                             nullable=False)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'),
                        nullable=False,
                        unique=True)

    user = db.relationship('User', backref='household_member')

    __table_args__ = (
        db.UniqueConstraint('household_id',
                            'user_id',
                            name='unique_household_member'),
    )
