# models/semester.py
from datetime import datetime
from . import db

class Semester(db.Model):
    """Tracks academic semesters for XP resets and historical tracking"""
    __tablename__ = 'semesters'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)  # e.g., "Spring 2023"
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    is_active = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        status = "Active" if self.is_active else "Inactive"
        return f'<Semester {self.name} ({status})>'
    
    @staticmethod
    def get_current_semester():
        """Returns the currently active semester or None if no semester is active"""
        return Semester.query.filter_by(is_active=True).first()
    
    @staticmethod
    def start_new_semester(name, start_date, end_date):
        """Starts a new semester and resets user XP"""
        from models.user import User
        
        # First, deactivate any currently active semesters
        current_semester = Semester.get_current_semester()
        if current_semester:
            current_semester.is_active = False
        
        # Create new semester
        new_semester = Semester(
            name=name,
            start_date=start_date,
            end_date=end_date,
            is_active=True
        )
        db.session.add(new_semester)
        
        # Reset all users' XP for the new semester
        users = User.query.all()
        for user in users:
            # Keep track of previous tier before reset
            previous_tier = user.current_tier
            
            # Reset XP and level
            user.current_xp = 0
            user.current_level = 1
            user.active_weeks_streak = 0
            user.current_semester = name
            
            # Don't reset tier - tier progression is permanent
            
            # Award a loot box for semester transition
            from models.loot_box import LootBoxType, LootBox
            
            # Find appropriate tier loot box
            loot_box_type = LootBoxType.query.filter_by(tier=previous_tier).first()
            if loot_box_type:
                new_loot_box = LootBox(
                    user_id=user.id,
                    type_id=loot_box_type.id,
                    awarded_for="semester_reset"
                )
                db.session.add(new_loot_box)
        
        db.session.commit()
        return new_semester