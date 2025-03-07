# models/__init__.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import models after db is defined
from .event import Event
from .participant import Participant
from .user import User
from .level import Level
from .user_activity import UserActivity

# You might want to add this function to initialize the levels in your database
def initialize_levels():
    """Initialize default levels if they don't exist"""
    levels = [
        {"level_number": 1, "xp_required": 0, "title": "Novice", "description": "Just starting out", "perks": "Basic access"},
        {"level_number": 2, "xp_required": 100, "title": "Explorer", "description": "Getting involved", "perks": "Create public events"},
        {"level_number": 3, "xp_required": 300, "title": "Enthusiast", "description": "Regular participant", "perks": "Priority registration"},
        {"level_number": 4, "xp_required": 600, "title": "Organizer", "description": "Experienced member", "perks": "Create private events"},
        {"level_number": 5, "xp_required": 1000, "title": "Leader", "description": "Community pillar", "perks": "Highlighted profile"}
    ]
    
    for level_data in levels:
        level = Level.query.filter_by(level_number=level_data["level_number"]).first()
        if not level:
            level = Level(**level_data)
            db.session.add(level)
    
    db.session.commit()
