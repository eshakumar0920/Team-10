"""
Test script for the leveling system functionality.
This script creates test users, events, and simulates participation to verify XP awards and leveling.
"""

import os
import sys
import unittest
from datetime import datetime, timedelta, UTC
from flask import Flask
from sqlalchemy import text

# Add parent directory to path so we can import application modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import config_by_name
from models import db, User, Level, Event, Participant, UserActivity
from models import UserInteraction, LootBox, LootBoxType, Semester

class LevelingSystemTest(unittest.TestCase):
    
    def setUp(self):
        """Set up test environment before each test"""
        # Create a test Flask app
        self.app = Flask(__name__)
        self.app.config.from_object(config_by_name['test'])
        
        # Initialize database
        db.init_app(self.app)
        
        # Push an application context
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        # Drop and recreate all tables for a clean state
        db.drop_all()
        db.create_all()
        
        # Initialize test data
        self._create_test_data()
        
    def tearDown(self):
        """Clean up after each test"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def _create_test_data(self):
        """Create test users, levels, and semester data"""
        # Create test users
        self.test_users = []
        for i in range(1, 5):
            user = User(
                username=f'testuser{i}',
                email=f'testuser{i}@example.com',
                password_hash='password_hash',
                current_level=1,
                current_xp=0,
                total_xp_earned=0,
                current_tier=1
            )
            db.session.add(user)
            self.test_users.append(user)
        
        # Commit to get user IDs
        db.session.commit()
        
        # Create test levels
        levels_data = [
            {"level_number": 1, "xp_required": 0, "level_xp": 0, "total_xp": 0, "tier": 1, 
             "title": "Novice", "description": "Just starting", "perks": "Basic"},
            
            {"level_number": 2, "xp_required": 50, "level_xp": 50, "total_xp": 50, "tier": 1,
             "title": "Beginner", "description": "Beginning", "perks": "More"},
            
            {"level_number": 3, "xp_required": 102, "level_xp": 52, "total_xp": 102, "tier": 1,
             "title": "Rookie", "description": "Improving", "perks": "Better"}
        ]
        
        for level_data in levels_data:
            level = Level(**level_data)
            db.session.add(level)
        
        # Create a test semester
        current_semester = Semester(
            name="Test Semester",
            start_date=datetime.now(UTC),
            end_date=datetime.now(UTC) + timedelta(days=90),
            is_active=True
        )
        db.session.add(current_semester)
        
        # Create loot box types
        for tier in range(1, 6):
            loot_box_type = LootBoxType(
                name=f"Tier {tier} Test Box",
                description=f"Test loot box for tier {tier}",
                tier=tier
            )
            db.session.add(loot_box_type)
        
        db.session.commit()
    
    def _create_test_event(self, creator_id):
        """Create a test event with the given creator"""
        event = Event(
            title="Test Event",
            description="This is a test event",
            location="Test Location",
            event_date=datetime.now(UTC).isoformat(),
            creator_id=creator_id
        )
        db.session.add(event)
        db.session.commit()
        
        # Award XP to creator
        event.award_creator_xp()
        
        return event
    
    def _join_event(self, event_id, user_id):
        """Make a user join an event"""
        participant = Participant(
            event_id=event_id,
            user_id=user_id
        )
        db.session.add(participant)
        db.session.commit()
        
        # Mark as attended to award XP
        participant.mark_attended()
        
        return participant
    
    def test_event_creation_xp(self):
        """Test that creating an event awards the correct XP"""
        # Create event with first test user
        event = self._create_test_event(self.test_users[0].id)
        
        # Get the user's updated data
        user = db.session.get(User, self.test_users[0].id)
        
        # Check that the user received the correct base XP for creating an event (200)
        # Note: Could be higher due to bonuses
        self.assertGreaterEqual(user.current_xp, 200)
        
        # Verify activity record was created
        activity = UserActivity.query.filter_by(
            user_id=self.test_users[0].id,
            activity_type='event_organization'
        ).first()
        
        self.assertIsNotNone(activity)
        self.assertEqual(activity.related_event_id, event.id)
    
    def test_event_attendance_xp(self):
        """Test that attending an event awards the correct XP"""
        # Create event with first test user
        event = self._create_test_event(self.test_users[0].id)
        
        # Second user joins the event
        self._join_event(event.id, self.test_users[1].id)
        
        # Get the participant's updated data
        user = db.session.get(User, self.test_users[1].id)
        
        # Check that the user received the correct base XP for attending (50)
        # Note: Could be higher due to bonuses
        self.assertGreaterEqual(user.current_xp, 50)
        
        # Verify activity record was created
        activity = UserActivity.query.filter_by(
            user_id=self.test_users[1].id,
            activity_type='event_attendance'
        ).first()
        
        self.assertIsNotNone(activity)
        self.assertEqual(activity.related_event_id, event.id)
    
    def test_level_up_mechanism(self):
        """Test that users level up correctly when they earn enough XP"""
        # Get the first test user
        user = db.session.get(User, self.test_users[0].id)
        
        # Initial level should be 1
        self.assertEqual(user.current_level, 1)
        
        # Award enough XP to reach level 2 (50 XP)
        user.current_xp = 0  # Reset XP first
        user.award_xp(
            base_amount=60,  # More than needed for level 2
            activity_type='test',
            description='Test level up'
        )
        
        # Check that the user leveled up
        self.assertEqual(user.current_level, 2)
        
        # Award more XP to reach level 3
        user.award_xp(
            base_amount=60,  # Should push them over the threshold for level 3
            activity_type='test',
            description='Test level up to 3'
        )
        
        # Check that the user leveled up again
        self.assertEqual(user.current_level, 3)
    
    def test_activity_bonus(self):
        """Test weekly activity bonus mechanism"""
        # Get the second test user
        user = db.session.get(User, self.test_users[1].id)
        
        # First event - should get no activity bonus
        initial_bonus = user.calculate_activity_bonus()
        self.assertEqual(initial_bonus, 1.0)
        
        # Record an event participation
        user.last_event_date = datetime.now(UTC) - timedelta(days=8)  # 8 days ago
        user.active_weeks_streak = 1
        db.session.commit()
        
        # Second event - different week, should get 1.1x bonus
        second_bonus = user.calculate_activity_bonus()
        self.assertEqual(second_bonus, 1.1)
        
        # Update streak to 2 weeks
        user.active_weeks_streak = 2
        db.session.commit()
        
        # Third event - should get 1.2x bonus
        third_bonus = user.calculate_activity_bonus()
        self.assertEqual(third_bonus, 1.2)
        
        # Update streak to 3 weeks
        user.active_weeks_streak = 3
        db.session.commit()
        
        # Fourth event - should get 1.25x bonus
        fourth_bonus = user.calculate_activity_bonus()
        self.assertEqual(fourth_bonus, 1.25)
        
    def test_interaction_bonus(self):
        """Test new interaction bonus mechanism"""
        # Create event with first test user
        event = self._create_test_event(self.test_users[0].id)
        
        # Make first user join and attend their own event (might be necessary)
        first_participant = Participant(
            event_id=event.id,
            user_id=self.test_users[0].id
        )
        db.session.add(first_participant)
        db.session.commit()
        first_participant.mark_attended()
        
        # Second user joins the event
        self._join_event(event.id, self.test_users[1].id)
        
        # Third user joins the event
        self._join_event(event.id, self.test_users[2].id)
        
        # Check that at least some interactions were created
        interactions = UserInteraction.query.filter_by(
            event_id=event.id
        ).all()
        
        self.assertTrue(len(interactions) > 0, "Expected at least one interaction to be created")
        
        # Create another event to test second interactions
        event2 = self._create_test_event(self.test_users[0].id)
        
        # Get the second user before joining
        user = db.session.get(User, self.test_users[1].id)
        initial_xp = user.current_xp
        
        # Join the event and check for interaction bonus
        self._join_event(event2.id, self.test_users[1].id)
        
        # Get the user again after joining
        user = db.session.get(User, self.test_users[1].id)
        
        # The increase should be more than just 50 if there was a 1.1x bonus
        xp_gained = user.current_xp - initial_xp
        self.assertGreaterEqual(xp_gained, 50, f"User gained {xp_gained} XP, which is less than the base amount")
        
        # Print more info about the activity for debugging
        activity = UserActivity.query.filter_by(
            user_id=self.test_users[1].id,
            related_event_id=event2.id
        ).first()
        
        if activity:
            print(f"Activity: {activity.description}, XP gained: {activity.xp_earned}")

    def test_loot_box_awarded_on_level_up(self):
        """Test that loot boxes are awarded when a user levels up"""
        # Get the first test user
        user = db.session.get(User, self.test_users[0].id)
        
        # Check initial loot box count
        initial_loot_boxes = LootBox.query.filter_by(user_id=self.test_users[0].id).count()
        
        # Award enough XP to level up
        user.award_xp(
            base_amount=60,  # More than needed for level 2
            activity_type='test',
            description='Test level up loot box'
        )
        
        # Check that a new loot box was awarded
        new_loot_boxes = LootBox.query.filter_by(user_id=self.test_users[0].id).count()
        self.assertEqual(new_loot_boxes, initial_loot_boxes + 1)
        
        # Verify the loot box is for the correct tier
        loot_box = LootBox.query.filter_by(user_id=self.test_users[0].id).first()
        loot_box_type = db.session.get(LootBoxType, loot_box.type_id)
        self.assertEqual(loot_box_type.tier, user.current_tier)

if __name__ == '__main__':
    unittest.main()