from datetime import datetime, UTC
from models import db

class Event(db.Model):
    __tablename__ = 'events'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    location = db.Column(db.String(100), nullable=False)
    event_date = db.Column(db.String(50), nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.String(50), nullable=False)
    
    # Add semester tracking for events
    semester = db.Column(db.String(20), nullable=True)
    
    # Fixed XP values as per the design
    xp_reward = db.Column(db.Integer, default=50)  # Base XP for attending (50)
    organizer_xp_reward = db.Column(db.Integer, default=200)  # XP for organizing (200)
    
    # Update relationship
    participants = db.relationship('Participant', back_populates='event', lazy=True)
    creator = db.relationship('User', backref=db.backref('created_events', lazy='dynamic'))
    
    def __init__(self, title, description, location, event_date, creator_id, semester=None):
        self.title = title
        self.description = description
        self.location = location
        self.event_date = event_date
        self.creator_id = creator_id
        self.created_at = datetime.now(UTC).isoformat()
        
        # Set semester if provided, otherwise try to get current semester
        if semester:
            self.semester = semester
        else:
            # Try to get current semester
            from models.semester import Semester
            current_semester = Semester.get_current_semester()
            if current_semester:
                self.semester = current_semester.name
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'location': self.location,
            'event_date': self.event_date,
            'creator_id': self.creator_id,
            'created_at': self.created_at,
            'semester': self.semester,
            'xp_reward': self.xp_reward,
            'organizer_xp_reward': self.organizer_xp_reward
        }
        
    def award_creator_xp(self):
        """Award XP to the creator/organizer of the event"""
        from models.user import User
        creator = db.session.get(User, self.creator_id)
        
        if creator:
            creator.award_xp(
                base_amount=self.organizer_xp_reward,
                activity_type='event_organization',
                event_id=self.id,
                description=f"Organized event: {self.title}"
            )
            return True
        return False