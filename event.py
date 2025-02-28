from datetime import datetime
from models import db

class Event(db.Model):
    __tablename__ = 'events'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    location = db.Column(db.String(100), nullable=False)
    event_date = db.Column(db.String(50), nullable=False)
    creator_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.String(50), nullable=False)
    
    participants = db.relationship('Participant', backref='event', lazy=True)
    
    def __init__(self, title, description, location, event_date, creator_id):
        self.title = title
        self.description = description
        self.location = location
        self.event_date = event_date
        self.creator_id = creator_id
        self.created_at = datetime.now().isoformat()
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'location': self.location,
            'event_date': self.event_date,
            'creator_id': self.creator_id,
            'created_at': self.created_at
        }
