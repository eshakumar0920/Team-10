# models/reward_system.py
import random
from . import db
from .loot_box import LootBox, LootBoxType
from .reward import RewardType, UserReward
from .drop_rate import LootBoxLevelRange, LootBoxTierRate, RewardBoxTier, RewardTierRate
from sqlalchemy import and_

class RewardSystem:
    @staticmethod
    def determine_loot_box_tier(user_level):
        """Determine which tier of loot box to award based on user level and drop rates"""
        # Find the level range record for this level
        level_range = LootBoxLevelRange.query.filter(
            and_(
                LootBoxLevelRange.level_min <= user_level,
                LootBoxLevelRange.level_max >= user_level
            )
        ).first()
        
        if not level_range:
            # Default to lowest tier if no level range found
            return 1
        
        # Get all tier rates for this level range
        tier_rates = LootBoxTierRate.query.filter_by(
            level_range_id=level_range.id
        ).order_by(LootBoxTierRate.tier).all()
        
        if not tier_rates:
            # Default to lowest tier if no tier rates found
            return 1
        
        # Roll a random floating point number between 0 and 100
        roll = random.uniform(0, 100)
        
        # Cumulative probability approach to determine tier
        cumulative = 0
        
        for tier_rate in tier_rates:
            cumulative += tier_rate.rate
            if roll <= cumulative:
                return tier_rate.tier
        
        # If no tier is selected (due to rounding errors or rates not summing to 100),
        # return the highest tier
        return tier_rates[-1].tier if tier_rates else 1
    
    @staticmethod
    def determine_reward_tier(loot_box_tier):
        """Determine which tier of reward to give based on loot box tier and drop rates"""
        # Find the box tier record for this loot box tier
        box_tier = RewardBoxTier.query.filter_by(
            loot_box_tier=loot_box_tier
        ).first()
        
        if not box_tier:
            # Default to loot box tier if no box tier found
            return loot_box_tier
        
        # Get all tier rates for this box tier
        tier_rates = RewardTierRate.query.filter_by(
            box_tier_id=box_tier.id
        ).order_by(RewardTierRate.tier).all()
        
        if not tier_rates:
            # Default to box tier if no tier rates found
            return loot_box_tier
        
        # Roll a random number between 0 and 100
        roll = random.uniform(0, 100)
        
        # Determine the tier based on the roll and drop rates
        cumulative = 0
        
        for tier_rate in tier_rates:
            cumulative += tier_rate.rate
            if roll <= cumulative:
                return tier_rate.tier
        
        # If no tier is selected, return the highest tier
        return tier_rates[-1].tier if tier_rates else loot_box_tier
    
    @staticmethod
    def select_random_reward(tier, user_id, is_max_level=False):
        """Select a random reward of the given tier for the user"""
        query = RewardType.query.filter_by(tier=tier)
        
        # Max level users have unique chance at rare items
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
        
        # Duplicates may be handled differently in future
        if existing:
            # For now, let's allow duplicates
            pass
        
        return selected_reward
    
    @staticmethod
    def award_loot_box_for_level_up(user_id, new_level, reason="level_up"):
        """Award a loot box based on user's level"""
        from .user import User
        
        user = db.session.get(User, user_id)
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
        loot_box = db.session.get(LootBox, loot_box_id)
        if not loot_box or loot_box.is_opened:
            return None, "Loot box not found or already opened"
        
        # Get the loot box type
        loot_box_type = db.session.get(LootBoxType, loot_box.type_id)
        if not loot_box_type:
            return None, "Loot box type not found"
        
        # Get the user
        from .user import User
        user = db.session.get(User, loot_box.user_id)
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