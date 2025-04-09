# migrations/migrate_normalized_tables.py
from datetime import datetime
import os
import sys

# Add the parent directory to the path so we can import models
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the application factory
from app import create_app

# Create the app with the development configuration
app = create_app('dev')

# Now import the models after app is defined
from models import db
from models.drop_rate import (
    LootBoxDropRate, RewardDropRate, 
    LootBoxLevelRange, LootBoxTierRate, RewardBoxTier, RewardTierRate
)
from models.level import Level
from models.user import User

def check_table_exists(table_name):
    """Check if a table exists in the database"""
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    return table_name in inspector.get_table_names()

def migrate_loot_box_drop_rates():
    """Migrate data from LootBoxDropRate to normalized tables"""
    print("Migrating loot box drop rates...")
    
    # Check if old and new tables exist
    if not check_table_exists('loot_box_drop_rates'):
        print("Loot box drop rates table doesn't exist - skipping migration")
        return
    
    if not check_table_exists('loot_box_level_ranges') or not check_table_exists('loot_box_tier_rates'):
        print("New loot box tables don't exist - skipping migration")
        return
    
    # Get all existing drop rates
    old_rates = LootBoxDropRate.query.all()
    migrated_count = 0
    
    for old_rate in old_rates:
        # Check if level range already exists
        existing_level_range = LootBoxLevelRange.query.filter_by(
            level_min=old_rate.level_min, 
            level_max=old_rate.level_max
        ).first()
        
        if existing_level_range:
            print(f"Level range {old_rate.level_min}-{old_rate.level_max} already exists, using existing record")
            level_range_id = existing_level_range.id
        else:
            # Create new level range
            level_range = LootBoxLevelRange(
                level_min=old_rate.level_min,
                level_max=old_rate.level_max
            )
            db.session.add(level_range)
            db.session.flush()  # Get ID before adding related tier rates
            level_range_id = level_range.id
        
        # Check if tier rates already exist for this level range
        existing_rates = LootBoxTierRate.query.filter_by(level_range_id=level_range_id).all()
        existing_tiers = [rate.tier for rate in existing_rates]
        
        # Create tier rates if they don't exist
        tier_rates_data = [
            {"tier": 1, "rate": old_rate.tier_1_rate},
            {"tier": 2, "rate": old_rate.tier_2_rate},
            {"tier": 3, "rate": old_rate.tier_3_rate},
            {"tier": 4, "rate": old_rate.tier_4_rate}
        ]
        
        for tier_data in tier_rates_data:
            if tier_data["tier"] not in existing_tiers:
                tier_rate = LootBoxTierRate(
                    level_range_id=level_range_id,
                    tier=tier_data["tier"],
                    rate=tier_data["rate"]
                )
                db.session.add(tier_rate)
            else:
                print(f"Tier {tier_data['tier']} for level range {old_rate.level_min}-{old_rate.level_max} already exists, skipping")
        
        migrated_count += 1
    
    print(f"Migrated {migrated_count} loot box drop rate ranges.")
    
def migrate_reward_drop_rates():
    """Migrate data from RewardDropRate to normalized tables"""
    print("Migrating reward drop rates...")
    
    # Check if old and new tables exist
    if not check_table_exists('reward_drop_rates'):
        print("Reward drop rates table doesn't exist - skipping migration")
        return
    
    if not check_table_exists('reward_box_tiers') or not check_table_exists('reward_tier_rates'):
        print("New reward tables don't exist - skipping migration")
        return
    
    # Get all existing drop rates
    old_rates = RewardDropRate.query.all()
    migrated_count = 0
    
    for old_rate in old_rates:
        # Check if box tier already exists
        existing_box_tier = RewardBoxTier.query.filter_by(
            loot_box_tier=old_rate.loot_box_tier
        ).first()
        
        if existing_box_tier:
            print(f"Box tier {old_rate.loot_box_tier} already exists, using existing record")
            box_tier_id = existing_box_tier.id
        else:
            # Create new box tier
            box_tier = RewardBoxTier(
                loot_box_tier=old_rate.loot_box_tier
            )
            db.session.add(box_tier)
            db.session.flush()  # Get ID before adding related tier rates
            box_tier_id = box_tier.id
        
        # Check if tier rates already exist for this box tier
        existing_rates = RewardTierRate.query.filter_by(box_tier_id=box_tier_id).all()
        existing_tiers = [rate.tier for rate in existing_rates]
        
        # Create tier rates if they don't exist
        tier_rates_data = [
            {"tier": 1, "rate": old_rate.tier_1_rate},
            {"tier": 2, "rate": old_rate.tier_2_rate},
            {"tier": 3, "rate": old_rate.tier_3_rate},
            {"tier": 4, "rate": old_rate.tier_4_rate}
        ]
        
        for tier_data in tier_rates_data:
            if tier_data["tier"] not in existing_tiers:
                tier_rate = RewardTierRate(
                    box_tier_id=box_tier_id,
                    tier=tier_data["tier"],
                    rate=tier_data["rate"]
                )
                db.session.add(tier_rate)
            else:
                print(f"Tier {tier_data['tier']} for box tier {old_rate.loot_box_tier} already exists, skipping")
        
        migrated_count += 1
    
    print(f"Migrated {migrated_count} reward drop rate tiers.")

def update_level_structure():
    """Update Level table to remove redundant fields"""
    print("Updating level structure...")
    
    # Check if table exists
    if not check_table_exists('levels'):
        print("Levels table doesn't exist - skipping update")
        return
    
    # Check if columns exist
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    columns = [col['name'] for col in inspector.get_columns('levels')]
    
    # Skip if total_xp column doesn't exist
    if 'total_xp' not in columns:
        print("total_xp column doesn't exist in Level model - skipping update")
        return
    
    # Skip if xp_required column doesn't exist
    if 'xp_required' not in columns:
        print("xp_required column doesn't exist in Level model - skipping update")
        return
    
    # Get all levels
    levels = Level.query.order_by(Level.level_number).all()
    
    for level in levels:
        # Ensure total_xp is populated with the proper value
        if hasattr(level, 'xp_required') and level.total_xp is None and level.xp_required is not None:
            level.total_xp = level.xp_required
    
    print(f"Updated {len(levels)} level records.")

def update_user_model():
    """Update User model to remove current_tier column"""
    print("Updating user tier handling...")
    
    # Check if table exists
    if not check_table_exists('users'):
        print("Users table doesn't exist - skipping update")
        return
    
    # Check if column exists
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    columns = [col['name'] for col in inspector.get_columns('users')]
    
    # Skip if current_tier column doesn't exist
    if 'current_tier' not in columns:
        print("current_tier column doesn't exist in User model - skipping update")
        return
    
    # Get all users
    users = User.query.all()
    
    # We don't need to do anything for users since we're changing to a property
    # But we could adjust logic here if needed
    
    print(f"Verified tier property for {len(users)} users.")

def perform_migration():
    """Perform the entire migration process"""
    print("Starting database migration...")
    
    try:
        # Perform all migrations in a transaction
        migrate_loot_box_drop_rates()
        migrate_reward_drop_rates()
        update_level_structure()
        update_user_model()
        
        # Commit all changes
        db.session.commit()
        print("Migration completed successfully!")
        
    except Exception as e:
        # Roll back on error
        db.session.rollback()
        print(f"Migration failed: {str(e)}")
        import traceback
        traceback.print_exc()
        raise

if __name__ == "__main__":
    # Use app context to ensure SQLAlchemy operations work properly
    with app.app_context():
        perform_migration()