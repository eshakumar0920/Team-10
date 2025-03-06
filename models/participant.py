from datetime import datetime
from models import db

class Participant(db.Model):
    __tablename__ = 'participants'
    
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Changed to ForeignKey
    joined_at = db.Column(db.String(50), nullable=False)
    
    # Add new fields for the leveling system
    xp_earned = db.Column(db.Integer, default=0)
    attendance_status = db.Column(db.String(20), default='registered')  # registered, attended, no-show
    
    __table_args__ = (db.UniqueConstraint('event_id', 'user_id', name='unique_participant'),)
    
    # Add relationship
    user = db.relationship('User', backref=db.backref('participations', lazy='dynamic'))
    event = db.relationship('Event', backref=db.backref('participants', lazy='dynamic'))
    
    def __init__(self, event_id, user_id):
        self.event_id = event_id
        self.user_id = user_id
        self.joined_at = datetime.now().isoformat()
    
    def to_dict(self):
        return {
            'id': self.id,
            'event_id': self.event_id,
            'user_id': self.user_id,
            'joined_at': self.joined_at,
            'xp_earned': self.xp_earned,
            'attendance_status': self.attendance_status
        }
    
    def mark_attended(self):
        """Mark participant as attended and award XP"""
        if self.attendance_status != 'attended':
            self.attendance_status = 'attended'
            
            # Get event to determine XP reward
            from models.event import Event
            event = Event.query.get(self.event_id)
            
            if event:
                xp_reward = event.xp_reward
                self.xp_earned = xp_reward
                
                # Award XP to user
                from models.user import User
                user = User.query.get(self.user_id)
                if user:
                    user.award_xp(
                        amount=xp_reward,
                        activity_type='event_attendance',
                        event_id=self.event_id,
                        description=f"Attended event: {event.title}"
                    )
                    
                db.session.commit()
                return True
        return False
