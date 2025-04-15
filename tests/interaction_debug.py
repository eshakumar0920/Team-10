"""
Debugging script to understand how user interactions are being tracked
"""

import os
import sys
from datetime import datetime
from flask import Flask

# Add parent directory to path so we can import application modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import config_by_name
from models import db, User, Event, Participant, UserInteraction, Semester

# Create a Flask app
app = Flask(__name__)
app.config.from_object(config_by_name['test'])
db.init_app(app)

def debug_interactions():
    with app.app_context():
        # Clean up previous test data
        db.drop_all()
        db.create_all()
        
        print("=== DEBUGGING USER INTERACTIONS ===")
        
        # Create a test semester
        semester = Semester(
            name="Test Semester",
            start_date=datetime.now(),
            end_date=datetime.now(),
            is_active=True
        )
        db.session.add(semester)
        db.session.commit()
        
        # Create test users
        user1 = User(username="debug_user1", email="debug1@test.com", password_hash="test")
        user2 = User(username="debug_user2", email="debug2@test.com", password_hash="test")
        user3 = User(username="debug_user3", email="debug3@test.com", password_hash="test")
        
        db.session.add_all([user1, user2, user3])
        db.session.commit()
        
        print(f"Created users: {user1.id}, {user2.id}, {user3.id}")
        
        # Create a test event
        event = Event(
            title="Debug Event",
            description="Testing interactions",
            location="Test Location",
            event_date=datetime.now().isoformat(),
            creator_id=user1.id
        )
        db.session.add(event)
        db.session.commit()
        
        print(f"Created event: {event.id}")
        
        # Create participants
        p1 = Participant(event_id=event.id, user_id=user1.id)
        db.session.add(p1)
        db.session.commit()
        p1.mark_attended()
        
        print("User 1 joined and was marked as attended")
        
        # Check for interactions after user 1 joins
        interactions = UserInteraction.query.all()
        print(f"Number of interactions after user 1 joins: {len(interactions)}")
        for i in interactions:
            print(f"  Interaction: user_id={i.user_id}, other_user_id={i.other_user_id}, event_id={i.event_id}")
        
        # Add user 2 to the event
        p2 = Participant(event_id=event.id, user_id=user2.id)
        db.session.add(p2)
        db.session.commit()
        p2.mark_attended()
        
        print("User 2 joined and was marked as attended")
        
        # Check for interactions after user 2 joins
        interactions = UserInteraction.query.all()
        print(f"Number of interactions after user 2 joins: {len(interactions)}")
        for i in interactions:
            print(f"  Interaction: user_id={i.user_id}, other_user_id={i.other_user_id}, event_id={i.event_id}")
        
        # Check if a bonus was applied for user 2
        activities = user2.activities.all()
        for a in activities:
            print(f"User 2 activity: {a.activity_type}, XP: {a.xp_earned}, Description: {a.description}")
        
        # Add user 3 to the event
        p3 = Participant(event_id=event.id, user_id=user3.id)
        db.session.add(p3)
        db.session.commit()
        p3.mark_attended()
        
        print("User 3 joined and was marked as attended")
        
        # Check for interactions after user 3 joins
        interactions = UserInteraction.query.all()
        print(f"Number of interactions after user 3 joins: {len(interactions)}")
        for i in interactions:
            print(f"  Interaction: user_id={i.user_id}, other_user_id={i.other_user_id}, event_id={i.event_id}")
        
        # Check if a bonus was applied for user 3
        activities = user3.activities.all()
        for a in activities:
            print(f"User 3 activity: {a.activity_type}, XP: {a.xp_earned}, Description: {a.description}")
        
        print("=== DEBUGGING COMPLETE ===")

if __name__ == "__main__":
    debug_interactions()