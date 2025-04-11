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

    if not email.endswith("@utdallas.edu"):
        return jsonify({"error": "Only @utdallas.edu emails are allowed"}), 403
    
    # Check if the password length is less than 6 characters
    if len(password) < 6:
        return jsonify({"error": "Password is too short. It must be at least 6 characters."}), 400

    print(f"Attempting to register user with email: {email}")

    try:
        response = supabase.auth.sign_up({"email": email, "password": password})

        # Proper error checking using attribute access
        if hasattr(response, "error") and response.error:
            error_message = response.error.message

            if "email already exists" in error_message.lower():
                return jsonify({
                    "error": "Email already registered",
                    "message": "Account with this email already exists"
                }), 409

            return jsonify({
                "error": error_message,
                "message": "Registration failed"
            }), 400

        # Handle case where user object might be None
        if not hasattr(response, "user") or response.user is None:
            return jsonify({
                "error": "Unexpected error during registration",
                "message": "User not created"
            }), 500

        return jsonify({
            "message": "Registration successful. Please check your email to confirm your account.",
            "email": email
        }), 201

    except Exception as e:
        return jsonify({
            "error": str(e),
            "message": "Registration failed due to server error"
        }), 500

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Missing email or password"}), 400

    if not email.endswith("@utdallas.edu"):
        return jsonify({"error": "Only @utdallas.edu emails are allowed"}), 403

    try:
        # Use .sign_in_with_password() method
        response = supabase.auth.sign_in_with_password({
            "email": email, 
            "password": password
        })
        # Access the access token from the session attribute
        access_token = response.session.access_token
        return jsonify({
            "message": "Login successful",
            "email": email,
            "access_token": access_token
        }), 200
    except Exception as e:
        # More robust error handling
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

@auth_bp.route("/verify", methods=["GET"])
def verify():
    token = request.headers.get("Authorization")
    
    if not token:
        return jsonify({"error": "Missing token"}), 401

    # Remove "Bearer " prefix if included
    if token.startswith("Bearer "):
        token = token[7:]

    try:
        # Use .get_user() method to fetch user info
        response = supabase.auth.get_user(token)

        # Check for error in response
        if hasattr(response, 'error') and response.error:
            return jsonify({"error": response.error.message}), 401

        # Ensure response.user exists
        if hasattr(response, 'user') and response.user:
            user_data = {
                "id": response.user.id,
                "email": response.user.email,
                "created_at": response.user.created_at
            }
            return jsonify(user_data), 200
        else:
            return jsonify({"error": "User not found"}), 404

    except Exception as e:
        error_message = str(e)

        if "JWT expired" in error_message:
            return jsonify({"error": "Token expired"}), 401
        elif "Invalid token" in error_message or "invalid signature" in error_message.lower():
            return jsonify({"error": "Invalid token"}), 401
        else:
            return jsonify({
                "error": error_message,
                "message": "Verification failed"
            }), 401
