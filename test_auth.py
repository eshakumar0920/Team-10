import requests
import json

BASE_URL = "http://localhost:5000/auth"

# ========== REGISTRATION TESTS ========== 
def test_register():
    """Test user registration"""
    print("\n=== Testing User Registration ===")
    data = {"email": "testuser1111@utdallas.edu", "password": "password12311"}
    response = requests.post(f"{BASE_URL}/register", json=data)
    print(f"Status code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_register_success():
    print("\n=== Testing Register: Valid utdallas email and strong password ===")
    data = {"email": "validuser@utdallas.edu", "password": "strongpass123"}
    response = requests.post(f"{BASE_URL}/register", json=data)
    print(f"Status code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    #print(response.status_code, response.json())

def test_register_missing_email():
    print("\n=== Testing Register: Missing email ===")
    data = {"password": "somepass"}
    response = requests.post(f"{BASE_URL}/register", json=data)
    print(f"Status code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    #print(response.status_code, response.json())

def test_register_missing_password():
    print("\n=== Testing Register: Missing password ===")
    data = {"email": "user@utdallas.edu"}
    response = requests.post(f"{BASE_URL}/register", json=data)
    print(f"Status code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    #print(response.status_code, response.json())

def test_register_invalid_email_domain():
    print("\n=== Testing Register: Non-utdallas email ===")
    data = {"email": "user@gmail.com", "password": "strongpass123"}
    response = requests.post(f"{BASE_URL}/register", json=data)
    print(f"Status code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    #print(response.status_code, response.json())

def test_register_weak_password():
    print("\n=== Testing Register: Weak password (less than 6 chars) ===")
    data = {"email": "weakpass@utdallas.edu", "password": "123"}
    response = requests.post(f"{BASE_URL}/register", json=data)
    print(f"Status code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    #print(response.status_code, response.json())

def test_register_email_already_exists():
    print("\n=== Testing Register: Duplicate email ===")
    data = {"email": "validuser@utdallas.edu", "password": "anotherpass"}
    response = requests.post(f"{BASE_URL}/register", json=data)
    print(f"Status code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    #print(response.status_code, response.json())

# ========== LOGIN TESTS ==========

def test_login():
    """Test user login"""
    print("\n=== Testing User Login ===")
    data = {"email": "test5user@gmail.com", "password": "password12311"}
    response = requests.post(f"{BASE_URL}/login", json=data)
    print(f"Status code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_login_success():
    print("\n=== Testing Login: Correct email and password ===")
    data = {"email": "validuser@utdallas.edu", "password": "strongpass123"}
    response = requests.post(f"{BASE_URL}/login", json=data)
    print(f"Status code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    #print(response.status_code, response.json())

def test_login_wrong_password():
    print("\n=== Testing Login: Wrong password ===")
    data = {"email": "validuser@utdallas.edu", "password": "wrongpassword"}
    response = requests.post(f"{BASE_URL}/login", json=data)
    print(f"Status code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    #print(response.status_code, response.json())

def test_login_unregistered_email():
    print("\n=== Testing Login: Unregistered email ===")
    data = {"email": "unknown@utdallas.edu", "password": "somepass"}
    response = requests.post(f"{BASE_URL}/login", json=data)
    print(f"Status code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    #print(response.status_code, response.json())

def test_login_missing_fields():
    print("\n=== Testing Login: Missing email and password ===")
    data = {}
    response = requests.post(f"{BASE_URL}/login", json=data)
    print(f"Status code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    #print(response.status_code, response.json())


# ========== VERIFICATION TESTS ==========

def test_verify():
    """Test verifying authenticated user"""
    print("\n=== Testing Token Verification ===")
    login_data = {"email": "test5user@gmail.com", "password": "password12311"}
    login_response = requests.post(f"{BASE_URL}/login", json=login_data)
    
    if login_response.status_code == 200:
        token = login_response.json().get("access_token")
        headers = {"Authorization": token}
        verify_response = requests.get(f"{BASE_URL}/verify", headers=headers)
        print(f"Status code: {verify_response.status_code}")
        print(f"Response: {json.dumps(verify_response.json(), indent=2)}")
    else:
        print("Login failed, skipping verification test.")

def test_verify_valid_token():
    print("\n === Testing Verify: Valid token ===")
    login_data = {"email": "validuser@utdallas.edu", "password": "strongpass123"}
    login_response = requests.post(f"{BASE_URL}/login", json=login_data)
    token = login_response.json().get("access_token")

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/verify", headers=headers)
    print(f"Status code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    #print(response.status_code, response.json())

def test_verify_missing_token():
    print("\n ===Verify: No token provided ===")
    response = requests.get(f"{BASE_URL}/verify")
    print(f"Status code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    #print(response.status_code, response.json())

def test_verify_invalid_token():
    print("\n=== Testing Verify: Invalid token ===")
    headers = {"Authorization": "Bearer invalidtoken123"}
    response = requests.get(f"{BASE_URL}/verify", headers=headers)
    print(f"Status code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    #print(response.status_code, response.json())



def run_all_tests():

    print("\n========== STARTING AUTH API TESTS ==========")
    print("\n----- REGISTRATION TESTS -----")
    test_register()
    test_register_success()
    test_register_missing_email()
    test_register_missing_password()
    test_register_invalid_email_domain()
    test_register_weak_password()
    test_register_email_already_exists()                                                                                            

    print("\n----- LOGIN TESTS -----")
    test_login()
    test_login_success()
    test_login_wrong_password()
    test_login_unregistered_email()
    test_login_missing_fields()

    print("\n----- VERIFICATION TESTS -----")
    test_verify()
    test_verify_valid_token()
    test_verify_missing_token()
    test_verify_invalid_token()
    
    print("\n=== All auth tests completed ===")

if __name__ == "__main__":
    run_all_tests()
