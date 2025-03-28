# models/level.py
from . import db

class Level(db.Model):
    __tablename__ = 'levels'
    
    id = db.Column(db.Integer, primary_key=True)
    level_number = db.Column(db.Integer, unique=True, nullable=False)
    xp_required = db.Column(db.Integer, nullable=False)  # Keep the existing column name
    title = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(255))
    perks = db.Column(db.String(255))
    
    # Add new columns for our enhanced leveling system
    level_xp = db.Column(db.Integer, nullable=True)  # XP required for this specific level
    total_xp = db.Column(db.Integer, nullable=True)  # Cumulative XP to reach this level
    tier = db.Column(db.Integer, nullable=True, default=1)  # Tier category
    
    def __repr__(self):
        return f'<Level {self.level_number}: {self.title}>'

    @staticmethod
    def initialize_levels():
        """Initialize the levels based on the leveling design"""
        # These titles, descriptions, and perks are tailored for this app but are merely sample ideas
        levels_data = [
            {"level_number": 1, "level_xp": 0, "total_xp": 0, "xp_required": 0, "tier": 1, 
             "title": "Novice", "description": "Just starting out", "perks": "Basic access"},
            
            {"level_number": 2, "level_xp": 50, "total_xp": 50, "xp_required": 50, "tier": 1,
             "title": "Beginner", "description": "Taking first steps", "perks": "Basic features"},
            
            {"level_number": 3, "level_xp": 52, "total_xp": 102, "xp_required": 102, "tier": 1,
             "title": "Rookie", "description": "Learning the ropes", "perks": "Extra features"},
            
            {"level_number": 4, "level_xp": 54, "total_xp": 156, "xp_required": 156, "tier": 1,
             "title": "Participant", "description": "Regular attendee", "perks": "Attendance benefits"},
            
            {"level_number": 5, "level_xp": 56, "total_xp": 212, "xp_required": 212, "tier": 1,
             "title": "Active Member", "description": "Consistently active", "perks": "Activity rewards"},
            
            {"level_number": 6, "level_xp": 58, "total_xp": 270, "xp_required": 270, "tier": 2,
             "title": "Explorer", "description": "Exploring opportunities", "perks": "Tier 2 profile badge"},
            
            {"level_number": 7, "level_xp": 60, "total_xp": 330, "xp_required": 330, "tier": 2,
             "title": "Contributor", "description": "Contributing regularly", "perks": "Event highlights"},
            
            {"level_number": 8, "level_xp": 62, "total_xp": 392, "xp_required": 392, "tier": 2,
             "title": "Supporter", "description": "Supporting the community", "perks": "Special access"},
            
            {"level_number": 9, "level_xp": 64, "total_xp": 456, "xp_required": 456, "tier": 2,
             "title": "Established", "description": "Established community member", "perks": "Priority registration"},
            
            {"level_number": 10, "level_xp": 67, "total_xp": 523, "xp_required": 523, "tier": 2,
             "title": "Enthusiast", "description": "Enthusiastic participant", "perks": "Premium features"},
            
            {"level_number": 11, "level_xp": 70, "total_xp": 593, "xp_required": 593, "tier": 3,
             "title": "Organizer", "description": "Organizing events", "perks": "Tier 3 profile badge"},
            
            {"level_number": 12, "level_xp": 73, "total_xp": 666, "xp_required": 666, "tier": 3,
             "title": "Leader", "description": "Leading the community", "perks": "Create private events"},
            
            {"level_number": 13, "level_xp": 76, "total_xp": 742, "xp_required": 742, "tier": 3,
             "title": "Mentor", "description": "Mentoring others", "perks": "Enhanced profile"},
            
            {"level_number": 14, "level_xp": 79, "total_xp": 821, "xp_required": 821, "tier": 3,
             "title": "Guide", "description": "Guiding community members", "perks": "Special visibility"},
            
            {"level_number": 15, "level_xp": 82, "total_xp": 903, "xp_required": 903, "tier": 3,
             "title": "Expert", "description": "Expert community member", "perks": "Featured status"},
            
            {"level_number": 16, "level_xp": 85, "total_xp": 988, "xp_required": 988, "tier": 4,
             "title": "Veteran", "description": "Veteran member", "perks": "Tier 4 profile badge"},
            
            {"level_number": 17, "level_xp": 88, "total_xp": 1076, "xp_required": 1076, "tier": 4,
             "title": "Champion", "description": "Community champion", "perks": "Special rewards"},
            
            {"level_number": 18, "level_xp": 92, "total_xp": 1168, "xp_required": 1168, "tier": 4,
             "title": "Elite", "description": "Elite community member", "perks": "Premium benefits"},
            
            {"level_number": 19, "level_xp": 96, "total_xp": 1264, "xp_required": 1264, "tier": 4,
             "title": "Master", "description": "Mastered community participation", "perks": "Enhanced visibility"},
            
            {"level_number": 20, "level_xp": 100, "total_xp": 1364, "xp_required": 1364, "tier": 4,
             "title": "Grandmaster", "description": "Grand master of events", "perks": "Special recognition"},
            
            {"level_number": 21, "level_xp": 187, "total_xp": 1551, "xp_required": 1551, "tier": 5,
             "title": "Legend", "description": "Community legend", "perks": "Tier 5 profile badge"},
            
            {"level_number": 22, "level_xp": 152, "total_xp": 1703, "xp_required": 1703, "tier": 5,
             "title": "Icon", "description": "Community icon", "perks": "Legendary status"},
            
            {"level_number": 23, "level_xp": 118, "total_xp": 1821, "xp_required": 1821, "tier": 5,
             "title": "Ambassador", "description": "Community ambassador", "perks": "Special privileges"},
            
            {"level_number": 24, "level_xp": 84, "total_xp": 1905, "xp_required": 1905, "tier": 5,
             "title": "Paragon", "description": "Paragon of participation", "perks": "Exclusive features"},
            
            {"level_number": 25, "level_xp": 50, "total_xp": 1955, "xp_required": 1955, "tier": 5,
             "title": "Ultimate", "description": "Ultimate community member", "perks": "All features unlocked"}
        ]
        
        for level_data in levels_data:
            level = Level.query.filter_by(level_number=level_data["level_number"]).first()
            if level:
                # Update existing level
                level.level_xp = level_data["level_xp"]
                level.total_xp = level_data["total_xp"]
                level.tier = level_data["tier"]
                # Don't overwrite these if they already exist with custom values
                if not level.title or level.title == "":
                    level.title = level_data["title"]
                if not level.description or level.description == "":
                    level.description = level_data["description"]
                if not level.perks or level.perks == "":
                    level.perks = level_data["perks"]
                # Always update xp_required to match total_xp
                level.xp_required = level_data["total_xp"]
            else:
                # Create new level
                level = Level(**level_data)
                db.session.add(level)
        
        db.session.commit()