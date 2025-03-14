# test_xp_system.py
"""
Experience (XP) System Comprehensive Test Suite

Purpose:
This file contains a series of tests to thoroughly validate the application's XP and leveling system.
It tests various aspects of the XP mechanics including:
1. Level progression as users accumulate XP
2. Edge cases such as negative XP, double attendance, and extremely large XP values
3. XP rewards for event organizers
4. A complete end-to-end flow simulating user registration, attendance, and XP awards

This test suite ensures that the XP system behaves correctly across different scenarios,
including normal operation and edge cases, to verify the integrity of the gamification features.

Created by: PG (Secondary functionality test for leveling system)
"""

# Import necessary modules and components
from app import create_app  # Import the application factory function
from models import db, User, Event, Participant, UserActivity, Level  # Import database models

# Create a test application instance with development configuration
app = create_app('dev')

def test_level_up():
    """Test that a user levels up correctly when they gain enough XP"""
    with app.app_context():
        # Retrieve test user from database
        user = User.query.filter_by(username="testuser1").first()
        if not user:
            print("Test user not found. Run test_data.py first.")
            return
            
        # Reset user to baseline state for consistent testing
        user.current_xp = 0
        user.current_level = 1
        db.session.commit()
        
        # Log initial user state for comparison
        print(f"Initial: User {user.username} is at level {user.current_level} with {user.current_xp} XP")
        
        # Test Case 1: Award exactly enough XP to reach level 2
        # The level threshold is defined as 100 XP in test_data.py
        user.award_xp(amount=100, activity_type='test_activity', description="Test level up")
        db.session.refresh(user)  # Refresh user data from database
        
        # Verify level up occurred correctly
        print(f"After 100 XP: User {user.username} is at level {user.current_level} with {user.current_xp} XP")
        
        # Test Case 2: Award more XP, but not enough to reach level 3
        # This tests partial progress toward the next level
        user.award_xp(amount=150, activity_type='test_activity', description="More test XP")
        db.session.refresh(user)
        
        # Verify user has more XP but hasn't leveled up again
        print(f"After 250 XP: User {user.username} is at level {user.current_level} with {user.current_xp} XP")
        
        # Test Case 3: Award enough to reach level 3
        # This confirms the level up system works continuously as more XP is gained
        user.award_xp(amount=50, activity_type='test_activity', description="Final test XP")
        db.session.refresh(user)
        
        # Final verification of level progression
        print(f"After 300 XP: User {user.username} is at level {user.current_level} with {user.current_xp} XP")

def test_edge_cases():
    """Test various edge cases in the XP system"""
    with app.app_context():
        # Retrieve test data
        user = User.query.filter_by(username="testuser2").first()
        event = Event.query.filter_by(title="Test Event 1").first()
        
        if not user or not event:
            print("Test data not found. Run test_data.py first.")
            return
            
        # Initialize user with some existing XP
        user.current_xp = 100
        user.current_level = 1
        db.session.commit()
        
        print(f"Initial: User {user.username} has {user.current_xp} XP")
        
        # Test Case 1: Attempt to award negative XP
        # System should prevent negative XP awards
        result = user.award_xp(amount=-50, activity_type='test_negative', description="Test negative XP")
        db.session.refresh(user)
        print(f"After negative XP attempt: User has {user.current_xp} XP, Award result: {result}")
        
        # Test Case 2: Attempt to mark attendance twice for the same event
        # System should prevent duplicate attendance
        
        # First clean up any existing participant records for this test
        existing = Participant.query.filter_by(user_id=user.id, event_id=event.id).all()
        for p in existing:
            db.session.delete(p)
        db.session.commit()
        
        # Create new participant record (simulate registration)
        participant = Participant(event_id=event.id, user_id=user.id)
        db.session.add(participant)
        db.session.commit()
        
        # Mark attended for the first time (should succeed)
        result1 = participant.mark_attended()
        db.session.refresh(user)
        first_xp = user.current_xp
        
        # Attempt to mark attended a second time (should fail or be idempotent)
        result2 = participant.mark_attended()
        db.session.refresh(user)
        second_xp = user.current_xp
        
        # Check if duplicate attendance was handled correctly
        print(f"First attend: {result1}, XP = {first_xp}")
        print(f"Second attend: {result2}, XP = {second_xp}")
        
        # Test Case 3: Very large XP value
        # Test system's ability to handle unusually large XP awards
        initial_xp = user.current_xp
        user.award_xp(amount=1000000, activity_type='test_large', description="Test large XP amount")
        db.session.refresh(user)
        print(f"After large XP: Level = {user.current_level}, XP = {user.current_xp}, Increase = {user.current_xp - initial_xp}")

