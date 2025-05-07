# Disaster Relief Chatbot

A Python-based chatbot for disaster relief assistance using NLP techniques.

## Project Structure

\`\`\`
disaster_chatbot/
├── data/
│   ├── messages.csv
│   └── categories.csv
├── models/
│   └── classifier.pkl
├── templates/
│   └── index.html
├── static/
│   ├── style.css
│   └── script.js
├── app.py
├── train_classifier.py
├── process_data.py
├── chatbot_response.py
└── logs/
\`\`\`

## Setup Instructions

1. Clone this repository
2. Install the required packages:
   \`\`\`
   pip install flask pandas numpy scikit-learn
   \`\`\`
3. Generate the dataset:
   \`\`\`
   python generate_dataset.py
   \`\`\`
4. Process the data:
   \`\`\`
   python process_data.py
   \`\`\`
5. Train the model:
   \`\`\`
   python train_classifier.py
   \`\`\`
6. Run the application:
   \`\`\`
   python app.py
   \`\`\`
7. Open your browser and navigate to `http://127.0.0.1:5000/`

## Features

- Natural Language Processing for intent classification
- Real-time chat interface
- Location and disaster type extraction
- Emergency response prioritization
- Logging of all interactions
\`\`\`

## How to Run the Chatbot

1. First, save the dataset generation code you provided as `generate_dataset.py`

2. Install the required packages:
   \`\`\`
   pip install flask pandas numpy scikit-learn
   \`\`\`

3. Run the dataset generation script:
   \`\`\`
   python generate_dataset.py
   \`\`\`

4. Process the data:
   \`\`\`
   python process_data.py
   \`\`\`

5. Train the model:
   \`\`\`
   python train_classifier.py
   \`\`\`

6. Start the Flask application:
   \`\`\`
   python app.py
   \`\`\`

7. Open your browser and navigate to `http://127.0.0.1:5000/`

## How the Chatbot Works

1. **Data Processing**: The `process_data.py` script cleans the text data, extracts features like location and disaster type, and prepares it for model training.

2. **Model Training**: The `train_classifier.py` script trains a Logistic Regression model on the processed data to classify user messages into different intents.

3. **Response Generation**: The `chatbot_response.py` module uses the trained model to predict the intent of user messages and generates appropriate responses.

4. **Web Interface**: The Flask application serves an HTML/CSS/JavaScript frontend that allows users to interact with the chatbot in real-time.

5. **Logging**: All interactions are logged for future analysis and improvement.

The chatbot can handle various disaster-related queries, including requests for rescue, medical aid, supplies, information, reporting missing persons, power failures, and evacuation requests. It also extracts location and disaster type information from user messages to provide more personalized responses.

