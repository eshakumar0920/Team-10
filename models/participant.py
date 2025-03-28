from datetime import datetime
from models import db

class Participant(db.Model):
    __tablename__ = 'participants'
    
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    joined_at = db.Column(db.String(50), nullable=False)
    
    # Add new fields for the leveling system
    xp_earned = db.Column(db.Integer, default=0)
    attendance_status = db.Column(db.String(20), default='registered')  # registered, attended, no-show
    
    __table_args__ = (db.UniqueConstraint('event_id', 'user_id', name='unique_participant'),)
    
    # Add relationship
    user = db.relationship('User', back_populates='participations')
    event = db.relationship('Event', back_populates='participants')
    
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
            
            # Get event to determine base XP reward
            from models.event import Event
            event = Event.query.get(self.event_id)
            
            if event:
                # Base XP for attending is set to 50 as per the leveling design
                base_xp = 50
                
                # Award XP to user with bonuses
                from models.user import User
                user = User.query.get(self.user_id)
                if user:
                    user.award_xp(
                        base_amount=base_xp,
                        activity_type='event_attendance',
                        event_id=self.event_id,
                        description=f"Attended event: {event.title}"
                    )
                    
                    # Store the actual XP earned (including bonuses) - calculated in award_xp
                    latest_activity = user.activities.order_by(db.desc('id')).first()
                    if latest_activity:
                        self.xp_earned = latest_activity.xp_earned
                    
                db.session.commit()
                return True
        return False