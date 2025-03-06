# test_data.py
from app import create_app
from models import db, User, Level, Event, Participant
app = create_app('dev')
def create_test_data():
    with app.app_context():
        # Create levels
        levels = [
            {"level_number": 1, "xp_required": 0, "title": "Novice", "description": "Just starting out", "perks": "Basic access"},
            {"level_number": 2, "xp_required": 100, "title": "Explorer", "description": "Getting involved", "perks": "Create public events"},
            {"level_number": 3, "xp_required": 300, "title": "Enthusiast", "description": "Regular participant", "perks": "Priority registration"},
        ]
        
        for level_data in levels:
            if not Level.query.filter_by(level_number=level_data["level_number"]).first():
                level = Level(**level_data)
                db.session.add(level)
        
        db.session.commit()
        
        # Create test users with explicit IDs
        users = [
            {"id": 1, "username": "testuser1", "email": "user1@example.com", "password_hash": "password"},
            {"id": 2, "username": "testuser2", "email": "user2@example.com", "password_hash": "password"}
        ]
        
        created_users = []
        for user_data in users:
            if not User.query.filter_by(email=user_data["email"]).first():
                user = User(**user_data)
                db.session.add(user)
                created_users.append(user)
        
        db.session.commit()
        
        # Create test events
        events = [
            {"title": "Test Event 1", "description": "Test description", "location": "Test location", 
             "event_date": "2023-12-01", "creator_id": 1, "xp_reward": 50},
            {"title": "Test Event 2", "description": "Another test event", "location": "Another location", 
             "event_date": "2023-12-15", "creator_id": 2, "xp_reward": 75}
        ]
        
        created_events = []
        for event_data in events:
            event = Event(**event_data)
            db.session.add(event)
            created_events.append(event)
        
        db.session.commit()
        
        # Add participants to events
        participant1 = Participant(event_id=1, user_id=2)
        participant2 = Participant(event_id=2, user_id=1)
        
        db.session.add(participant1)
        db.session.add(participant2)
        db.session.commit()
        
        print("Test data created successfully!")
if __name__ == "__main__":
    create_test_data()
