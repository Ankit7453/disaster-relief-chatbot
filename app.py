from flask import Flask, render_template, request, jsonify
import pickle
import os
import logging
from datetime import datetime
from chatbot_response import generate_response

app = Flask(__name__)

# Configure logging
if not os.path.exists('logs'):
    os.makedirs('logs')

logging.basicConfig(
    filename=f'logs/chatbot_{datetime.now().strftime("%Y%m%d")}.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Load the trained model
try:
    with open('models/classifier.pkl', 'rb') as f:
        model = pickle.load(f)
    logging.info("Model loaded successfully")
except Exception as e:
    logging.error(f"Error loading model: {str(e)}")
    model = None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Log the incoming message
        logging.info(f"User message: {user_message}")
        
        # Generate response using the chatbot_response module
        intent, response, disaster_type, location = generate_response(user_message, model)
        
        # Log the response
        logging.info(f"Bot response: {response} (Intent: {intent})")
        
        return jsonify({
            'response': response,
            'intent': intent,
            'disaster_type': disaster_type,
            'location': location
        })
    
    except Exception as e:
        logging.error(f"Error processing message: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True)