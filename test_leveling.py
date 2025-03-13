# test_leveling.py
<<<<<<< HEAD
"""
XP and Leveling System Integration Test

Purpose:
This file contains a test script to verify the correct functionality of the application's
experience (XP) system and user level progression. It focuses on testing two main features:
1. Marking attendance at events and awarding XP for participation
2. Awarding XP to event organizers/creators

The test simulates a complete flow of a user attending an event and an organizer being
credited for creating an event, then verifies that XP is correctly awarded and levels
are properly updated in the database.

Created by: PG (Initial basic functionality test)
"""

# Import necessary modules and components
from app import create_app  # Import the application factory function
from models import db, User, Event, Participant, UserActivity  # Import database models

# Create a test application instance with development configuration
=======
# The intial basic functionality test created to test attendance marking and xp awarding. -PG
from app import create_app
from models import db, User, Event, Participant, UserActivity
>>>>>>> c2a661cd (Update test_leveling and create test_xp_system)
app = create_app('dev')

def test_xp_system():
    """
    Test the XP and leveling system functionality by simulating event attendance
    and tracking the resulting XP awards and level changes.
    """
    with app.app_context():
        # Retrieve test user and event from the database
        user = User.query.filter_by(username="testuser1").first()
        event = Event.query.filter_by(title="Test Event 2").first()
<<<<<<< HEAD
       
        # Verify test data exists before proceeding
        if not user or not event:
            print("Test data not found. Run test_data.py first.")
            return
       
        # Reset the user's state to ensure consistent test conditions
        # Set XP to 0 and level to 1 (starting values)
        user.current_xp = 0
        user.current_level = 1
        db.session.commit()
       
        # Clean up any existing participant records for this user and event
        # This ensures the test starts with a clean slate
=======
        
        if not user or not event:
            print("Test data not found. Run test_data.py first.")
            return
        
        # Reset the user's XP to 0 for testing
        user.current_xp = 0
        user.current_level = 1
        db.session.commit()
        
        # Delete any existing participant record to start fresh
>>>>>>> 84abf27f (Debug test_leveling)
        existing_participant = Participant.query.filter_by(user_id=user.id, event_id=event.id).first()
        if existing_participant:
            db.session.delete(existing_participant)
            db.session.commit()
<<<<<<< HEAD
           
        # Also remove any activity records related to this user and event
        # to ensure accurate activity tracking during the test
        existing_activities = UserActivity.query.filter_by(
            user_id=user.id,
=======
            
        # Delete any existing activity records for this user/event
        existing_activities = UserActivity.query.filter_by(
            user_id=user.id, 
>>>>>>> 84abf27f (Debug test_leveling)
            related_event_id=event.id
        ).all()
        for activity in existing_activities:
            db.session.delete(activity)
        db.session.commit()
<<<<<<< HEAD
       
        # Create a new participant record to associate the user with the event
        # This simulates a user registering for an event
        participant = Participant(event_id=event.id, user_id=user.id)
        db.session.add(participant)
        db.session.commit()
       
        # Log the initial state of the user for comparison
=======
        
        # Create a new participant record
        participant = Participant(event_id=event.id, user_id=user.id)
        db.session.add(participant)
        db.session.commit()
        
        # Check initial XP and level
>>>>>>> 84abf27f (Debug test_leveling)
        print(f"Initial state: User {user.username} is at level {user.current_level} with {user.current_xp} XP")
       
        # Simulate the user attending the event and being awarded XP
        # This calls the mark_attended method which should award attendance XP
        participant.mark_attended()
<<<<<<< HEAD
       
        # Refresh the user object to get updated XP and level values from the database
=======
        
        # Refresh user from database to get updated values
>>>>>>> 84abf27f (Debug test_leveling)
        db.session.refresh(user)
        print(f"After attendance: User {user.username} is at level {user.current_level} with {user.current_xp} XP")
       
        # Simulate awarding XP to the event creator/organizer
        # This tests the organizer reward system
        event.award_creator_xp()
<<<<<<< HEAD
       
        # Refresh user data again to see any additional changes
        db.session.refresh(user)
       
        # Display all user activities to verify proper activity tracking
=======
        
        # Refresh user again
        db.session.refresh(user)
        
        # Check user activities
>>>>>>> 84abf27f (Debug test_leveling)
        activities = UserActivity.query.filter_by(user_id=user.id).all()
        print(f"\nUser activities for {user.username}:")
        for activity in activities:
            print(f"- {activity.activity_type}: {activity.xp_earned} XP, {activity.description}")
       
        # Check and report if the user leveled up during the test
        if user.current_level > 1:
            print(f"\nUser has leveled up to level {user.current_level}!")
        else:
            print("\nUser has not leveled up yet.")

# Execute the test when the script is run directly
if __name__ == "__main__":
    test_xp_system()