from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# PostgreSQL database configuration
# You can replace this with environment variables in production
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://eventadmin:your_password@localhost/events_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define your models
class Event(db.Model):
    __tablename__ = 'events'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    location = db.Column(db.String(100), nullable=False)
    event_date = db.Column(db.String(50), nullable=False)
    creator_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.String(50), nullable=False)
    
    participants = db.relationship('Participant', backref='event', lazy=True)

class Participant(db.Model):
    __tablename__ = 'participants'
    
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    joined_at = db.Column(db.String(50), nullable=False)
    
    __table_args__ = (db.UniqueConstraint('event_id', 'user_id', name='unique_participant'),)

# Create tables (only needed first time)
with app.app_context():
    db.create_all()

# API Endpoints
@app.route('/api/events', methods=['POST'])
def create_event():
    # Get JSON data from request
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['title', 'location', 'event_date', 'creator_id']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Create new event
    new_event = Event(
        title=data['title'],
        description=data.get('description', ''),
        location=data['location'],
        event_date=data['event_date'],
        creator_id=data['creator_id'],
        created_at=datetime.now().isoformat()
    )
    
    # Save to database
    db.session.add(new_event)
    db.session.commit()
    
    return jsonify({'id': new_event.id, 'message': 'Event created successfully'}), 201

@app.route('/api/events', methods=['GET'])
def get_events():
    # Get query parameters for filtering
    location = request.args.get('location')
    date = request.args.get('date')
    search_term = request.args.get('q')
    
    # Start with base query
    query = Event.query
    
    # Apply filters
    if location:
        query = query.filter(Event.location.ilike(f'%{location}%'))
    
    if date:
        query = query.filter(Event.event_date.like(f'{date}%'))
    
    if search_term:
        query = query.filter(
            db.or_(
                Event.title.ilike(f'%{search_term}%'),
                Event.description.ilike(f'%{search_term}%')
            )
        )
    
    # Add sorting
    query = query.order_by(Event.event_date.asc())
    
    # Execute query
    events = query.all()
    
    # Convert to list of dictionaries
    return jsonify([{
        'id': e.id,
        'title': e.title,
        'description': e.description,
        'location': e.location,
        'event_date': e.event_date,
        'creator_id': e.creator_id,
        'created_at': e.created_at
    } for e in events])

@app.route('/api/events/<int:event_id>', methods=['GET'])
def get_event(event_id):
    event = Event.query.get(event_id)
    
    if event is None:
        return jsonify({'error': 'Event not found'}), 404
    
    # Get participants count
    participants_count = Participant.query.filter_by(event_id=event_id).count()
    
    return jsonify({
        'id': event.id,
        'title': event.title,
        'description': event.description,
        'location': event.location,
        'event_date': event.event_date,
        'creator_id': event.creator_id,
        'created_at': event.created_at,
        'participants_count': participants_count
    })

@app.route('/api/events/<int:event_id>/join', methods=['POST'])
def join_event(event_id):
    data = request.get_json()
    
    # Validate user_id is provided
    if 'user_id' not in data:
        return jsonify({'error': 'Missing user_id field'}), 400
    
    user_id = data['user_id']
    
    # Check if event exists
    event = Event.query.get(event_id)
    if event is None:
        return jsonify({'error': 'Event not found'}), 404
    
    # Check if already joined
    existing = Participant.query.filter_by(
        event_id=event_id, 
        user_id=user_id
    ).first()
    
    if existing:
        return jsonify({'error': 'User already joined this event'}), 409
    
    # Create new participant
    new_participant = Participant(
        event_id=event_id,
        user_id=user_id,
        joined_at=datetime.now().isoformat()
    )
    
    db.session.add(new_participant)
    db.session.commit()
    
    return jsonify({'message': 'Successfully joined the event'})

@app.route('/api/events/<int:event_id>/leave', methods=['POST'])
def leave_event(event_id):
    data = request.get_json()
    
    # Validate user_id is provided
    if 'user_id' not in data:
        return jsonify({'error': 'Missing user_id field'}), 400
    
    user_id = data['user_id']
    
    # Find participant
    participant = Participant.query.filter_by(
        event_id=event_id, 
        user_id=user_id
    ).first()
    
    if not participant:
        return jsonify({'error': 'User is not participating in this event'}), 404
    
    # Delete the participant
    db.session.delete(participant)
    db.session.commit()
    
    return jsonify({'message': 'Successfully left the event'})

@app.route('/api/events/<int:event_id>/participants', methods=['GET'])
def get_participants(event_id):
    # Check if event exists
    event = Event.query.get(event_id)
    if event is None:
        return jsonify({'error': 'Event not found'}), 404
        
    # Get all participants for this event
    participants = Participant.query.filter_by(event_id=event_id).all()
    
    return jsonify([{
        'user_id': p.user_id,
        'joined_at': p.joined_at
    } for p in participants])

if __name__ == '__main__':
    app.run(debug=True)
