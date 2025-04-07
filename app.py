from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests  # Required to call DeepSeek R1 API

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

# DeepSeek API Configuration
DEEPSEEK_API_URL = "https://api.deepseek.com/chat/completions"  # Replace with the actual API endpoint
DEEPSEEK_API_KEY = "YOUR_API_KEY"  # Replace with your DeepSeek API Key

@app.route('/')
def serve_html():
    """ Serve the frontend HTML file. """
    return send_from_directory('', 'deepseek_chat_ui.html')

@app.route('/chat', methods=['POST'])
def chat():
    """ Handle chat requests from the frontend. """
    data = request.json
    if not data or 'message' not in data:
        return jsonify({'error': 'No message provided'}), 400
    
    user_message = data['message']

    # Prepare payload for DeepSeek API
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "deepseek-chat",  # Adjust based on API docs
        "messages": [{"role": "user", "content": user_message}]
    }

    # Call DeepSeek API
    try:
        response = requests.post(DEEPSEEK_API_URL, json=payload, headers=headers)
        response_data = response.json()  # Convert response to JSON
        
        # Debugging: Print full API response
        print("API Response:", response_data)

        # Extract reply correctly based on API response format
        if "choices" in response_data and len(response_data["choices"]) > 0:
            bot_reply = response_data["choices"][0].get("message", {}).get("content", "I couldn't process that.")
        else:
            bot_reply = "I couldn't process that."
    
    except Exception as e:
        return jsonify({'error': f"API request failed: {str(e)}"}), 500

    return jsonify({'reply': bot_reply})

if __name__ == '__main__':
    app.run(debug=True)
