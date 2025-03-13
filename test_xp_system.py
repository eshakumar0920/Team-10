# test_xp_system.py
from app import create_app
from models import db, User, Event, Participant, UserActivity, Level
app = create_app('dev')

def test_level_up():
    """Test that a user levels up correctly when they gain enough XP"""
    with app.app_context():
        user = User.query.filter_by(username="testuser1").first()
        if not user:
            print("Test user not found. Run test_data.py first.")
            return
            
        # Reset user state
        user.current_xp = 0
        user.current_level = 1
        db.session.commit()
        
        # Check initial level
        print(f"Initial: User {user.username} is at level {user.current_level} with {user.current_xp} XP")
        
        # Award exactly enough XP to reach level 2 (should be 100 XP per test_data.py)
        user.award_xp(amount=100, activity_type='test_activity', description="Test level up")
        db.session.refresh(user)
        
        # Check level up
        print(f"After 100 XP: User {user.username} is at level {user.current_level} with {user.current_xp} XP")
        
        # Award more XP, but not enough to reach level 3
        user.award_xp(amount=150, activity_type='test_activity', description="More test XP")
        db.session.refresh(user)
        
        # Check level again
        print(f"After 250 XP: User {user.username} is at level {user.current_level} with {user.current_xp} XP")
        
        # Award enough to reach level 3
        user.award_xp(amount=50, activity_type='test_activity', description="Final test XP")
        db.session.refresh(user)
        
        # Final check
        print(f"After 300 XP: User {user.username} is at level {user.current_level} with {user.current_xp} XP")

def test_edge_cases():
    """Test various edge cases in the XP system"""
    with app.app_context():
        user = User.query.filter_by(username="testuser2").first()
        event = Event.query.filter_by(title="Test Event 1").first()
        
        if not user or not event:
            print("Test data not found. Run test_data.py first.")
            return
            
        # Reset user state
        user.current_xp = 100
        user.current_level = 1
        db.session.commit()
        
        print(f"Initial: User {user.username} has {user.current_xp} XP")
        
        # Test 1: Attempt to award negative XP
        result = user.award_xp(amount=-50, activity_type='test_negative', description="Test negative XP")
        db.session.refresh(user)
        print(f"After negative XP attempt: User has {user.current_xp} XP, Award result: {result}")
        
        # Test 2: Attempt to mark attendance twice
        # Clear any existing participants
        existing = Participant.query.filter_by(user_id=user.id, event_id=event.id).all()
        for p in existing:
            db.session.delete(p)
        db.session.commit()
        
        # Create new participant and mark attended
        participant = Participant(event_id=event.id, user_id=user.id)
        db.session.add(participant)
        db.session.commit()
        
        # Mark attended first time
        result1 = participant.mark_attended()
        db.session.refresh(user)
        first_xp = user.current_xp
        
        # Mark attended second time
        result2 = participant.mark_attended()
        db.session.refresh(user)
        second_xp = user.current_xp
        
        print(f"First attend: {result1}, XP = {first_xp}")
        print(f"Second attend: {result2}, XP = {second_xp}")
        
        # Test 3: Very large XP value
        initial_xp = user.current_xp
        user.award_xp(amount=1000000, activity_type='test_large', description="Test large XP amount")
        db.session.refresh(user)
        print(f"After large XP: Level = {user.current_level}, XP = {user.current_xp}, Increase = {user.current_xp - initial_xp}")

def test_organizer_xp():
    """Test that event organizers receive the correct XP"""
    with app.app_context():
        # Find event and creator
        event = Event.query.filter_by(title="Test Event 1").first()
        if not event:
            print("Test event not found. Run test_data.py first.")
            return
            
        creator = db.session.get(User, event.creator_id)
        if not creator:
            print(f"Creator user (ID: {event.creator_id}) not found.")
            return
            
        # Reset creator's XP
        initial_xp = creator.current_xp
        
        # Award organizer XP
        print(f"Event organizer XP reward: {event.organizer_xp_reward}")
        print(f"Before: Creator {creator.username} has {creator.current_xp} XP")
        
        result = event.award_creator_xp()
        db.session.refresh(creator)
        
        print(f"After: Creator {creator.username} has {creator.current_xp} XP")
        print(f"XP increase: {creator.current_xp - initial_xp}")
        print(f"Award result: {result}")

def test_full_flow():
    """Test a complete user journey through the XP system"""
    with app.app_context():
        # Find the highest user ID currently in the database
        highest_user_id = db.session.query(db.func.max(User.id)).scalar() or 0
        
        # Create new test users with explicit IDs
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
            # Create an event
            event = Event(
                title="XP System Test Event",
                description="Testing the full XP system",
                location="Test Location",
                event_date="2023-12-31",
                creator_id=organizer.id,
                xp_reward=50,
                organizer_xp_reward=200
            )
            db.session.add(event)
            db.session.commit()
            
            print(f"Created event: {event.title} by {organizer.username}")
            print(f"Organizer initial XP: {organizer.current_xp}")
            print(f"Attendee initial XP: {attendee.current_xp}")
            
            # Register attendee for event
            participant = Participant(event_id=event.id, user_id=attendee.id)
            db.session.add(participant)
            db.session.commit()
            print(f"Registered attendee for event")
            
            # Mark attendance
            participant.mark_attended()
            db.session.refresh(attendee)
            print(f"After attendance: Attendee XP = {attendee.current_xp}")
            
            # Award organizer XP
            event.award_creator_xp()
            db.session.refresh(organizer)
            print(f"After organization: Organizer XP = {organizer.current_xp}")
            
            # Check user activities
            attendee_activities = UserActivity.query.filter_by(user_id=attendee.id).all()
            organizer_activities = UserActivity.query.filter_by(user_id=organizer.id).all()
            
            print("\nAttendee activities:")
            for activity in attendee_activities:
                print(f"- {activity.activity_type}: {activity.xp_earned} XP, {activity.description}")
            
            print("\nOrganizer activities:")
            for activity in organizer_activities:
                print(f"- {activity.activity_type}: {activity.xp_earned} XP, {activity.description}")
        
        finally:
            # Clean up test data - use try/except to ensure cleanup happens even if test fails
            try:
                # Delete activities first (foreign key constraints)
                activities = UserActivity.query.filter(
                    (UserActivity.user_id == organizer.id) | 
                    (UserActivity.user_id == attendee.id)
                ).all()
                for activity in activities:
                    db.session.delete(activity)
                
                # Delete participant
                participants = Participant.query.filter(
                    (Participant.user_id == organizer.id) | 
                    (Participant.user_id == attendee.id)
                ).all()
                for p in participants:
                    db.session.delete(p)
                
                # Delete the event
                if 'event' in locals() and event.id:
                    event_to_delete = db.session.get(Event, event.id)
                    if event_to_delete:
                        db.session.delete(event_to_delete)
                
                # Delete the test users
                db.session.delete(organizer)
                db.session.delete(attendee)
                db.session.commit()
                print("\nTest data cleaned up")
            except Exception as e:
                print(f"Error during cleanup: {e}")
                db.session.rollback()

if __name__ == "__main__":
    print("\n--- Testing Level Up ---")
    test_level_up()
    
    print("\n--- Testing Edge Cases ---")
    test_edge_cases()
    
    print("\n--- Testing Organizer XP ---")
    test_organizer_xp()
    
    print("\n--- Testing Full Flow ---")
    test_full_flow()