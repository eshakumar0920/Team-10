# models/user_interaction.py
from datetime import datetime, UTC
from . import db

class UserInteraction(db.Model):
    """Tracks interactions between users to calculate new interaction bonuses"""
    __tablename__ = 'user_interactions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    other_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    interaction_date = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(UTC))
    semester = db.Column(db.String(20), nullable=True)  # To track interactions per semester
    
    __table_args__ = (
        db.UniqueConstraint('user_id', 'other_user_id', 'event_id', name='unique_interaction'),
    )
    
    def __repr__(self):
        return f'<UserInteraction user_id={self.user_id}, other_user_id={self.other_user_id}, date={self.interaction_date}>'