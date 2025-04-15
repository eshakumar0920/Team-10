import os
import sys
import unittest
from unittest.mock import patch, MagicMock
import random
from datetime import datetime, UTC
from flask import Flask
from sqlalchemy import text, Column, DateTime

# Add parent directory to path so we can import application modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the models
from config import config_by_name
from models import db
from models.user import User
from models.loot_box import LootBox, LootBoxType
from models.reward import RewardType, UserReward
from models.drop_rate import LootBoxDropRate, RewardDropRate
from models.reward_system import RewardSystem

class RewardSystemTestCase(unittest.TestCase):
    """Test cases for the reward system functionality"""
    
    def setUp(self):
        """Set up test environment before each test"""
        # Create a test Flask app
        self.app = Flask(__name__)
        self.app.config.from_object(config_by_name['test'])
        
        # Initialize database
        db.init_app(self.app)

        self.app_context = self.app.app_context()
        self.app_context.push()

        # optional: create a test DB or tables here
        db.drop_all()
        db.create_all()
        
        # Seed the database with test data
        self._create_test_data()
    
    def tearDown(self):
        """Clean up after each test"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def _create_test_data(self):
        """Create test data for the tests"""
        # Create test user
        self.test_user = User(
            username="testuser",
            email="test@example.com",
            password_hash="fakehash",
            current_level=10
        )
        db.session.add(self.test_user)
        
        # Create loot box types (one for each tier)
        for tier in range(1, 5):
            box_type = LootBoxType(
                name=f"Tier {tier} Box",
                description=f"A tier {tier} loot box",
                tier=tier,
                icon_url=f"/static/images/box_tier_{tier}.png"
            )
            db.session.add(box_type)
        
        # Create reward types (multiple per tier)
        tiers = [1, 2, 3, 4]
        categories = ["Season", "Event", "Unique"]
        themes = ["Fall", "Winter", "Sport", "Coding"]
        
        for tier in tiers:
            for i in range(3):  # 3 rewards per tier
                reward_type = RewardType(
                    name=f"Tier {tier} Reward {i+1}",
                    description=f"A tier {tier} reward item",
                    image_url=f"/static/images/reward_tier_{tier}_{i+1}.png",
                    tier=tier,
                    category=random.choice(categories),
                    theme=random.choice(themes),
                    is_rare=(tier == 4 and i == 0)  # Make one tier 4 reward rare
                )
                db.session.add(reward_type)
        
        # Create drop rate tables
        # Loot box drop rates
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
            }
        ]
        
        for rate_data in loot_box_rates:
            db.session.add(LootBoxDropRate(**rate_data))
        
        # Reward drop rates
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
        
        for rate_data in reward_rates:
            db.session.add(RewardDropRate(**rate_data))
        
        db.session.commit()
    
    @patch('random.uniform')
    def test_determine_loot_box_tier(self, mock_uniform):
        """Test that loot box tiers are determined correctly based on user level and RNG"""
        # Force different random rolls to test all tiers
        
        # Test level 7 user (falls in 6-10 range)
        # Tier 2 box (75% chance) - Set roll to 30%
        mock_uniform.return_value = 30.0
        tier = RewardSystem.determine_loot_box_tier(7)
        self.assertEqual(tier, 2)
        
        # Tier 3 box (19% chance) - Set roll to 80%
        mock_uniform.return_value = 80.0
        tier = RewardSystem.determine_loot_box_tier(7)
        self.assertEqual(tier, 3)
        
        # Tier 4 box (6% chance) - Set roll to 95%
        mock_uniform.return_value = 95.0
        tier = RewardSystem.determine_loot_box_tier(7)
        self.assertEqual(tier, 4)
        
        # Test edge case: level outside defined ranges
        mock_uniform.return_value = 50.0
        tier = RewardSystem.determine_loot_box_tier(30)
        self.assertEqual(tier, 1)  # Should default to tier 1
    
    @patch('random.uniform')
    def test_determine_reward_tier(self, mock_uniform):
        """Test that reward tiers are determined correctly based on loot box tier and RNG"""
        # Test with tier 3 loot box
        
        # Tier 1 reward (20% chance) - Set roll to 10%
        mock_uniform.return_value = 10.0
        tier = RewardSystem.determine_reward_tier(3)
        self.assertEqual(tier, 1)
        
        # Tier 2 reward (40% chance) - Set roll to 30%
        mock_uniform.return_value = 30.0
        tier = RewardSystem.determine_reward_tier(3)
        self.assertEqual(tier, 2)
        
        # Tier 3 reward (30% chance) - Set roll to 70%
        mock_uniform.return_value = 70.0
        tier = RewardSystem.determine_reward_tier(3)
        self.assertEqual(tier, 3)
        
        # Tier 4 reward (10% chance) - Set roll to 95%
        mock_uniform.return_value = 95.0
        tier = RewardSystem.determine_reward_tier(3)
        self.assertEqual(tier, 4)
    
    @patch('random.choice')
    def test_select_random_reward(self, mock_choice):
        """Test selecting a random reward of a given tier"""
        # Mock the random.choice to return the first reward of tier 2
        tier_2_rewards = RewardType.query.filter_by(tier=2).all()
        mock_choice.return_value = tier_2_rewards[0]
        
        # Select a reward
        reward = RewardSystem.select_random_reward(2, self.test_user.id)
        
        # Verify the reward
        self.assertIsNotNone(reward)
        self.assertEqual(reward.tier, 2)
        self.assertEqual(reward.id, tier_2_rewards[0].id)
    
    @patch('models.reward_system.RewardSystem.determine_loot_box_tier')
    def test_award_loot_box_for_level_up(self, mock_determine_tier):
        """Test awarding a loot box for leveling up"""
        # Mock the tier determination to return tier 3
        mock_determine_tier.return_value = 3
        
        # Award loot box for leveling up
        loot_box = RewardSystem.award_loot_box_for_level_up(
            self.test_user.id, 
            12,  # New level
            "level_up"
        )
        
        # Verify the loot box
        self.assertIsNotNone(loot_box)
        self.assertEqual(loot_box.user_id, self.test_user.id)
        self.assertEqual(loot_box.is_opened, False)
        
        # Verify the loot box type
        loot_box_type = db.session.get(LootBoxType, loot_box.type_id)
        self.assertEqual(loot_box_type.tier, 3)
        self.assertEqual(loot_box.awarded_for, "level_up_level_12")
    
    @patch('models.reward_system.RewardSystem.determine_reward_tier')
    @patch('models.reward_system.RewardSystem.select_random_reward')
    def test_process_loot_box_opening(self, mock_select_reward, mock_determine_tier):
        """Test opening a loot box and receiving a reward"""
        # Create a loot box for testing
        loot_box_type = LootBoxType.query.filter_by(tier=2).first()
        loot_box = LootBox(
            user_id=self.test_user.id,
            type_id=loot_box_type.id,
            awarded_for="test_opening"
        )
        db.session.add(loot_box)
        db.session.commit()
        
        # Mock the tier determination to return tier 3
        mock_determine_tier.return_value = 3
        
        # Mock the reward selection to return a specific reward
        tier_3_reward = RewardType.query.filter_by(tier=3).first()
        mock_select_reward.return_value = tier_3_reward
        
        # Process the loot box opening
        user_reward, error = RewardSystem.process_loot_box_opening(loot_box.id)
        
        # Verify the results
        self.assertIsNone(error)
        self.assertIsNotNone(user_reward)
        self.assertEqual(user_reward.user_id, self.test_user.id)
        self.assertEqual(user_reward.reward_type_id, tier_3_reward.id)
        self.assertEqual(user_reward.loot_box_id, loot_box.id)
        
        # Verify the loot box is now marked as opened
        loot_box = db.session.get(LootBox, loot_box.id)
        self.assertTrue(loot_box.is_opened)
        self.assertIsNotNone(loot_box.opened_at)
    
    def test_process_loot_box_already_opened(self):
        """Test attempting to open an already opened loot box"""
        # Create a pre-opened loot box
        loot_box_type = LootBoxType.query.filter_by(tier=1).first()
        loot_box = LootBox(
            user_id=self.test_user.id,
            type_id=loot_box_type.id,
            awarded_for="test_already_opened",
            is_opened=True,
            opened_at=datetime.now(UTC)
        )
        db.session.add(loot_box)
        db.session.commit()
        
        # Try to open it again
        user_reward, error = RewardSystem.process_loot_box_opening(loot_box.id)
        
        # Verify an error was returned
        self.assertIsNone(user_reward)
        self.assertIsNotNone(error)
        self.assertIn("already opened", error)
    
    def test_equip_reward(self):
        """Test equipping a reward as profile picture"""
        # Create a real test user
        test_user = self.test_user  # Add any required fields if needed
        db.session.add(test_user)
        db.session.commit()

        # Create a reward type
        reward_type = RewardType.query.filter_by(tier=3).first()

        # Create a UserReward
        user_reward = UserReward(
            user_id=test_user.id,
            reward_type_id=reward_type.id
        )
        db.session.add(user_reward)
        db.session.commit()

        # Equip the reward
        result = user_reward.equip()

        # Refresh user from db to get updated profile picture
        db.session.refresh(test_user)

        # Assertions
        self.assertTrue(result)
        self.assertTrue(user_reward.is_equipped)
        self.assertEqual(test_user.profile_picture, reward_type.image_url)



if __name__ == '__main__':
    unittest.main()