# models/level.py
from . import db

class Level(db.Model):
    __tablename__ = 'levels'
    
    id = db.Column(db.Integer, primary_key=True)
    level_number = db.Column(db.Integer, unique=True, nullable=False)
    total_xp = db.Column(db.Integer, nullable=False)  # Cumulative XP to reach this level
    title = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(255))
    perks = db.Column(db.String(255))
    tier = db.Column(db.Integer, nullable=False, default=1)  # Tier category
    
    # Remove redundant xp_required and level_xp columns
    
    def __repr__(self):
        return f'<Level {self.level_number}: {self.title}>'
    
    @property
    def level_xp(self):
        """Calculate XP required for just this level (derived from total_xp)"""
        if self.level_number == 1:
            return 0
            
        # Get the previous level's total_xp
        prev_level = Level.query.filter_by(level_number=self.level_number - 1).first()
        if prev_level:
            return self.total_xp - prev_level.total_xp
        
        # Fallback if previous level not found
        return self.total_xp

    @staticmethod
    def initialize_levels():
        """Initialize the levels based on the leveling design"""
        # These titles, descriptions, and perks are tailored for this app but are merely sample ideas
        levels_data = [
            {"level_number": 1, "total_xp": 0, "tier": 1, 
             "title": "Novice", "description": "Just starting out", "perks": "Basic access"},
            
            {"level_number": 2, "total_xp": 50, "tier": 1,
             "title": "Beginner", "description": "Taking first steps", "perks": "Basic features"},
            
            {"level_number": 3, "total_xp": 102, "tier": 1,
             "title": "Rookie", "description": "Learning the ropes", "perks": "Extra features"},
            
            {"level_number": 4, "total_xp": 156, "tier": 1,
             "title": "Participant", "description": "Regular attendee", "perks": "Attendance benefits"},
            
            {"level_number": 5, "total_xp": 212, "tier": 1,
             "title": "Active Member", "description": "Consistently active", "perks": "Activity rewards"},
            
            {"level_number": 6, "total_xp": 270, "tier": 2,
             "title": "Explorer", "description": "Exploring opportunities", "perks": "Tier 2 profile badge"},
            
            {"level_number": 7, "total_xp": 330, "tier": 2,
             "title": "Contributor", "description": "Contributing regularly", "perks": "Event highlights"},
            
            {"level_number": 8, "total_xp": 392, "tier": 2,
             "title": "Supporter", "description": "Supporting the community", "perks": "Special access"},
            
            {"level_number": 9, "total_xp": 456, "tier": 2,
             "title": "Established", "description": "Established community member", "perks": "Priority registration"},
            
            {"level_number": 10, "total_xp": 523, "tier": 2,
             "title": "Enthusiast", "description": "Enthusiastic participant", "perks": "Premium features"},
            
            {"level_number": 11, "total_xp": 593, "tier": 3,
             "title": "Organizer", "description": "Organizing events", "perks": "Tier 3 profile badge"},
            
            {"level_number": 12, "total_xp": 666, "tier": 3,
             "title": "Leader", "description": "Leading the community", "perks": "Create private events"},
            
            {"level_number": 13, "total_xp": 742, "tier": 3,
             "title": "Mentor", "description": "Mentoring others", "perks": "Enhanced profile"},
            
            {"level_number": 14, "total_xp": 821, "tier": 3,
             "title": "Guide", "description": "Guiding community members", "perks": "Special visibility"},
            
            {"level_number": 15, "total_xp": 903, "tier": 3,
             "title": "Expert", "description": "Expert community member", "perks": "Featured status"},
            
            {"level_number": 16, "total_xp": 988, "tier": 4,
             "title": "Veteran", "description": "Veteran member", "perks": "Tier 4 profile badge"},
            
            {"level_number": 17, "total_xp": 1076, "tier": 4,
             "title": "Champion", "description": "Community champion", "perks": "Special rewards"},
            
            {"level_number": 18, "total_xp": 1168, "tier": 4,
             "title": "Elite", "description": "Elite community member", "perks": "Premium benefits"},
            
            {"level_number": 19, "total_xp": 1264, "tier": 4,
             "title": "Master", "description": "Mastered community participation", "perks": "Enhanced visibility"},
            
            {"level_number": 20, "total_xp": 1364, "tier": 4,
             "title": "Grandmaster", "description": "Grand master of events", "perks": "Special recognition"},
            
            {"level_number": 21, "total_xp": 1551, "tier": 5,
             "title": "Legend", "description": "Community legend", "perks": "Tier 5 profile badge"},
            
            {"level_number": 22, "total_xp": 1703, "tier": 5,
             "title": "Icon", "description": "Community icon", "perks": "Legendary status"},
            
            {"level_number": 23, "total_xp": 1821, "tier": 5,
             "title": "Ambassador", "description": "Community ambassador", "perks": "Special privileges"},
            
            {"level_number": 24, "total_xp": 1905, "tier": 5,
             "title": "Paragon", "description": "Paragon of participation", "perks": "Exclusive features"},
            
            {"level_number": 25, "total_xp": 1955, "tier": 5,
             "title": "Ultimate", "description": "Ultimate community member", "perks": "All features unlocked"}
        ]
        
        for level_data in levels_data:
            level = Level.query.filter_by(level_number=level_data["level_number"]).first()
            if level:
                # Update existing level
                level.total_xp = level_data["total_xp"]
                level.tier = level_data["tier"]
                # Don't overwrite these if they already exist with custom values
                if not level.title or level.title == "":
                    level.title = level_data["title"]
                if not level.description or level.description == "":
                    level.description = level_data["description"]
                if not level.perks or level.perks == "":
                    level.perks = level_data["perks"]
            else:
                # Create new level
                level = Level(**level_data)
                db.session.add(level)
        
        db.session.commit()