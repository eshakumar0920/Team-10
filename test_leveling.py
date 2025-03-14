# test_leveling.py
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
        existing_participant = Participant.query.filter_by(user_id=user.id, event_id=event.id).first()
        if existing_participant:
            db.session.delete(existing_participant)
            db.session.commit()
           
        # Also remove any activity records related to this user and event
        # to ensure accurate activity tracking during the test
        existing_activities = UserActivity.query.filter_by(
            user_id=user.id,
            related_event_id=event.id
        ).all()
        for activity in existing_activities:
            db.session.delete(activity)
        db.session.commit()
       
        # Create a new participant record to associate the user with the event
        # This simulates a user registering for an event
        participant = Participant(event_id=event.id, user_id=user.id)
        db.session.add(participant)
        db.session.commit()
       
        # Log the initial state of the user for comparison
        print(f"Initial state: User {user.username} is at level {user.current_level} with {user.current_xp} XP")
       
        # Simulate the user attending the event and being awarded XP
        # This calls the mark_attended method which should award attendance XP
        participant.mark_attended()
       
        # Refresh the user object to get updated XP and level values from the database
        db.session.refresh(user)
        print(f"After attendance: User {user.username} is at level {user.current_level} with {user.current_xp} XP")
       
        # Simulate awarding XP to the event creator/organizer
        # This tests the organizer reward system
        event.award_creator_xp()
       
        # Refresh user data again to see any additional changes
        db.session.refresh(user)
       
        # Display all user activities to verify proper activity tracking
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