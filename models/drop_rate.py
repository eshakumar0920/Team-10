# models/drop_rate.py
from . import db
from sqlalchemy import inspect

# Original models - needed for backwards compatibility during migration
class LootBoxDropRate(db.Model):
    """Defines the drop rates for different loot box tiers based on player level"""
    __tablename__ = 'loot_box_drop_rates'
    
    id = db.Column(db.Integer, primary_key=True)
    level_min = db.Column(db.Integer, nullable=False)
    level_max = db.Column(db.Integer, nullable=False)
    tier_1_rate = db.Column(db.Float, default=0)
    tier_2_rate = db.Column(db.Float, default=0)
    tier_3_rate = db.Column(db.Float, default=0)
    tier_4_rate = db.Column(db.Float, default=0)
    
    def __repr__(self):
        return f'<LootBoxDropRate Lvl {self.level_min}-{self.level_max}>'
    
# Original models - needed for backwards compatibility during migration
class RewardDropRate(db.Model):
    """Defines the drop rates for different reward tiers based on loot box tier"""
    __tablename__ = 'reward_drop_rates'
    
    id = db.Column(db.Integer, primary_key=True)
    loot_box_tier = db.Column(db.Integer, nullable=False)
    tier_1_rate = db.Column(db.Float, default=0)
    tier_2_rate = db.Column(db.Float, default=0)
    tier_3_rate = db.Column(db.Float, default=0)
    tier_4_rate = db.Column(db.Float, default=0)
    
    def __repr__(self):
        return f'<RewardDropRate Box Tier {self.loot_box_tier}>'
     
