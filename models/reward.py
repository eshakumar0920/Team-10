# models/reward.py
from . import db
from datetime import datetime, UTC

from .user import User

class RewardType(db.Model):
    """Defines different types of rewards (profile images)"""
    __tablename__ = 'reward_types'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(255), nullable=False)
    tier = db.Column(db.Integer, default=1)  # Tier of the reward (1-4)
    category = db.Column(db.String(50))  # "Season", "Event", or "Unique"
    theme = db.Column(db.String(50))  # e.g., "Fall", "Sport", "Coding", etc.
    is_rare = db.Column(db.Boolean, default=False)  # For max level unique items
    
    # Relationship with user rewards
    user_rewards = db.relationship('UserReward', backref='reward_type', lazy='dynamic')
    
    def __repr__(self):
        return f'<RewardType {self.name} (Tier {self.tier})>'


class UserReward(db.Model):
    """Tracks rewards in users' inventories"""
    __tablename__ = 'user_rewards'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    reward_type_id = db.Column(db.Integer, db.ForeignKey('reward_types.id'), nullable=False)
    acquired_at = db.Column(db.DateTime(timezone=True), default=lambda:datetime.now(UTC))
    is_equipped = db.Column(db.Boolean, default=False)  # Is this the user's active profile image
    loot_box_id = db.Column(db.Integer, db.ForeignKey('loot_boxes.id'), nullable=True)  # Which loot box it came from
    
    def __repr__(self):
        status = "Equipped" if self.is_equipped else "Not Equipped"
        return f'<UserReward {status} for user_id={self.user_id}>'
    
    def equip(self):
        """Sets this reward as the user's active profile image"""
        # First, unequip any currently equipped rewards for this user
        UserReward.query.filter_by(user_id=self.user_id, is_equipped=True).update({'is_equipped': False})
        
        # Then equip this one
        self.is_equipped = True
        
        # Update the user's profile picture
        user = db.session.get(User, self.user_id)
        reward = db.session.get(RewardType, self.reward_type_id)
        if user and reward:
            user.profile_picture = reward.image_url
        
        db.session.commit()
        return True