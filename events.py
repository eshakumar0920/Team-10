from flask import Blueprint, request, jsonify
from models import db, Event, Participant

events_bp = Blueprint('events', __name__)

@events_bp.route('/events', methods=['POST'])
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
        creator_id=data['creator_id']
    )
    
    # Save to database
    db.session.add(new_event)
    db.session.commit()
    
    return jsonify({'id': new_event.id, 'message': 'Event created successfully'}), 201

@events_bp.route('/events', methods=['GET'])
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
    return jsonify([event.to_dict() for event in events])

@events_bp.route('/events/<int:event_id>', methods=['GET'])
def get_event(event_id):
    event = Event.query.get(event_id)
    
    if event is None:
        return jsonify({'error': 'Event not found'}), 404
    
    # Get participants count
    participants_count = Participant.query.filter_by(event_id=event_id).count()
    
    event_data = event.to_dict()
    event_data['participants_count'] = participants_count
    
    return jsonify(event_data)

@events_bp.route('/events/<int:event_id>/join', methods=['POST'])
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
    new_participant = Participant(event_id, user_id)
    
    db.session.add(new_participant)
    db.session.commit()
    
    return jsonify({'message': 'Successfully joined the event'})

@events_bp.route('/events/<int:event_id>/leave', methods=['POST'])
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

@events_bp.route('/events/<int:event_id>/participants', methods=['GET'])
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
