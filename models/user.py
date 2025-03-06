# models/user.py
from datetime import datetime
from . import db

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    current_level = db.Column(db.Integer, default=1)
    current_xp = db.Column(db.Integer, default=0)
    total_xp_earned = db.Column(db.Integer, default=0)
    join_date = db.Column(db.DateTime, default=datetime.utcnow)
    profile_picture = db.Column(db.String(255), nullable=True)
    
    # Relationships
    activities = db.relationship('UserActivity', backref='user', lazy='dynamic')
    participations = db.relationship('Participant', backref='user', lazy='dynamic')
    
    def award_xp(self, amount, activity_type, event_id=None, description=None):
        """Award XP to user and check for level up"""
        if amount <= 0:
            return False
            
        # Update XP
        self.current_xp += amount
        self.total_xp_earned += amount
        
        # Record activity
        new_activity = UserActivity(
            user_id=self.id,
            activity_type=activity_type,
            xp_earned=amount,
            related_event_id=event_id,
            description=description
        )
        db.session.add(new_activity)
        
        # Check for level up
        self.check_level_up()
        
        db.session.commit()
        return True
    
    def check_level_up(self):
        """Check if user has enough XP to level up"""
        from .level import Level
        
        next_level = Level.query.filter(Level.level_number > self.current_level).order_by(Level.level_number).first()
        
        if next_level and self.current_xp >= next_level.xp_required:
            self.current_level = next_level.level_number
            return True
        
        return False
