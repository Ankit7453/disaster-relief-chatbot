import random
import pandas as pd
import os
import datetime

# Define core categories
intents = [
    'request_rescue', 'request_medical_aid', 'request_supplies', 'request_information',
    'missing_person', 'power_failure', 'evacuation_request', 'damage_report'
]

disaster_types = ['flood', 'landslide', 'earthquake', 'fire', 'cloudburst', 'drought', 'hailstorm']
districts = ['Nainital', 'Chamoli', 'Dehradun', 'Rudraprayag', 'Tehri', 'Pithoragarh', 'Almora', 'Uttarkashi', 'Bageshwar', 'Pauri']
regions = ['Kumaon', 'Garhwal']
severity_levels = ['low', 'moderate', 'high', 'critical']

# Multiple responses for realism
responses = {
    'request_rescue': [
        'Rescue team is being dispatched. Stay calm.',
        'Rescuers are on the way. Stay in a safe place.',
        'Help is coming, please keep your phone available for updates.'
    ],
    'request_medical_aid': [
        'Medical assistance is being sent. Avoid moving.',
        'A doctor team is on the way. Stay stable.',
        'We’ve informed the medical unit. Hold tight.'
    ],
    'request_supplies': [
        'Food and water are being arranged.',
        'Relief supplies are en route to your area.',
        'We’re sending basic supplies. Hang in there.'
    ],
    'request_information': [
        'Please check the official website for live updates.',
        'Contact local relief control rooms for latest info.',
        'Refer to your district disaster control number for details.'
    ],
    'missing_person': [
        'Our search team is looking into it.',
        'We’ve logged the missing person report.',
        'Authorities have been informed and are tracking the case.'
    ],
    'power_failure': [
        'Electricity board is addressing the failure.',
        'Power should be restored soon, stay patient.',
        'Repair work is in progress to restore power.'
    ],
    'evacuation_request': [
        'Evacuation is being coordinated, follow instructions.',
        'Evacuation orders are being sent. Stay alert.',
        'Your location is being reviewed for evacuation support.'
    ],
    'damage_report': [
        'Thank you. Damage team will assess and respond.',
        'We’ve logged your report for quick action.',
        'Our engineers are being notified to assess the damage.'
    ]
}

# Message templates with variations
message_templates = [
    "Help! Our house is stuck due to a {disaster} in {district}.",
    "Severe {disaster} has affected us in {district}, need urgent help!",
    "There is a {disaster} in {district}, please assist us.",
    "We are trapped in a {disaster} in {district}, send help!",
    "Due to {disaster}, situation is worsening in {district}. Need aid!",
    "Water and food are running out after {disaster} hit {district}.",
    "We need medical assistance due to {disaster} in {district}.",
    "Electricity has gone after {disaster} in {district}.",
    "People missing after {disaster} in {district}.",
    "We need to evacuate urgently due to {disaster} in {district}."
]

# Keyword mapping for intent detection
keyword_to_intent = {
    'trapped': 'request_rescue',
    'rescue': 'request_rescue',
    'medical': 'request_medical_aid',
    'doctor': 'request_medical_aid',
    'food': 'request_supplies',
    'water': 'request_supplies',
    'information': 'request_information',
    'missing': 'missing_person',
    'lost': 'missing_person',
    'power': 'power_failure',
    'electricity': 'power_failure',
    'evacuate': 'evacuation_request',
    'evacuation': 'evacuation_request',
    'damage': 'damage_report',
    'collapsed': 'damage_report'
}

def infer_intent(message):
    for keyword, intent in keyword_to_intent.items():
        if keyword in message.lower():
            return intent
    return random.choice(intents)  # fallback

def generate_data(n=5000):
    intent_data = []
    message_data = []
    response_data = []

    for i in range(n):
        disaster = random.choice(disaster_types)
        district = random.choice(districts)
        region = 'Kumaon' if district in ['Nainital', 'Almora', 'Pithoragarh', 'Bageshwar'] else 'Garhwal'
        severity = random.choice(severity_levels)
        user_id = f"user_{random.randint(1000, 9999)}"
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        message = random.choice(message_templates).format(disaster=disaster, district=district)
        intent = infer_intent(message)
        response = random.choice(responses[intent])

        # Append to datasets
        intent_data.append([message, disaster, district, region, severity, user_id, timestamp, intent])
        message_data.append([message, disaster, district, region, severity, user_id, timestamp])
        response_data.append([intent, response])

    return intent_data, message_data, response_data

# Generate datasets
intent_labels, disaster_messages, responses_data = generate_data(5000)

# Create DataFrames
df_intents = pd.DataFrame(intent_labels, columns=['message', 'disaster_type', 'district', 'region', 'severity', 'user_id', 'timestamp', 'intent'])
df_messages = pd.DataFrame(disaster_messages, columns=['message', 'disaster_type', 'district', 'region', 'severity', 'user_id', 'timestamp'])
df_responses = pd.DataFrame(responses_data, columns=['intent', 'response'])

# Save to CSV
df_intents.to_csv('disaster_intent_labels.csv', index=False)
df_messages.to_csv('disaster_messages_dataset.csv', index=False)
df_responses.to_csv('disaster_responses.csv', index=False)

print("✅ Improved datasets have been saved as 'disaster_intent_labels.csv', 'disaster_messages_dataset.csv', and 'disaster_responses.csv'.")
