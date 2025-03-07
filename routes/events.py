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
    try:
        # Get query parameters
        query = request.args.get('query', '', type=str)
        location = request.args.get('location', '', type=str)
        date_from = request.args.get('date_from', '', type=str)
        date_to = request.args.get('date_to', '', type=str)

        # Convert datetime.now() to a string format matching the database
        now_str = datetime.now().strftime("%Y-%m-%d")

        # Start with base query - only show future events
        events_query = Event.query.filter(Event.event_date >= now_str)

        # Apply filters conditionally
        if query:
            events_query = events_query.filter(or_(
                Event.title.ilike(f'%{query}%'),
                Event.description.ilike(f'%{query}%')
            ))

        if location:
            events_query = events_query.filter(Event.location.ilike(f'%{location}%'))

        # Date filtering with proper string conversion
        if date_from:
            try:
                from_date = datetime.strptime(date_from, "%Y-%m-%d").strftime("%Y-%m-%d")
                events_query = events_query.filter(Event.event_date >= from_date)
            except ValueError:
                return jsonify({"error": "Invalid date_from format. Use YYYY-MM-DD."}), 400

        if date_to:
            try:
                to_date = datetime.strptime(date_to, "%Y-%m-%d").strftime("%Y-%m-%d")
                events_query = events_query.filter(Event.event_date <= to_date)
            except ValueError:
                return jsonify({"error": "Invalid date_to format. Use YYYY-MM-DD."}), 400

        # Sort by event date (earliest first)
        events_query = events_query.order_by(Event.event_date)

        # Execute query
        events = events_query.all()

        # Return JSON response
        return jsonify([event.to_dict() for event in events]), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


#"Added event search functionality".