class LootBoxLevelRange(db.Model):
    """Defines the level ranges for loot box drop rates"""
    __tablename__ = 'loot_box_level_ranges'
    
    id = db.Column(db.Integer, primary_key=True)
    level_min = db.Column(db.Integer, nullable=False)  # Minimum level for this range
    level_max = db.Column(db.Integer, nullable=False)  # Maximum level for this range
    
    # Relationship with drop rates
    drop_rates = db.relationship('LootBoxTierRate', back_populates='level_range', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<LootBoxLevelRange Lvl {self.level_min}-{self.level_max}>'


class LootBoxTierRate(db.Model):
    """Defines the drop rate for a specific tier and level range"""
    __tablename__ = 'loot_box_tier_rates'
    
    id = db.Column(db.Integer, primary_key=True)
    level_range_id = db.Column(db.Integer, db.ForeignKey('loot_box_level_ranges.id'), nullable=False)
    tier = db.Column(db.Integer, nullable=False)  # The tier (1-4)
    rate = db.Column(db.Float, default=0)  # Drop rate percentage for this tier
    
    # Relationship with level range
    level_range = db.relationship('LootBoxLevelRange', back_populates='drop_rates')
    
    __table_args__ = (
        db.UniqueConstraint('level_range_id', 'tier', name='unique_loot_box_tier_rate'),
    )
    
    def __repr__(self):
        return f'<LootBoxTierRate Level Range {self.level_range_id}, Tier {self.tier}: {self.rate}%>'


class RewardBoxTier(db.Model):
    """Defines the loot box tiers for reward drop rates"""
    __tablename__ = 'reward_box_tiers'
    
    id = db.Column(db.Integer, primary_key=True)
    loot_box_tier = db.Column(db.Integer, nullable=False, unique=True)  # Tier of the loot box (1-4)
    
    # Relationship with drop rates
    drop_rates = db.relationship('RewardTierRate', back_populates='box_tier', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<RewardBoxTier {self.loot_box_tier}>'


class RewardTierRate(db.Model):
    """Defines the drop rate for a specific reward tier and box tier"""
    __tablename__ = 'reward_tier_rates'
    
    id = db.Column(db.Integer, primary_key=True)
    box_tier_id = db.Column(db.Integer, db.ForeignKey('reward_box_tiers.id'), nullable=False)
    tier = db.Column(db.Integer, nullable=False)  # The reward tier (1-4)
    rate = db.Column(db.Float, default=0)  # Drop rate percentage for this tier
    
    # Relationship with box tier
    box_tier = db.relationship('RewardBoxTier', back_populates='drop_rates')
    
    __table_args__ = (
        db.UniqueConstraint('box_tier_id', 'tier', name='unique_reward_tier_rate'),
    )
    
    def __repr__(self):
        return f'<RewardTierRate Box Tier {self.box_tier_id}, Reward Tier {self.tier}: {self.rate}%>'


def table_exists(table_name):
    """Check if a table exists in the database"""
    inspector = inspect(db.engine)
    return table_name in inspector.get_table_names()


def initialize_drop_rates():
    """Initialize default drop rates based on the reward system design"""
    # Check if tables exist before attempting to populate them
    if not (table_exists('loot_box_level_ranges') and table_exists('loot_box_tier_rates') and 
            table_exists('reward_box_tiers') and table_exists('reward_tier_rates')):
        print("Drop rate tables don't exist yet - skipping initialization")
        return
    
    # Initialize loot box level ranges and drop rates
    loot_box_ranges = [
        {
            "level_min": 1,
            "level_max": 5,
            "tier_rates": [
                {"tier": 1, "rate": 80.0},
                {"tier": 2, "rate": 15.0},
                {"tier": 3, "rate": 4.0},
                {"tier": 4, "rate": 1.0}
            ]
        },
        {
            "level_min": 6,
            "level_max": 10,
            "tier_rates": [
                {"tier": 1, "rate": 0.0},
                {"tier": 2, "rate": 75.0},
                {"tier": 3, "rate": 19.0},
                {"tier": 4, "rate": 6.0}
            ]
        },
        {
            "level_min": 11,
            "level_max": 15,
            "tier_rates": [
                {"tier": 1, "rate": 0.0},
                {"tier": 2, "rate": 65.0},
                {"tier": 3, "rate": 25.0},
                {"tier": 4, "rate": 10.0}
            ]
        },
        {
            "level_min": 16,
            "level_max": 20,
            "tier_rates": [
                {"tier": 1, "rate": 0.0},
                {"tier": 2, "rate": 50.0},
                {"tier": 3, "rate": 35.0},
                {"tier": 4, "rate": 15.0}
            ]
        },
        {
            "level_min": 21,
            "level_max": 25,
            "tier_rates": [
                {"tier": 1, "rate": 0.0},
                {"tier": 2, "rate": 40.0},
                {"tier": 3, "rate": 35.0},
                {"tier": 4, "rate": 25.0}
            ]
        }
    ]
    
    # Initialize reward box tiers and drop rates
    reward_tiers = [
        {
            "loot_box_tier": 1,
            "tier_rates": [
                {"tier": 1, "rate": 75.0},
                {"tier": 2, "rate": 20.0},
                {"tier": 3, "rate": 4.5},
                {"tier": 4, "rate": 0.5}
            ]
        },
        {
            "loot_box_tier": 2,
            "tier_rates": [
                {"tier": 1, "rate": 45.0},
                {"tier": 2, "rate": 40.0},
                {"tier": 3, "rate": 12.0},
                {"tier": 4, "rate": 3.0}
            ]
        },
        {
            "loot_box_tier": 3,
            "tier_rates": [
                {"tier": 1, "rate": 20.0},
                {"tier": 2, "rate": 40.0},
                {"tier": 3, "rate": 30.0},
                {"tier": 4, "rate": 10.0}
            ]
        },
        {
            "loot_box_tier": 4,
            "tier_rates": [
                {"tier": 1, "rate": 0.0},
                {"tier": 2, "rate": 35.0},
                {"tier": 3, "rate": 45.0},
                {"tier": 4, "rate": 20.0}
            ]
        }
    ]
    
    # Add loot box level ranges and their tier rates
    for range_data in loot_box_ranges:
        tier_rates = range_data.pop("tier_rates")
        existing = LootBoxLevelRange.query.filter_by(
            level_min=range_data["level_min"], 
            level_max=range_data["level_max"]
        ).first()
        
        if not existing:
            level_range = LootBoxLevelRange(**range_data)
            db.session.add(level_range)
            db.session.flush()  # Get ID before adding related tier rates
            
            for tier_data in tier_rates:
                tier_rate = LootBoxTierRate(
                    level_range_id=level_range.id,
                    tier=tier_data["tier"],
                    rate=tier_data["rate"]
                )
                db.session.add(tier_rate)
    
    # Add reward box tiers and their tier rates
    for tier_data in reward_tiers:
        tier_rates = tier_data.pop("tier_rates")
        existing = RewardBoxTier.query.filter_by(
            loot_box_tier=tier_data["loot_box_tier"]
        ).first()
        
        if not existing:
            box_tier = RewardBoxTier(**tier_data)
            db.session.add(box_tier)
            db.session.flush()  # Get ID before adding related tier rates
            
            for rate_data in tier_rates:
                tier_rate = RewardTierRate(
                    box_tier_id=box_tier.id,
                    tier=rate_data["tier"],
                    rate=rate_data["rate"]
                )
                db.session.add(tier_rate)
    
    db.session.commit()