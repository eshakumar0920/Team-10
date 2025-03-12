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
    # Get query parameters
    query = request.args.get('query', '')
    location = request.args.get('location')
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')

    # Start with base query - only show future events
    events_query = Event.query.filter(Event.event_date >= datetime.now().isoformat())

    # Apply filters conditionally
    if query:
        events_query = events_query.filter(or_(
            Event.title.ilike(f'%{query}%'),
            Event.description.ilike(f'%{query}%')
        ))

    if location:
        events_query = events_query.filter(Event.location.ilike(f'%{location}%'))

    # Date filtering
    if date_from:
        try:
            from_date = datetime.fromisoformat(date_from)
            events_query = events_query.filter(Event.event_date >= from_date.isoformat())
        except ValueError:
            pass

    if date_to:
        try:
            to_date = datetime.fromisoformat(date_to)
            events_query = events_query.filter(Event.event_date <= to_date.isoformat())
        except ValueError:
            pass

    # Sort by event date (earliest first)
    events_query = events_query.order_by(Event.event_date)

    # Execute query
    events = events_query.all()
    
    # Return JSON response
    return jsonify([event.to_dict() for event in events])

#"Added event search functionality".
