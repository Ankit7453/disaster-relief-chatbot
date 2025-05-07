import pandas as pd
import numpy as np
import re
import pickle
import random
from process_data import clean_text, extract_location, extract_disaster_type
from transformers import pipeline
# Load responses
try:
    responses_df = pd.read_csv('data/disaster_responses.csv')
    responses_dict = dict(zip(responses_df['intent'], responses_df['response']))
except:
    # Fallback responses if file not found
    responses_dict = {
        'request_rescue': 'Rescue team is being sent. Stay safe.',
        'request_medical_aid': 'Medical assistance is on the way. Please stay calm.',
        'request_supplies': 'Relief team will reach shortly with essentials.',
        'request_information': 'You can contact the nearest relief center for more information.',
        'missing_person': 'We are searching for the missing person. Please stay available for updates.',
        'power_failure': 'The power supply will be restored soon. Please stay prepared.',
        'evacuation_request': 'Evacuation teams are being mobilized. Stay safe and follow instructions.'
    }

# Default responses for when intent prediction fails
default_responses = [
    "I understand this is a difficult situation. How can I assist you further?",
    "I'm here to help. Could you provide more details about your situation?",
    "Let me connect you with the appropriate disaster relief services.",
    "Your safety is our priority. Please stay in a secure location if possible.",
    "I'm processing your request. Please stand by for assistance."
]
classifier = pipeline("text-classification", model="bhadresh-savani/distilbert-base-uncased-emotion")
def generate_response(user_message, model=None):
    """Generate a response based on the user message and predicted intent"""
    # Clean the message
    cleaned_message = clean_text(user_message)
    
    # Extract location and disaster type
    location = extract_location(user_message)
    disaster_type = extract_disaster_type(user_message)
    
    # Predict intent using BERT if available
    if model is not None:
        try:
            intent = model.predict([cleaned_message])[0]
        except:
            # If prediction fails, use a default intent
            intent = random.choice(list(responses_dict.keys()))
    else:
        # Use BERT for intent prediction
        intent_result = classifier(user_message)
        intent = intent_result[0]['label'].lower()  # Extract the label of the prediction
    
    # Get response based on intent
    if intent in responses_dict:
        response = responses_dict[intent]
    else:
        response = random.choice(default_responses)
    
    # Personalize the response with location and disaster type if available
    # response = f"{response} The situation in {location} due to {disaster_type.lower()} is being handled. Please stay safe."
    
    return intent, response, disaster_type, location

def keyword_based_intent(message):
    """Determine intent based on keywords when model is not available"""
    message = message.lower()
    
    if any(word in message for word in ['rescue', 'save', 'help', 'stuck', 'trapped']):
        return 'request_rescue'
    
    if any(word in message for word in ['medical', 'doctor', 'hospital', 'injured', 'hurt', 'wound']):
        return 'request_medical_aid'
    
    if any(word in message for word in ['food', 'water', 'supplies', 'blanket', 'medicine', 'essentials']):
        return 'request_supplies'
    
    if any(word in message for word in ['information', 'update', 'news', 'status', 'situation']):
        return 'request_information'
    
    if any(word in message for word in ['missing', 'lost', 'find', 'locate', 'disappeared']):
        return 'missing_person'
    
    if any(word in message for word in ['power', 'electricity', 'outage', 'blackout']):
        return 'power_failure'
    
    if any(word in message for word in ['evacuate', 'evacuation', 'leave', 'escape']):
        return 'evacuation_request'
    
    # Default to information request if no keywords match
    return 'request_information'