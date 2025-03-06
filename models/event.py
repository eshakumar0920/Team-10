from datetime import datetime
from models import db

class Event(db.Model):
    __tablename__ = 'events'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    location = db.Column(db.String(100), nullable=False)
    event_date = db.Column(db.String(50), nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Changed to ForeignKey
    created_at = db.Column(db.String(50), nullable=False)
    
    # Add new fields for the leveling system
    xp_reward = db.Column(db.Integer, default=50)  # Base XP for attending
    organizer_xp_reward = db.Column(db.Integer, default=200)  # XP for organizing
    
    # Update relationship
    participants = db.relationship('Participant', backref='event', lazy=True)
    creator = db.relationship('User', backref=db.backref('created_events', lazy='dynamic'))
    
    def __init__(self, title, description, location, event_date, creator_id, xp_reward=50, organizer_xp_reward=200):
        self.title = title
        self.description = description
        self.location = location
        self.event_date = event_date
        self.creator_id = creator_id
        self.created_at = datetime.now().isoformat()
        self.xp_reward = xp_reward
        self.organizer_xp_reward = organizer_xp_reward
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'location': self.location,
            'event_date': self.event_date,
            'creator_id': self.creator_id,
            'created_at': self.created_at,
            'xp_reward': self.xp_reward,
            'organizer_xp_reward': self.organizer_xp_reward
        }
        
    def award_creator_xp(self):
        """Award XP to the creator/organizer of the event"""
        from models.user import User
        creator = User.query.get(self.creator_id)
        
        if creator:
            creator.award_xp(
                amount=self.organizer_xp_reward,
                activity_type='event_organization',
                event_id=self.id,
                description=f"Organized event: {self.title}"
            )
            return True
        return False
