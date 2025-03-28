# models/drop_rate.py
from . import db
from sqlalchemy import inspect

class LootBoxDropRate(db.Model):
    """Defines the drop rates for different loot box tiers based on player level"""
    __tablename__ = 'loot_box_drop_rates'
    
    id = db.Column(db.Integer, primary_key=True)
    level_min = db.Column(db.Integer, nullable=False)  # Minimum level for this range
    level_max = db.Column(db.Integer, nullable=False)  # Maximum level for this range
    tier_1_rate = db.Column(db.Float, default=0)  # Drop rate percentage for Tier 1 boxes
    tier_2_rate = db.Column(db.Float, default=0)  # Drop rate percentage for Tier 2 boxes
    tier_3_rate = db.Column(db.Float, default=0)  # Drop rate percentage for Tier 3 boxes
    tier_4_rate = db.Column(db.Float, default=0)  # Drop rate percentage for Tier 4 boxes
    
    def __repr__(self):
        return f'<LootBoxDropRate Lvl {self.level_min}-{self.level_max}>'


class RewardDropRate(db.Model):
    """Defines the drop rates for different reward tiers based on loot box tier"""
    __tablename__ = 'reward_drop_rates'
    
    id = db.Column(db.Integer, primary_key=True)
    loot_box_tier = db.Column(db.Integer, nullable=False)  # Tier of the loot box (1-4)
    tier_1_rate = db.Column(db.Float, default=0)  # Drop rate percentage for Tier 1 rewards
    tier_2_rate = db.Column(db.Float, default=0)  # Drop rate percentage for Tier 2 rewards
    tier_3_rate = db.Column(db.Float, default=0)  # Drop rate percentage for Tier 3 rewards
    tier_4_rate = db.Column(db.Float, default=0)  # Drop rate percentage for Tier 4 rewards
    
    def __repr__(self):
        return f'<RewardDropRate Box Tier {self.loot_box_tier}>'


def table_exists(table_name):
    """Check if a table exists in the database"""
    inspector = inspect(db.engine)
    return table_name in inspector.get_table_names()


def initialize_drop_rates():
    """Initialize default drop rates based on the reward system design"""
    # Check if tables exist before attempting to populate them
    if not table_exists('loot_box_drop_rates') or not table_exists('reward_drop_rates'):
        print("Drop rate tables don't exist yet - skipping initialization")
        return
    
    # Initialize loot box drop rates by level tier
    loot_box_rates = [
        {
            "level_min": 1, "level_max": 5,
            "tier_1_rate": 80.0, "tier_2_rate": 15.0, "tier_3_rate": 4.0, "tier_4_rate": 1.0
        },
        {
            "level_min": 6, "level_max": 10,
            "tier_1_rate": 0.0, "tier_2_rate": 75.0, "tier_3_rate": 19.0, "tier_4_rate": 6.0
        },
        {
            "level_min": 11, "level_max": 15,
            "tier_1_rate": 0.0, "tier_2_rate": 65.0, "tier_3_rate": 25.0, "tier_4_rate": 10.0
        },
        {
            "level_min": 16, "level_max": 20,
            "tier_1_rate": 0.0, "tier_2_rate": 50.0, "tier_3_rate": 35.0, "tier_4_rate": 15.0
        },
        {
            "level_min": 21, "level_max": 25,
            "tier_1_rate": 0.0, "tier_2_rate": 40.0, "tier_3_rate": 35.0, "tier_4_rate": 25.0
        }
    ]
    
    # Initialize reward drop rates by loot box tier
    reward_rates = [
        {
            "loot_box_tier": 1,
            "tier_1_rate": 75.0, "tier_2_rate": 20.0, "tier_3_rate": 4.5, "tier_4_rate": 0.5
        },
        {
            "loot_box_tier": 2,
            "tier_1_rate": 45.0, "tier_2_rate": 40.0, "tier_3_rate": 12.0, "tier_4_rate": 3.0
        },
        {
            "loot_box_tier": 3,
            "tier_1_rate": 20.0, "tier_2_rate": 40.0, "tier_3_rate": 30.0, "tier_4_rate": 10.0
        },
        {
            "loot_box_tier": 4,
            "tier_1_rate": 0.0, "tier_2_rate": 35.0, "tier_3_rate": 45.0, "tier_4_rate": 20.0
        }
    ]
    
    # Add loot box drop rates if they don't exist yet
    for rate_data in loot_box_rates:
        existing = LootBoxDropRate.query.filter_by(
            level_min=rate_data["level_min"], 
            level_max=rate_data["level_max"]
        ).first()
        
        if not existing:
            new_rate = LootBoxDropRate(**rate_data)
            db.session.add(new_rate)
    
    # Add reward drop rates if they don't exist yet
    for rate_data in reward_rates:
        existing = RewardDropRate.query.filter_by(
            loot_box_tier=rate_data["loot_box_tier"]
        ).first()
        
        if not existing:
            new_rate = RewardDropRate(**rate_data)
            db.session.add(new_rate)
    
    db.session.commit()