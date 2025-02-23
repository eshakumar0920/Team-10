'''
This is the intial echo server that can be used to test back-end features of our application.
You can connect to this server using your preferred HTTP client library.

How It Works:
    The server listens for POST requests at the /echo endpoint.
    It expects a JSON payload with a message key.
    It returns the same message wrapped in a JSON response.

Testing the Server:
You can use curl or Postman to test it.

-PG
'''

from flask import Flask, request, jsonify

# Initialize Flask app
app = Flask(__name__)

# Route for GET request - basic server check
@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({'status': 'server is running'})

# Route for POST request - echo message
@app.route('/echo', methods=['POST'])
def echo():
    try:
        # Print request content type and data for debugging
        print(f"Content-Type: {request.content_type}")
        print(f"Raw Data: {request.get_data(as_text=True)}")
        
        # Get the JSON data from the request
        data = request.get_json()
        
        # Check if message exists in the request
        if not data:
            return jsonify({
                'error': 'No JSON data received',
                'status': 'failed'
            }), 400
            
        if 'message' not in data:
            return jsonify({
                'error': 'No message provided',
                'status': 'failed'
            }), 400
        
        # Echo back the message
        return jsonify({
            'message': data['message'],
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'failed'
        }), 400

if __name__ == '__main__':
    # Run the server in debug mode
    app.run(debug=True, host='0.0.0.0', port=5000)
