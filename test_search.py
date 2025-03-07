import requests
import json

# Base URL of your API
BASE_URL = 'http://localhost:5000/api'

def test_search_events_by_query():
    """Test searching events by query parameter"""
    print("\n=== Testing Search Events by Query ===")
    response = requests.get(f'{BASE_URL}/search?query=Python')
    print(f"Status code: {response.status_code}")
    events = response.json()
    print(f"Found {len(events)} events")
    if events:
        print(f"First event: {json.dumps(events[0], indent=2)}")
    return events

def test_search_events_by_location():
    """Test searching events by location parameter"""
    print("\n=== Testing Search Events by Location ===")
    response = requests.get(f'{BASE_URL}/search?location=New York')
    print(f"Status code: {response.status_code}")
    events = response.json()
    print(f"Found {len(events)} events")
    if events:
        print(f"First event: {json.dumps(events[0], indent=2)}")
    return events

def test_search_events_by_date_range():
    """Test searching events by date range"""
    print("\n=== Testing Search Events by Date Range ===")
    response = requests.get(f'{BASE_URL}/search?date_from=2025-03-01&date_to=2025-03-10')
    print(f"Status code: {response.status_code}")
    events = response.json()
    print(f"Found {len(events)} events")
    if events:
        print(f"First event: {json.dumps(events[0], indent=2)}")
    return events

def test_search_events_empty_result():
    """Test searching events with no results"""
    print("\n=== Testing Search Events with No Results ===")
    response = requests.get(f'{BASE_URL}/search?query=NonexistentEvent')
    print(f"Status code: {response.status_code}")
    events = response.json()
    print(f"Found {len(events)} events")
    return events

def test_search_events_invalid_date():
    """Test searching events with invalid date format"""
    print("\n=== Testing Search Events with Invalid Date Format ===")
    response = requests.get(f'{BASE_URL}/search?date_from=invalid-date&date_to=2025-03-10')
    print(f"Status code: {response.status_code}")
    events = response.json()
    print(f"Found {len(events)} events")
    return events

def run_all_search_tests():
    """Run all search API tests"""
    # Test by query
    test_search_events_by_query()
    
    # Test by location
    test_search_events_by_location()
    
    # Test by date range
    test_search_events_by_date_range()
    
    # Test with no result
    test_search_events_empty_result()
    
    # Test with invalid date format
    test_search_events_invalid_date()

    print("\n=== All search tests completed ===")

if __name__ == "__main__":
    run_all_search_tests()
