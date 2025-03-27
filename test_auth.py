import requests
import json

BASE_URL = "http://localhost:5000/auth"

def test_register():
    """Test user registration"""
    print("\n=== Testing User Registration ===")
    data = {"email": "test3user@gmail.com", "password": "password12311"}
    response = requests.post(f"{BASE_URL}/register", json=data)
    print(f"Status code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_login():
    """Test user login"""
    print("\n=== Testing User Login ===")
    data = {"email": "test3user@gmail.com", "password": "password12311"}
    response = requests.post(f"{BASE_URL}/login", json=data)
    print(f"Status code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_verify():
    """Test verifying authenticated user"""
    print("\n=== Testing Token Verification ===")
    login_data = {"email": "test3user@gmail.com", "password": "password12311"}
    login_response = requests.post(f"{BASE_URL}/login", json=login_data)
    
    if login_response.status_code == 200:
        token = login_response.json().get("access_token")
        headers = {"Authorization": token}
        verify_response = requests.get(f"{BASE_URL}/verify", headers=headers)
        print(f"Status code: {verify_response.status_code}")
        print(f"Response: {json.dumps(verify_response.json(), indent=2)}")
    else:
        print("Login failed, skipping verification test.")

def run_all_tests():
    test_register()
    test_login()
    test_verify()
    print("\n=== All auth tests completed ===")

if __name__ == "__main__":
    run_all_tests()
