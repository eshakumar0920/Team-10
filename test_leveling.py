# test_leveling.py
from app import create_app
from models import db, User, Event, Participant, UserActivity
app = create_app('dev')

def test_xp_system():
    with app.app_context():
        # Get test user and event
        user = User.query.filter_by(username="testuser1").first()
        event = Event.query.filter_by(title="Test Event 2").first()
        
        if not user or not event:
            print("Test data not found. Run test_data.py first.")
            return
        
        # Reset the user's XP to 0 for testing
        user.current_xp = 0
        user.current_level = 1
        db.session.commit()
        
        # Delete any existing participant record to start fresh
        existing_participant = Participant.query.filter_by(user_id=user.id, event_id=event.id).first()
        if existing_participant:
            db.session.delete(existing_participant)
            db.session.commit()
            
        # Delete any existing activity records for this user/event
        existing_activities = UserActivity.query.filter_by(
            user_id=user.id, 
            related_event_id=event.id
        ).all()
        for activity in existing_activities:
            db.session.delete(activity)
        db.session.commit()
        
        # Create a new participant record
        participant = Participant(event_id=event.id, user_id=user.id)
        db.session.add(participant)
        db.session.commit()
        
        # Check initial XP and level
        print(f"Initial state: User {user.username} is at level {user.current_level} with {user.current_xp} XP")
        
        # Mark attendance and award XP
        participant.mark_attended()
        
        # Refresh user from database to get updated values
        db.session.refresh(user)
        print(f"After attendance: User {user.username} is at level {user.current_level} with {user.current_xp} XP")
        
        # Award organizer XP
        event.award_creator_xp()
        
        # Refresh user again
        db.session.refresh(user)
        
        # Check user activities
        activities = UserActivity.query.filter_by(user_id=user.id).all()
        print(f"\nUser activities for {user.username}:")
        for activity in activities:
            print(f"- {activity.activity_type}: {activity.xp_earned} XP, {activity.description}")
        
        # Check if level up occurred
        if user.current_level > 1:
            print(f"\nUser has leveled up to level {user.current_level}!")
        else:
            print("\nUser has not leveled up yet.")

if __name__ == "__main__":
    test_xp_system()