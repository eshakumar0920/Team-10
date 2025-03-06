# models/user_activity.py
from datetime import datetime
from . import db

class UserActivity(db.Model):
    __tablename__ = 'user_activities'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    activity_type = db.Column(db.String(64), nullable=False)
    xp_earned = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    related_event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=True)
    description = db.Column(db.String(255))
    
    def __repr__(self):
        return f'<UserActivity {self.activity_type}: {self.xp_earned} XP>'
