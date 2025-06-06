# models/user.py
from datetime import datetime, timedelta, UTC
from . import db
from .user_activity import UserActivity

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    
    # Level and XP tracking
    current_level = db.Column(db.Integer, default=1)
    current_xp = db.Column(db.Integer, default=0)
    total_xp_earned = db.Column(db.Integer, default=0)  # Lifetime total (never resets)
    
    # Profile information
    join_date = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(UTC))
    profile_picture = db.Column(db.String(255), nullable=True)
    
    # Weekly activity tracking
    last_event_date = db.Column(db.DateTime(timezone=True), nullable=True)
    active_weeks_streak = db.Column(db.Integer, default=0)
    
    # Semester tracking
    current_semester = db.Column(db.String(20), nullable=True)
    
    # Relationships
    activities = db.relationship('UserActivity', backref='user', lazy='dynamic')
    participations = db.relationship('Participant', back_populates='user')
    loot_boxes = db.relationship('LootBox', backref='user', lazy='dynamic')
    rewards = db.relationship('UserReward', backref='user', lazy='dynamic')
    
    @property
    def current_tier(self):
        """Get user's current tier based on level (calculated dynamically)"""
        from .level import Level
        level_info = Level.query.filter_by(level_number=self.current_level).first()
        return level_info.tier if level_info else 1
    
    def calculate_activity_bonus(self):
        """Calculate the weekly activity bonus multiplier"""
        if not self.last_event_date:
            return 1.0  # No bonus if this is the first event
        
        # Get current active weeks streak
        if self.active_weeks_streak == 1:
            return 1.1  # 1 week streak = 1.1x
        elif self.active_weeks_streak == 2:
            return 1.2  # 2 week streak = 1.2x
        elif self.active_weeks_streak >= 3:
            return 1.25  # 3+ week streak = 1.25x
        else:
            return 1.0  # No streak = no bonus
    
    def calculate_interaction_bonus(self, event_id):
        """Calculate the new interaction bonus multiplier (1.1x if new interactions)"""
        from .user_interaction import UserInteraction
        from .participant import Participant
        from .semester import Semester
        
        # Get the current semester
        current_semester = Semester.get_current_semester()
        if not current_semester:
            return 1.0  # No bonus if no active semester
        
        # Find all participants in this event
        participants = Participant.query.filter_by(event_id=event_id).all()
        
        # Check if any participants are new interactions
        has_new_interaction = False
        two_weeks_ago = datetime.now(UTC) - timedelta(days=14)
        
        for participant in participants:
            # Skip self
            if participant.user_id == self.id:
                continue
            
            # Check if there's been an interaction this semester
            interaction = UserInteraction.query.filter_by(
                user_id=self.id,
                other_user_id=participant.user_id,
                semester=current_semester.name
            ).first()
            
            # Check if there's been an interaction in the last two weeks
            recent_interaction = UserInteraction.query.filter(
                UserInteraction.user_id == self.id,
                UserInteraction.other_user_id == participant.user_id,
                UserInteraction.interaction_date >= two_weeks_ago
            ).first()
            
            # If no interaction this semester or no recent interaction, this is a "new" interaction
            if not interaction or not recent_interaction:
                has_new_interaction = True
                
                # Record this interaction
                new_interaction = UserInteraction(
                    user_id=self.id,
                    other_user_id=participant.user_id,
                    event_id=event_id,
                    semester=current_semester.name
                )
                db.session.add(new_interaction)
        
        return 1.1 if has_new_interaction else 1.0
    
    def update_activity_streak(self):
        """Update the user's weekly activity streak"""
        now = datetime.now(UTC)
        if not self.last_event_date:
            # First event
            self.active_weeks_streak = 1
        else:
            # Check if last event was in a different week but within the last two weeks
            last_week_start = (now - timedelta(days=now.weekday() + 7)).replace(
                hour=0, minute=0, second=0, microsecond=0)
            two_weeks_ago = (now - timedelta(days=14))
            
            if self.last_event_date < last_week_start and self.last_event_date >= two_weeks_ago:
                # Last event was in the previous week - continue streak
                self.active_weeks_streak += 1
            elif self.last_event_date < two_weeks_ago:
                # Last event was more than two weeks ago - reset streak
                self.active_weeks_streak = 1
            # If in same week, streak doesn't change
        
        # Update last event date
        self.last_event_date = now
    
    def award_xp(self, base_amount, activity_type, event_id=None, description=None):
        """Award XP to user with appropriate bonuses and check for level up"""
        if base_amount <= 0:
            return False
        
        # Calculate bonus multipliers
        activity_bonus = self.calculate_activity_bonus()
        interaction_bonus = 1.0
        if event_id:
            interaction_bonus = self.calculate_interaction_bonus(event_id)
        
        # Calculate total XP with bonuses
        total_multiplier = activity_bonus * interaction_bonus
        xp_awarded = int(base_amount * total_multiplier)
        
        # Update user's XP
        previous_level = self.current_level
        self.current_xp += xp_awarded
        self.total_xp_earned += xp_awarded
        
        # Update activity streak
        self.update_activity_streak()
        
        # Record activity
        bonus_description = f"(Base: {base_amount} XP, Activity: {activity_bonus}x, Interaction: {interaction_bonus}x)"
        full_description = f"{description if description else activity_type} {bonus_description}"
        
        new_activity = UserActivity(
            user_id=self.id,
            activity_type=activity_type,
            xp_earned=xp_awarded,
            related_event_id=event_id,
            description=full_description
        )
        db.session.add(new_activity)
        
        # Check for level up
        self.check_level_up()
        
        # Award loot box if leveled up
        if self.current_level > previous_level:
            self.award_level_up_loot_box(previous_level)
        
        # Maximum level check - if at max level, award loot box for event participation
        if self.current_level == 25 and activity_type in ['event_attendance', 'event_organization']:
            self.award_max_level_loot_box()
        
        db.session.commit()
        return True
    
    def check_level_up(self):
        """Check if user has enough XP to level up"""
        from .level import Level
        
        # Find all levels that the user's XP qualifies for
        eligible_levels = Level.query.filter(
            Level.total_xp <= self.current_xp
        ).order_by(Level.level_number.desc()).all()
        
        if eligible_levels:
            # Get the highest eligible level
            highest_eligible = eligible_levels[0]
            
            # Update user's level if it has increased
            if highest_eligible.level_number > self.current_level:
                self.current_level = highest_eligible.level_number
                return True
        
        return False
    
    def award_level_up_loot_box(self, previous_level):
        """Award a loot box for leveling up"""
        from .reward_system import RewardSystem
        
        # Use the reward system to award the loot box based on level
        RewardSystem.award_loot_box_for_level_up(self.id, self.current_level, "level_up")
    
    def award_max_level_loot_box(self):
        """Award a loot box for event participation at max level"""
        from .loot_box import LootBoxType, LootBox
        
        # Find max tier loot box
        loot_box_type = LootBoxType.query.filter_by(tier=5).first()  # Tier 5 for max level
        if loot_box_type:
            new_loot_box = LootBox(
                user_id=self.id,
                type_id=loot_box_type.id,
                awarded_for="max_level_event_participation"
            )
            db.session.add(new_loot_box)
    
    def get_equipped_reward(self):
        """Get the currently equipped reward (profile image)"""
        from .reward import UserReward
        
        equipped = UserReward.query.filter_by(user_id=self.id, is_equipped=True).first()
        return equipped
    
    def equip_reward(self, reward_id):
        """Equip a reward as the user's profile image"""
        from .reward import UserReward
        
        reward = UserReward.query.filter_by(id=reward_id, user_id=self.id).first()
        if reward:
            return reward.equip()
        return False
    
    def reset_semester_xp(self, semester_name):
        """Reset user's XP for a new semester"""
        self.current_xp = 0
        self.current_level = 1
        self.active_weeks_streak = 0
        self.current_semester = semester_name
        # Don't reset total_xp_earned
        db.session.commit()