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
        #print("Login Successful")
        # Access the access token from the session attribute
        access_token = response.session.access_token
       # print(f"Login successful for user {email}")
        #return jsonify({"access_token": access_token}), 200
        return jsonify({
            "message": "Login successful",
            "email": email,
            "access_token": access_token
        }), 200
    except Exception as e:
        # More robust error handling
        #print(f"Login error: {str(e)}")
       # return jsonify({"error": str(e)}), 401
        error_message = str(e)

        if "Invalid login credentials" in error_message:
            return jsonify({
                "error": "Invalid email or password",
                "message": "Login failed"
            }), 401
        elif "user not found" in error_message.lower():
            return jsonify({
                "error": "User not found",
                "message": "No account exists with this email"
            }), 404
        else:
            return jsonify({
                "error": error_message,
                "message": "Login failed"
            }), 401
'''
@auth_bp.route("/verify", methods=["GET"])
def verify():
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"error": "Missing token"}), 401

    try:
        # Use .get_user() method correctly
        response = supabase.auth.get_user(token)
        
        # Access user information directly from the response
        #return jsonify(response.user.model_dump()), 200
        if response.get("error"):
            return jsonify({"error": response.error.message}), 401
            # Handle the case where there's an error in the response
            #return jsonify({"error": response["error"]["message"]}), 401
            
        user_data = { 
            "id": response.user.id,  # Access user ID
            "email": response.user.email,  # Access user email
            "created_at": response.user.created_at  # Access user creation date
        }
        return jsonify(user_data), 200  # Return user data as JSON
    except Exception as e:
        print(f"Verification error: {str(e)}")
        return jsonify({"error": str(e)}), 401
   
'''

@auth_bp.route("/verify", methods=["GET"])
def verify():
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"error": "Missing token"}), 401

    try:
        # Use .get_user() method correctly
        response = supabase.auth.get_user(token)

        # Check if there's an error directly in the response
        if hasattr(response, 'error') and response.error:
            return jsonify({"error": response.error.message}), 401
        
        # Ensure response.user exists before trying to access its attributes
        if hasattr(response, 'user'):
            user_data = {
                "id": response.user.id,  # Access user ID
                "email": response.user.email,  # Access user email
                "created_at": response.user.created_at  # Access user creation date
            }
            return jsonify(user_data), 200  # Return user data as JSON
        else:
            return jsonify({"error": "User not found"}), 404

    except Exception as e:
        print(f"Verification error: {str(e)}")
        return jsonify({"error": str(e)}), 401
