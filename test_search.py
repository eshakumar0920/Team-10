import requests
import json

# Base URL of your API
BASE_URL = 'http://localhost:5000/api/search'

def test_search_events_by_query():
    """Test searching events by title"""
    print("\n=== Testing Search Events by Query ===")
    params = {'query': 'Python'}
    response = requests.get(BASE_URL, params=params)
    print(f"Status code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_search_events_by_location():
    """Test searching events by location"""
    print("\n=== Testing Search Events by Location ===")
    params = {'location': 'New York'}
    response = requests.get(BASE_URL, params=params)
    print(f"Status code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_search_events_by_date_range():
    """Test searching events within a specific date range"""
    print("\n=== Testing Search Events by Date Range ===")
    params = {'date_from': '2025-03-01', 'date_to': '2025-03-10'}
    response = requests.get(BASE_URL, params=params)
    print(f"Status code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_search_events_no_results():
    """Test searching for an event that does not exist"""
    print("\n=== Testing Search with No Results ===")
    params = {'query': 'Blockchain'}
    response = requests.get(BASE_URL, params=params)
    print(f"Status code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_search_events_invalid_date():
    """Test searching with an invalid date format"""
    print("\n=== Testing Search with Invalid Date Format ===")
    params = {'date_from': 'invalid-date', 'date_to': '2025-03-10'}
    response = requests.get(BASE_URL, params=params)
    print(f"Status code: {response.status_code}")
    print(f"Response: {response.text}")  # Print raw response to debug

def run_all_search_tests():
    """Run all search API tests"""
    test_search_events_by_query()
    test_search_events_by_location()
    test_search_events_by_date_range()
    test_search_events_no_results()
    test_search_events_invalid_date()
    print("\n=== All search tests completed ===")

if __name__ == "__main__":
    run_all_search_tests()