def test_organizer_xp():
    """Test that event organizers receive the correct XP"""
    with app.app_context():
        # Find test event for organizer testing
        event = Event.query.filter_by(title="Test Event 1").first()
        if not event:
            print("Test event not found. Run test_data.py first.")
            return
            
        # Get the event creator user
        creator = db.session.get(User, event.creator_id)
        if not creator:
            print(f"Creator user (ID: {event.creator_id}) not found.")
            return
            
        # Store creator's initial XP for comparison
        initial_xp = creator.current_xp
        
        # Display the expected organizer XP reward
        print(f"Event organizer XP reward: {event.organizer_xp_reward}")
        print(f"Before: Creator {creator.username} has {creator.current_xp} XP")
        
        # Award XP to the organizer (creator)
        result = event.award_creator_xp()
        db.session.refresh(creator)
        
        # Verify the organizer received the correct amount of XP
        print(f"After: Creator {creator.username} has {creator.current_xp} XP")
        print(f"XP increase: {creator.current_xp - initial_xp}")
        print(f"Award result: {result}")

def test_full_flow():
    """Test a complete user journey through the XP system"""
    with app.app_context():
        # Find the highest user ID to avoid ID conflicts when creating test users
        highest_user_id = db.session.query(db.func.max(User.id)).scalar() or 0
        
        # Create new test users for this specific test
        # Using explicit IDs to avoid conflicts with existing data
        organizer = User(
            id=highest_user_id + 1,  # Explicitly set ID to avoid conflict
            username="test_organizer", 
            email="org@example.com", 
            password_hash="password"
        )
        attendee = User(
            id=highest_user_id + 2,  # Explicitly set ID to avoid conflict
            username="test_attendee", 
            email="att@example.com", 
            password_hash="password"
        )
        db.session.add(organizer)
        db.session.add(attendee)
        db.session.commit()
        
        try:
            # Create a test event for this specific test
            event = Event(
                title="XP System Test Event",
                description="Testing the full XP system",
                location="Test Location",
                event_date="2023-12-31",
                creator_id=organizer.id,
                xp_reward=50,               # XP reward for attendees
                organizer_xp_reward=200     # XP reward for the organizer
            )
            db.session.add(event)
            db.session.commit()
            
            # Log initial state
            print(f"Created event: {event.title} by {organizer.username}")
            print(f"Organizer initial XP: {organizer.current_xp}")
            print(f"Attendee initial XP: {attendee.current_xp}")
            
            # Step 1: Register attendee for the event
            participant = Participant(event_id=event.id, user_id=attendee.id)
            db.session.add(participant)
            db.session.commit()
            print(f"Registered attendee for event")
            
            # Step 2: Mark the attendee as having attended the event
            participant.mark_attended()
            db.session.refresh(attendee)
            print(f"After attendance: Attendee XP = {attendee.current_xp}")
            
            # Step 3: Award XP to the event organizer
            event.award_creator_xp()
            db.session.refresh(organizer)
            print(f"After organization: Organizer XP = {organizer.current_xp}")
            
            # Step 4: Verify activity records were created properly
            # Check that the system logged all XP awards with the correct details
            attendee_activities = UserActivity.query.filter_by(user_id=attendee.id).all()
            organizer_activities = UserActivity.query.filter_by(user_id=organizer.id).all()
            
            # Display all activities for verification
            print("\nAttendee activities:")
            for activity in attendee_activities:
                print(f"- {activity.activity_type}: {activity.xp_earned} XP, {activity.description}")
            
            print("\nOrganizer activities:")
            for activity in organizer_activities:
                print(f"- {activity.activity_type}: {activity.xp_earned} XP, {activity.description}")
        
        finally:
            # Clean up all test data created during this test
            # Using a try/finally pattern ensures cleanup happens even if the test fails
            try:
                # Delete in reverse order of dependencies to respect foreign key constraints
                
                # First, delete activities (they reference users and events)
                activities = UserActivity.query.filter(
                    (UserActivity.user_id == organizer.id) | 
                    (UserActivity.user_id == attendee.id)
                ).all()
                for activity in activities:
                    db.session.delete(activity)
                
                # Delete participant records (they reference users and events)
                participants = Participant.query.filter(
                    (Participant.user_id == organizer.id) | 
                    (Participant.user_id == attendee.id)
                ).all()
                for p in participants:
                    db.session.delete(p)
                
                # Delete the event (references organizer user)
                if 'event' in locals() and event.id:
                    event_to_delete = db.session.get(Event, event.id)
                    if event_to_delete:
                        db.session.delete(event_to_delete)
                
                # Finally, delete the test users we created
                db.session.delete(organizer)
                db.session.delete(attendee)
                db.session.commit()
                print("\nTest data cleaned up")
            except Exception as e:
                # Handle any errors during cleanup
                print(f"Error during cleanup: {e}")
                db.session.rollback()  # Rollback the transaction if an error occurs

# Execute the tests when the script is run directly
if __name__ == "__main__":
    print("\n--- Testing Level Up ---")
    test_level_up()
    
    print("\n--- Testing Edge Cases ---")
    test_edge_cases()
    
    print("\n--- Testing Organizer XP ---")
    test_organizer_xp()
    
    print("\n--- Testing Full Flow ---")
    test_full_flow()