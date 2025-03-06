from datetime import datetime
from models import db

class Participant(db.Model):
    __tablename__ = 'participants'
    
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    joined_at = db.Column(db.String(50), nullable=False)
    
    __table_args__ = (db.UniqueConstraint('event_id', 'user_id', name='unique_participant'),)
    
    def __init__(self, event_id, user_id):
        self.event_id = event_id
        self.user_id = user_id
        self.joined_at = datetime.now().isoformat()
    
    def to_dict(self):
        return {
            'id': self.id,
            'event_id': self.event_id,
            'user_id': self.user_id,
            'joined_at': self.joined_at
        }
