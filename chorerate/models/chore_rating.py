from chorerate import db


class ChoreRating(db.Model):
    '''Model for the chore rating table'''
    __tablename__ = 'chore_ratings'
    id = db.Column(db.Integer, primary_key=True)
    household_member_id = db.Column(db.Integer, db.ForeignKey(
        'household_members.id'), nullable=False)
    chore_id = db.Column(db.Integer,
                         db.ForeignKey('chores.id'),
                         nullable=False)
    rating = db.Column(db.SmallInteger,
                       db.CheckConstraint('rating >= 1 AND rating <= 10'),
                       nullable=False)

    chore = db.relationship('Chore', backref='ratings')

    def __repr__(self):
        return f"<{self.user_id} rated '{self.chore_id}': {self.rating}>"
