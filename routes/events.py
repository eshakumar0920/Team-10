# routes/events.py
#from flask import Blueprint

#events_bp = Blueprint('events', __name__)

# Your route definitions here
# @events_bp.route('/events', methods=['GET'])
# def get_events():
#     ...
# routes/events.py
from flask import Blueprint, request, jsonify
from models import Event, db
from sqlalchemy import or_
from datetime import datetime

events_bp = Blueprint('events', __name__)
@events_bp.route('/search', methods=['GET'])
def search_events():
    # Mock data (simulating events in the database)
    mock_events = [
        {
            'id': 1,
            'title': 'Python Workshop',
            'description': 'Learn Python programming',
            'location': 'Texas',
            'event_date': '2025-03-10',
            'creator_id': 1,
            'created_at': '2025-03-01',
            'xp_reward': 50,
            'organizer_xp_reward': 200
        },
        {
            'id': 2,
            'title': 'JavaScript for Beginners',
            'description': 'Intro to JavaScript programming',
            'location': 'California',
            'event_date': '2025-04-01',
            'creator_id': 2,
            'created_at': '2025-03-01',
            'xp_reward': 50,
            'organizer_xp_reward': 200
        }
    ]

    # Get query parameters
    query = request.args.get('query', '')
    location = request.args.get('location')
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')

    # Start with mock events (simulate the filtering from database)
    filtered_events = mock_events

    # Apply filters conditionally
    if query:
        filtered_events = [event for event in filtered_events if query.lower() in event['title'].lower() or query.lower() in event['description'].lower()]

    if location:
        filtered_events = [event for event in filtered_events if location.lower() in event['location'].lower()]

    # Date filtering
    if date_from:
        try:
            from_date = datetime.fromisoformat(date_from)
            filtered_events = [event for event in filtered_events if datetime.fromisoformat(event['event_date']) >= from_date]
        except ValueError:
            pass

    if date_to:
        try:
            to_date = datetime.fromisoformat(date_to)
            filtered_events = [event for event in filtered_events if datetime.fromisoformat(event['event_date']) <= to_date]
        except ValueError:
            pass

    # Sort by event date (earliest first)
    filtered_events = sorted(filtered_events, key=lambda x: x['event_date'])

    # Return mock filtered events
    return jsonify(filtered_events)

#"Added event search functionality".
