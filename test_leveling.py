# test_leveling.py
from app import create_app
from models import db, User, Event, Participant, UserActivity
app = create_app('dev')

def test_xp_system():
    with app.app_context():
        # Get test user and event
        user = User.query.filter_by(username="testuser1").first()
        event = Event.query.filter_by(title="Test Event 2").first()
        participant = Participant.query.filter_by(user_id=user.id, event_id=event.id).first()
        
        if not user or not event or not participant:
            print("Test data not found. Run test_data.py first.")
            return
        
        # Check initial XP and level
        print(f"Initial state: User {user.username} is at level {user.current_level} with {user.current_xp} XP")
        
        # Mark attendance and award XP
        participant.mark_attended()
        
        # Check updated XP and level - UPDATED LINE BELOW
        user = db.session.get(User, user.id)  # Refresh user from database using recommended method
        print(f"After attendance: User {user.username} is at level {user.current_level} with {user.current_xp} XP")
        
        # Award organizer XP
        event.award_creator_xp()
        
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
