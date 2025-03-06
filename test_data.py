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
        
        # Find the highest user ID currently in the database
        highest_user_id = db.session.query(db.func.max(User.id)).scalar() or 0
        start_id = highest_user_id + 1
        
        # Create test users with IDs that don't conflict
        users = [
            {"id": start_id, "username": "testuser1", "email": "user1@example.com", "password_hash": "password"},
            {"id": start_id + 1, "username": "testuser2", "email": "user2@example.com", "password_hash": "password"}
        ]
        
        user_ids = []
        for i, user_data in enumerate(users):
            # Check if user already exists by email
            existing_user = User.query.filter_by(email=user_data["email"]).first()
            if existing_user:
                user_ids.append(existing_user.id)
            else:
                user = User(**user_data)
                db.session.add(user)
                user_ids.append(user_data["id"])
        
        db.session.commit()
        
        # Create test events using the user IDs we have
        events = [
            {"title": "Test Event 1", "description": "Test description", "location": "Test location", 
             "event_date": "2023-12-01", "creator_id": user_ids[0], "xp_reward": 50},
            {"title": "Test Event 2", "description": "Another test event", "location": "Another location", 
             "event_date": "2023-12-15", "creator_id": user_ids[1], "xp_reward": 75}
        ]
        
        created_events = []
        for event_data in events:
            # Check if event with same title already exists
            if not Event.query.filter_by(title=event_data["title"]).first():
                event = Event(**event_data)
                db.session.add(event)
                created_events.append(event)
        
        db.session.commit()
        
        # Get event IDs (whether newly created or existing)
        event1 = Event.query.filter_by(title="Test Event 1").first()
        event2 = Event.query.filter_by(title="Test Event 2").first()
        
        if event1 and event2:
            # Check if participants already exist
            if not Participant.query.filter_by(event_id=event1.id, user_id=user_ids[1]).first():
                participant1 = Participant(event_id=event1.id, user_id=user_ids[1])
                db.session.add(participant1)
            
            if not Participant.query.filter_by(event_id=event2.id, user_id=user_ids[0]).first():
                participant2 = Participant(event_id=event2.id, user_id=user_ids[0])
                db.session.add(participant2)
            
            db.session.commit()
        
        print("Test data created successfully!")
if __name__ == "__main__":
    create_test_data()
