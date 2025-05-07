import pandas as pd
import numpy as np
import pickle
import os
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC 
from sklearn.metrics import classification_report
from sklearn.pipeline import Pipeline

def train_model():
    """Train and save the NLP classifier model using SVM"""
    # Check if processed data exists
    if not os.path.exists('data/processed_messages.csv') or not os.path.exists('data/categories.csv'):
        print("Processed data not found. Please run process_data.py first.")
        return
    
    # Create models directory if it doesn't exist
    if not os.path.exists('models'):
        os.makedirs('models')
    
    # Load the processed data
    messages_df = pd.read_csv('data/processed_messages.csv')
    categories_df = pd.read_csv('data/categories.csv')
    
    # Merge datasets if needed
    if 'intent' not in messages_df.columns:
        df = pd.merge(messages_df, categories_df, on='message', how='inner')
    else:
        df = messages_df
    
    # Split the data
    X = df['clean_message'] if 'clean_message' in df.columns else df['message']
    y = df['intent']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Load the vectorizer
    with open('data/vectorizer.pkl', 'rb') as f:
        vectorizer = pickle.load(f)
    
    # Use SVM 
    model = LinearSVC()

    # Create a pipeline
    pipeline = Pipeline([
        ('tfidf', vectorizer),
        ('classifier', model)
    ])
    
    # Train the model
    pipeline.fit(X_train, y_train)
    
    # Evaluate the model
    y_pred = pipeline.predict(X_test)
    print(classification_report(y_test, y_pred))
    
    # Save the model
    with open('models/classifier.pkl', 'wb') as f:
        pickle.dump(pipeline, f)
    
    print("Model trained with SVM and saved to models/classifier.pkl")

if __name__ == "__main__":
    train_model()
