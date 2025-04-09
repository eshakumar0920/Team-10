'''
This script populates the database with sample data in order to test API endpoints
-PG
'''
# test_seed.py
import time
import random
from datetime import datetime
from app import create_app, db
from models import User, RewardType, UserReward
from sqlalchemy.exc import IntegrityError

# Try to import LootBox model if it exists
try:
    from models import LootBox
    has_lootbox_model = True
except ImportError:
    has_lootbox_model = False
    print("LootBox model not found - will try to create user reward without loot box")

# Create the app with the development configuration
app = create_app('dev')

# Create app context
with app.app_context():
    # Check if testuser already exists
    existing_user = User.query.filter_by(username="testuser").first()
    
    if existing_user:
        print(f"User 'testuser' already exists with ID: {existing_user.id}")
        test_user = existing_user
    else:
        # Create a new test user with a unique username
        timestamp = int(time.time())
        test_user = User(username=f"testuser_{timestamp}", 
                         email=f"test_{timestamp}@example.com")
        
        # Add password if required by your model
        if hasattr(test_user, 'set_password'):
            test_user.set_password("password123")
        
        try:
            db.session.add(test_user)
            db.session.commit()
            print(f"Created new test user with ID: {test_user.id}")
        except IntegrityError:
            db.session.rollback()
            print("Could not create user due to integrity error.")
            # Try with an even more unique username
            new_timestamp = int(time.time())
            test_user = User(username=f"testuser_{new_timestamp}", 
                             email=f"test_{new_timestamp}@example.com")
            db.session.add(test_user)
            db.session.commit()
            print(f"Created alternate test user with ID: {test_user.id}")
    
    # Create a loot box if the model is available
    loot_box_id = None
    if has_lootbox_model:
        # Check if a loot box already exists
        existing_lootbox = LootBox.query.first()
        if existing_lootbox:
            loot_box_id = existing_lootbox.id
            print(f"Using existing loot box with ID: {loot_box_id}")
        else:
            # Create a new loot box
            try:
                loot_box = LootBox(
                    name="Test Loot Box",
                    tier="common",
                    user_id=test_user.id
                    # Add other required fields as needed
                )
                db.session.add(loot_box)
                db.session.commit()
                loot_box_id = loot_box.id
                print(f"Created loot box with ID: {loot_box_id}")
            except Exception as e:
                db.session.rollback()
                print(f"Error creating loot box: {type(e).__name__}: {str(e)}")
    
    # Test creating a reward type
    try:
        random_num = random.randint(1000, 9999)
        test_reward = RewardType(
            name=f"Test Reward {random_num}",
            description="A reward for testing purposes",
            image_url="https://example.com/image.png",
            tier="1",
            category="achievement",
            theme="testing",
            is_rare=False
        )
        db.session.add(test_reward)
        db.session.commit()
        print(f"Created reward type with ID: {test_reward.id}")
    except IntegrityError:
        db.session.rollback()
        print("Could not create reward type due to integrity error.")
        # Get an existing reward type instead
        test_reward = RewardType.query.first()
        if test_reward:
            print(f"Using existing reward type with ID: {test_reward.id}")
        else:
            print("No reward types found in database.")
            exit(1)
    
    # Create a user reward (assign the reward to the user)
    try:
        # Check if loot_box_id is nullable
        is_nullable = UserReward.__table__.columns['loot_box_id'].nullable
        print(f"loot_box_id column is nullable: {is_nullable}")
        
        # Create new reward for user
        user_reward = UserReward(
            user_id=test_user.id,
            reward_type_id=test_reward.id,
            is_equipped=False,
            acquired_at=datetime.now()
        )
        
        # Only set loot_box_id if we have a valid ID or if the column is not nullable
        if loot_box_id is not None:
            user_reward.loot_box_id = loot_box_id
        elif not is_nullable:
            print("Warning: loot_box_id is required but no loot box exists")
            # Try to create a minimal valid record by directly executing SQL
            from sqlalchemy import text
            sql = text("""
                INSERT INTO user_rewards (user_id, reward_type_id, is_equipped, acquired_at, loot_box_id)
                VALUES (:user_id, :reward_type_id, :is_equipped, :acquired_at, NULL)
                RETURNING id
            """)
            result = db.session.execute(sql, {
                'user_id': test_user.id,
                'reward_type_id': test_reward.id,
                'is_equipped': False,
                'acquired_at': datetime.now()
            })
            user_reward_id = result.fetchone()[0]
            db.session.commit()
            print(f"Created user reward with ID: {user_reward_id} using direct SQL")
            user_reward = UserReward.query.get(user_reward_id)
            
        else:
            # Column is nullable, proceed with the ORM approach
            print("Adding user reward with loot_box_id=NULL")
            db.session.add(user_reward)
            db.session.commit()
            print(f"Created user reward with ID: {user_reward.id}")
    except Exception as e:
        db.session.rollback()
        print(f"Error creating user reward: {type(e).__name__}: {str(e)}")
        print("Could not create user reward after multiple attempts.")
    
    print("\nTest endpoints:")
    print(f"GET http://localhost:5000/api/rewards/users/{test_user.id}/rewards")
    if 'user_reward' in locals() and user_reward and hasattr(user_reward, 'id') and user_reward.id is not None:
        print(f"POST http://localhost:5000/api/rewards/users/{test_user.id}/rewards/{user_reward.id}/equip")