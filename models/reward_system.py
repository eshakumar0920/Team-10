# models/reward_system.py
import random
from . import db
from .loot_box import LootBox, LootBoxType
from .reward import RewardType, UserReward
from .drop_rate import LootBoxDropRate, RewardDropRate
from sqlalchemy import and_

class RewardSystem:
    @staticmethod
    def determine_loot_box_tier(user_level):
        """Determine which tier of loot box to award based on user level and drop rates"""
        # Find the drop rate record for this level range
        drop_rate = LootBoxDropRate.query.filter(
            and_(
                LootBoxDropRate.level_min <= user_level,
                LootBoxDropRate.level_max >= user_level
            )
        ).first()
        
        if not drop_rate:
            # Default to lowest tier if no drop rate found
            return 1
        
        # Roll a random number between 0 and 100
        roll = random.uniform(0, 100)
        
        # Determine the tier based on the roll and drop rates
        cumulative = 0
        
        # Check Tier 1
        cumulative += drop_rate.tier_1_rate
        if roll <= cumulative:
            return 1
        
        # Check Tier 2
        cumulative += drop_rate.tier_2_rate
        if roll <= cumulative:
            return 2
        
        # Check Tier 3
        cumulative += drop_rate.tier_3_rate
        if roll <= cumulative:
            return 3
        
        # If we made it here, it's Tier 4
        return 4
    
    @staticmethod
    def determine_reward_tier(loot_box_tier):
        """Determine which tier of reward to give based on loot box tier and drop rates"""
        # Find the drop rate record for this loot box tier
        drop_rate = RewardDropRate.query.filter_by(loot_box_tier=loot_box_tier).first()
        
        if not drop_rate:
            # Default to loot box tier if no drop rate found
            return loot_box_tier
        
        # Roll a random number between 0 and 100
        roll = random.uniform(0, 100)
        
        # Determine the tier based on the roll and drop rates
        cumulative = 0
        
        # Check Tier 1
        cumulative += drop_rate.tier_1_rate
        if roll <= cumulative:
            return 1
        
        # Check Tier 2
        cumulative += drop_rate.tier_2_rate
        if roll <= cumulative:
            return 2
        
        # Check Tier 3
        cumulative += drop_rate.tier_3_rate
        if roll <= cumulative:
            return 3
        
        # If we made it here, it's Tier 4
        return 4
    
    @staticmethod
    def select_random_reward(tier, user_id, is_max_level=False):
        """Select a random reward of the given tier for the user"""
        query = RewardType.query.filter_by(tier=tier)
        
        # If user is max level and we want rare items, filter for those
        if is_max_level and tier == 4:
            # Chance to get a rare item
            if random.random() < 0.25:  # 25% chance for rare item
                query = query.filter_by(is_rare=True)
        
        # Get all eligible rewards
        eligible_rewards = query.all()
        
        if not eligible_rewards:
            # Fall back to tier 1 if no rewards found
            eligible_rewards = RewardType.query.filter_by(tier=1).all()
        
        if not eligible_rewards:
            # If still no rewards, something's wrong
            return None
        
        # Select a random reward from the eligible ones
        selected_reward = random.choice(eligible_rewards)
        
        # Check if user already has this reward
        existing = UserReward.query.filter_by(
            user_id=user_id, 
            reward_type_id=selected_reward.id
        ).first()
        
        if existing:
            # If so, we could give them a duplicate or try again
            # For now, let's allow duplicates
            pass
        
        return selected_reward
    
    @staticmethod
    def award_loot_box_for_level_up(user_id, new_level, reason="level_up"):
        """Award a loot box based on user's level"""
        from .user import User
        
        user = User.query.get(user_id)
        if not user:
            return None
        
        # Determine loot box tier based on user level
        box_tier = RewardSystem.determine_loot_box_tier(new_level)
        
        # Find appropriate loot box type
        loot_box_type = LootBoxType.query.filter_by(tier=box_tier).first()
        if not loot_box_type:
            # Fall back to tier 1 if no matching type
            loot_box_type = LootBoxType.query.filter_by(tier=1).first()
        
        if not loot_box_type:
            return None
        
        # Create the loot box
        new_loot_box = LootBox(
            user_id=user_id,
            type_id=loot_box_type.id,
            awarded_for=f"{reason}_level_{new_level}"
        )
        
        db.session.add(new_loot_box)
        db.session.commit()
        
        return new_loot_box
    
    @staticmethod
    def process_loot_box_opening(loot_box_id):
        """Process the opening of a loot box and award a reward"""
        # Get the loot box
        loot_box = LootBox.query.get(loot_box_id)
        if not loot_box or loot_box.is_opened:
            return None, "Loot box not found or already opened"
        
        # Get the loot box type
        loot_box_type = LootBoxType.query.get(loot_box.type_id)
        if not loot_box_type:
            return None, "Loot box type not found"
        
        # Get the user
        from .user import User
        user = User.query.get(loot_box.user_id)
        if not user:
            return None, "User not found"
        
        # Determine reward tier
        reward_tier = RewardSystem.determine_reward_tier(loot_box_type.tier)
        
        # Select random reward
        is_max_level = user.current_level >= 25
        reward = RewardSystem.select_random_reward(reward_tier, user.id, is_max_level)
        
        if not reward:
            return None, "No rewards available"
        
        # Add the reward to the user's inventory
        user_reward = UserReward(
            user_id=user.id,
            reward_type_id=reward.id,
            loot_box_id=loot_box.id
        )
        
        # Mark the loot box as opened
        loot_box.is_opened = True
        loot_box.opened_at = db.func.now()
        
        db.session.add(user_reward)
        db.session.commit()
        
        return user_reward, None  # Return the reward and no error