from flask import Blueprint, request, jsonify
from config import Config  # Import Config class

auth_bp = Blueprint("auth", __name__)

# Get the Supabase client instance using Config class
supabase = Config.get_supabase_client()

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Missing email or password"}), 400
    
    # Debug: Log email to confirm it's correct
    print(f"Attempting to register user with email: {email}")
    '''
    response = supabase.auth.sign_up({"email": email, "password": password})

    if "error" in response:
        return jsonify({"error": response["error"]["message"]}), 400

    return jsonify({"message": "User registered successfully"}), 201'
    '''
    try:
        # Attempt to register the user
        response = supabase.auth.sign_up({"email": email, "password": password})

        # If an error is returned in the response, log it
        if "error" in response:
            print(f"Error in registration: {response['error']['message']}")
            return jsonify({"error": response["error"]["message"]}), 400
        
        print(f"User registered successfully: {response}")
        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        # If any exception occurs, print the error
        print(f"Exception occurred: {e}")
        return jsonify({"error": str(e)}), 400

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    '''
    response = supabase.auth.sign_in_with_password({"email": email, "password": password})

    if "error" in response:
        return jsonify({"error": response["error"]["message"]}), 401

    return jsonify({"access_token": response["session"]["access_token"]}), 200 '''

    try:
        # Use .sign_in_with_password() method
        response = supabase.auth.sign_in_with_password({
            "email": email, 
            "password": password
        })

        # Access the access token from the session attribute
        access_token = response.session.access_token

        return jsonify({"access_token": access_token}), 200
    except Exception as e:
        # More robust error handling
        print(f"Login error: {str(e)}")
        return jsonify({"error": str(e)}), 401

@auth_bp.route("/verify", methods=["GET"])
def verify():
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"error": "Missing token"}), 401

    try:
        # Use .get_user() method correctly
        response = supabase.auth.get_user(token)
        
        # Access user information directly from the response
        return jsonify(response.user.model_dump()), 200
    except Exception as e:
        print(f"Verification error: {str(e)}")
        return jsonify({"error": str(e)}), 401
    '''
    response = supabase.auth.get_user(token)
    if "error" in response:
        return jsonify({"error": response["error"]["message"]}), 401

    return jsonify(response["user"]), 200 '''
