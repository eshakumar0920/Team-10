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
from .reward import RewardType, UserReward  # Add new models
from .drop_rate import LootBoxDropRate, RewardDropRate, initialize_drop_rates  # Add new models

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

def initialize_reward_types():
    """Initialize default reward types (profile images)"""
    # Check if the reward_types table exists
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    if 'reward_types' not in inspector.get_table_names():
        print("Reward types table doesn't exist yet - skipping initialization")
        return
    
    # Season-themed rewards (Fall, Spring, Summer)
    season_rewards = [
        # Tier 1 Season Rewards
        {"name": "Spring Sprout", "description": "A fresh spring sprout avatar", "tier": 1, "category": "Season", "theme": "Spring", "image_url": "/static/rewards/season/spring_basic.png"},
        {"name": "Summer Sun", "description": "A bright summer sun avatar", "tier": 1, "category": "Season", "theme": "Summer", "image_url": "/static/rewards/season/summer_basic.png"},
        {"name": "Fall Leaf", "description": "A colorful fall leaf avatar", "tier": 1, "category": "Season", "theme": "Fall", "image_url": "/static/rewards/season/fall_basic.png"},
        
        # Tier 2 Season Rewards
        {"name": "Spring Garden", "description": "A blooming spring garden avatar", "tier": 2, "category": "Season", "theme": "Spring", "image_url": "/static/rewards/season/spring_medium.png"},
        {"name": "Summer Beach", "description": "A sunny beach avatar", "tier": 2, "category": "Season", "theme": "Summer", "image_url": "/static/rewards/season/summer_medium.png"},
        {"name": "Fall Forest", "description": "A colorful autumn forest avatar", "tier": 2, "category": "Season", "theme": "Fall", "image_url": "/static/rewards/season/fall_medium.png"},
        
        # Tier 3 Season Rewards
        {"name": "Spring Celebration", "description": "A festive spring celebration avatar", "tier": 3, "category": "Season", "theme": "Spring", "image_url": "/static/rewards/season/spring_premium.png"},
        {"name": "Summer Festival", "description": "A vibrant summer festival avatar", "tier": 3, "category": "Season", "theme": "Summer", "image_url": "/static/rewards/season/summer_premium.png"},
        {"name": "Fall Harvest", "description": "A bountiful fall harvest avatar", "tier": 3, "category": "Season", "theme": "Fall", "image_url": "/static/rewards/season/fall_premium.png"},
        
        # Tier 4 Season Rewards
        {"name": "Spring Majesty", "description": "A majestic spring landscape avatar", "tier": 4, "category": "Season", "theme": "Spring", "image_url": "/static/rewards/season/spring_elite.png"},
        {"name": "Summer Paradise", "description": "A paradisaical summer avatar", "tier": 4, "category": "Season", "theme": "Summer", "image_url": "/static/rewards/season/summer_elite.png"},
        {"name": "Fall Panorama", "description": "A breathtaking fall panorama avatar", "tier": 4, "category": "Season", "theme": "Fall", "image_url": "/static/rewards/season/fall_elite.png"},
    ]
    
    # Event-themed rewards
    event_rewards = [
        # Tier 1 Event Rewards
        {"name": "Study Book", "description": "A simple book avatar", "tier": 1, "category": "Event", "theme": "Study", "image_url": "/static/rewards/event/study_basic.png"},
        {"name": "Sports Ball", "description": "A basic sports ball avatar", "tier": 1, "category": "Event", "theme": "Sport", "image_url": "/static/rewards/event/sport_basic.png"},
        {"name": "Game Controller", "description": "A simple game controller avatar", "tier": 1, "category": "Event", "theme": "Gaming", "image_url": "/static/rewards/event/gaming_basic.png"},
        {"name": "Code Tag", "description": "A basic code tag avatar", "tier": 1, "category": "Event", "theme": "Coding", "image_url": "/static/rewards/event/coding_basic.png"},
        
        # Tier 2 Event Rewards
        {"name": "Study Desk", "description": "A tidy study desk avatar", "tier": 2, "category": "Event", "theme": "Study", "image_url": "/static/rewards/event/study_medium.png"},
        {"name": "Sports Equipment", "description": "Various sports equipment avatar", "tier": 2, "category": "Event", "theme": "Sport", "image_url": "/static/rewards/event/sport_medium.png"},
        {"name": "Gaming Setup", "description": "A gaming setup avatar", "tier": 2, "category": "Event", "theme": "Gaming", "image_url": "/static/rewards/event/gaming_medium.png"},
        {"name": "Code Editor", "description": "A code editor avatar", "tier": 2, "category": "Event", "theme": "Coding", "image_url": "/static/rewards/event/coding_medium.png"},
        
        # Tier 3 Event Rewards
        {"name": "Library", "description": "A grand library avatar", "tier": 3, "category": "Event", "theme": "Study", "image_url": "/static/rewards/event/study_premium.png"},
        {"name": "Stadium", "description": "A sports stadium avatar", "tier": 3, "category": "Event", "theme": "Sport", "image_url": "/static/rewards/event/sport_premium.png"},
        {"name": "Gaming Tournament", "description": "A gaming tournament avatar", "tier": 3, "category": "Event", "theme": "Gaming", "image_url": "/static/rewards/event/gaming_premium.png"},
        {"name": "Developer Workspace", "description": "A professional developer workspace avatar", "tier": 3, "category": "Event", "theme": "Coding", "image_url": "/static/rewards/event/coding_premium.png"},
        
        # Tier 4 Event Rewards
        {"name": "Knowledge Master", "description": "An elite knowledge master avatar", "tier": 4, "category": "Event", "theme": "Study", "image_url": "/static/rewards/event/study_elite.png"},
        {"name": "Sports Champion", "description": "A championship winning avatar", "tier": 4, "category": "Event", "theme": "Sport", "image_url": "/static/rewards/event/sport_elite.png"},
        {"name": "Gaming Legend", "description": "A legendary gaming avatar", "tier": 4, "category": "Event", "theme": "Gaming", "image_url": "/static/rewards/event/gaming_elite.png"},
        {"name": "Code Master", "description": "A masterful coding avatar", "tier": 4, "category": "Event", "theme": "Coding", "image_url": "/static/rewards/event/coding_elite.png"},
    ]
    
    # Unique rare rewards (available only to max level players)
    rare_rewards = [
        {"name": "Golden Trophy", "description": "A golden trophy for exceptional achievement", "tier": 4, "category": "Unique", "theme": "Achievement", "image_url": "/static/rewards/rare/golden_trophy.png", "is_rare": True},
        {"name": "Diamond Badge", "description": "A diamond badge for consistent excellence", "tier": 4, "category": "Unique", "theme": "Achievement", "image_url": "/static/rewards/rare/diamond_badge.png", "is_rare": True},
        {"name": "Platinum Star", "description": "A platinum star for outstanding contributions", "tier": 4, "category": "Unique", "theme": "Achievement", "image_url": "/static/rewards/rare/platinum_star.png", "is_rare": True},
        {"name": "Legend Crown", "description": "A crown fit for a legend", "tier": 4, "category": "Unique", "theme": "Achievement", "image_url": "/static/rewards/rare/legend_crown.png", "is_rare": True},
    ]
    
    # Combine all rewards
    all_rewards = season_rewards + event_rewards + rare_rewards
    
    # Add rewards if they don't exist yet
    for reward_data in all_rewards:
        existing = RewardType.query.filter_by(name=reward_data["name"]).first()
        if not existing:
            new_reward = RewardType(**reward_data)
            db.session.add(new_reward)
    
    db.session.commit()

# Define this function after all the component functions are defined
def initialize_default_data():
    """Initialize all default data"""
    initialize_levels()
    initialize_loot_box_types()
    initialize_current_semester()
    initialize_drop_rates()  # Initialize drop rates
    initialize_reward_types()  # Initialize reward types