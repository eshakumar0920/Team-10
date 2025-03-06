import requests
import json
import os
import sys
from pathlib import Path

# Add parent directory to path so we can import app
sys.path.append(str(Path(__file__).parent))

# Base URL of your API
BASE_URL = 'http://localhost:5000/api'

def test_create_user():
    """Test creating a new user for testing purposes"""
    print("\n=== Creating Test User ===")
    user_data = {
        "name": "Test User",
        "email": "testuser@example.com",
        "password": "password123"  # Add other required fields as needed
    }
    
    response = requests.post(f'{BASE_URL}/users', json=user_data)
    print(f"Status code: {response.status_code}")
    
    if response.status_code == 201:
        print(f"Created test user: {json.dumps(response.json(), indent=2)}")
        return response.json().get('id')
    else:
        print(f"Failed to create test user: {response.text}")
        return None

def test_get_existing_user():
    """Get an existing user to use for tests"""
    print("\n=== Finding Existing User ===")
    response = requests.get(f'{BASE_URL}/users')
    
    if response.status_code == 200 and response.json():
        users = response.json()
        first_user = users[0]
        user_id = first_user.get('id')
        print(f"Using existing user with ID: {user_id}")
        return user_id
    return None

def test_create_event():
    """Test creating a new event"""
    print("\n=== Testing Event Creation ===")
    event_data = {
        "title": "Python Coding Workshop",
        "description": "Learn Python basics and Flask development",
        "location": "Computer Lab 101",
        "event_date": "2025-03-15T14:00:00",
        "creator_id": 1
    }
    
    response = requests.post(f'{BASE_URL}/events', json=event_data)
    print(f"Status code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 201:
        return response.json().get('id')
    return None

def test_get_all_events():
    """Test retrieving all events"""
    print("\n=== Testing Get All Events ===")
    response = requests.get(f'{BASE_URL}/events')
    print(f"Status code: {response.status_code}")
    events = response.json()
    print(f"Found {len(events)} events")
    if events:
        print(f"First event: {json.dumps(events[0], indent=2)}")
    return events

def test_get_event(event_id):
    """Test retrieving a specific event"""
    print(f"\n=== Testing Get Event {event_id} ===")
    response = requests.get(f'{BASE_URL}/events/{event_id}')
    print(f"Status code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_join_event(event_id, user_id):
    """Test joining an event"""
    print(f"\n=== Testing Join Event {event_id} (User {user_id}) ===")
    response = requests.post(
        f'{BASE_URL}/events/{event_id}/join',
        json={"user_id": user_id}
    )
    print(f"Status code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_get_participants(event_id):
    """Test getting event participants"""
    print(f"\n=== Testing Get Participants for Event {event_id} ===")
    response = requests.get(f'{BASE_URL}/events/{event_id}/participants')
    print(f"Status code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_leave_event(event_id, user_id):
    """Test leaving an event"""
    print(f"\n=== Testing Leave Event {event_id} (User {user_id}) ===")
    response = requests.post(
        f'{BASE_URL}/events/{event_id}/leave',
        json={"user_id": user_id}
    )
    print(f"Status code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def run_all_tests():
    """Run all API tests"""
    # Get an existing user or create a new test user
    user_id = test_get_existing_user()
    if not user_id:
        user_id = test_create_user()
        if not user_id:
            print("Failed to get or create a valid user, stopping tests.")
            return
    
    # Create an event
    event_id = test_create_event()
    if not event_id:
        print("Failed to create event, stopping tests.")
        return
    
    # Get all events
    test_get_all_events()
    
    # Get specific event
    test_get_event(event_id)
    
    # Join event
    test_join_event(event_id, user_id)
    
    # Get participants
    test_get_participants(event_id)
    
    # Leave event
    test_leave_event(event_id, user_id)
    
    print("\n=== All tests completed ===")

if __name__ == "__main__":
    run_all_tests()
