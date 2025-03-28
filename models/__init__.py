# models/__init__.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import models after db is defined
from .event import Event
from .participant import Participant
from .user import User
from .level import Level
from .user_activity import UserActivity
from .user_interaction import UserInteraction
from .loot_box import LootBox, LootBoxType
from .semester import Semester

def initialize_default_data():
    """Initialize all default data"""
    initialize_levels()
    initialize_loot_box_types()
    initialize_current_semester()

def initialize_levels():
    """Initialize default levels"""
    # Import for type checking
    from sqlalchemy import inspect
    
    # Check if level_xp column exists in levels table
    with db.engine.connect() as conn:
        inspector = inspect(db.engine)
        columns = [col['name'] for col in inspector.get_columns('levels')]
        
        # If the new columns don't exist, don't try to set them yet
        # Migration will add them later
        if 'level_xp' not in columns or 'total_xp' not in columns or 'tier' not in columns:
            print("New level columns not found - skipping level initialization until migration completes")
            return
    
    # If we have the columns, initialize the levels
    Level.initialize_levels()

def initialize_loot_box_types():
    """Initialize default loot box types"""
    loot_box_types = [
        {
            "name": "Tier 1 Loot Box",
            "description": "A basic loot box for Tier 1 players",
            "tier": 1, 
            "icon_url": "/static/lootboxes/tier1.png"
        },
        {
            "name": "Tier 2 Loot Box",
            "description": "An improved loot box for Tier 2 players",
            "tier": 2,
            "icon_url": "/static/lootboxes/tier2.png"
        },
        {
            "name": "Tier 3 Loot Box",
            "description": "A valuable loot box for Tier 3 players",
            "tier": 3,
            "icon_url": "/static/lootboxes/tier3.png"
        },
        {
            "name": "Tier 4 Loot Box",
            "description": "A premium loot box for Tier 4 players",
            "tier": 4,
            "icon_url": "/static/lootboxes/tier4.png"
        },
        {
            "name": "Tier 5 Loot Box",
            "description": "An elite loot box for Tier 5 players",
            "tier": 5,
            "icon_url": "/static/lootboxes/tier5.png"
        }
    ]
    
    for loot_box_data in loot_box_types:
        loot_box = LootBoxType.query.filter_by(name=loot_box_data["name"]).first()
        if not loot_box:
            loot_box = LootBoxType(**loot_box_data)
            db.session.add(loot_box)
    
    db.session.commit()

def initialize_current_semester():
    """Initialize the current semester if none exists"""
    current_semester = Semester.get_current_semester()
    
    if not current_semester:
        from datetime import datetime, timedelta
        
        # Create a default current semester (this semester)
        today = datetime.utcnow()
        
        # Determine semester name based on current month
        if today.month < 6:  # Spring semester (January-May)
            semester_name = f"Spring {today.year}"
            start_date = datetime(today.year, 1, 15)  # January 15th
            end_date = datetime(today.year, 5, 15)    # May 15th
        elif today.month < 9:  # Summer semester (June-August)
            semester_name = f"Summer {today.year}"
            start_date = datetime(today.year, 6, 1)   # June 1st
            end_date = datetime(today.year, 8, 15)    # August 15th
        else:  # Fall semester (September-December)
            semester_name = f"Fall {today.year}"
            start_date = datetime(today.year, 9, 1)   # September 1st
            end_date = datetime(today.year, 12, 15)   # December 15th
        
        new_semester = Semester(
            name=semester_name,
            start_date=start_date,
            end_date=end_date,
            is_active=True
        )
        
        db.session.add(new_semester)
        db.session.commit()