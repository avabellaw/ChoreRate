from chorerate import db
from datetime import datetime, timedelta


class RegistrationLink(db.Model):
    '''Model for household registration links'''
    __tablename__ = 'registration_links'
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(32), unique=True, nullable=False)
    household_id = db.Column(db.Integer,
                             db.ForeignKey('households.id'),
                             nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime,
                           default=lambda: datetime.utcnow()
                           + timedelta(days=7))

    household = db.relationship('Household', backref='invites')

    def has_expired(self):
        '''Check if the registration link has expired'''
        return self.expires_at < datetime.now()
