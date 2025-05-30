import os
import logging
from flask import Flask, render_template, request, jsonify
from chatbot import EntertainmentChatbot

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "entertainment-chatbot-secret-key")

# Initialize chatbot
chatbot = EntertainmentChatbot()

@app.route('/')
def index():
    """Main chat interface"""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({
                'error': 'Message cannot be empty'
            }), 400
        
        # Get bot response
        bot_response = chatbot.get_response(user_message)
        
        return jsonify({
            'response': bot_response['message'],
            'quick_replies': bot_response.get('quick_replies', []),
            'category': bot_response.get('category', 'general')
        })
        
    except Exception as e:
        logging.error(f"Error in chat endpoint: {str(e)}")
        return jsonify({
            'error': 'Sorry, I encountered an error. Please try again!'
        }), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
