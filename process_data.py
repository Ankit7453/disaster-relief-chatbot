import pandas as pd
import numpy as np
import re
import pickle
import os
from sklearn.feature_extraction.text import TfidfVectorizer

def clean_text(text):
    """Clean and preprocess text data"""
    # Convert to lowercase
    text = text.lower()
    
    # Remove special characters and digits
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def extract_location(text):
    """Extract location information from text"""
    # List of locations from the dataset
    districts = ['nainital', 'chamoli', 'dehradun', 'rudraprayag', 'tehri', 'pithoragarh', 'almora', 'uttarkashi']
    regions = ['kumaon', 'garhwal']
    
    # Check for districts
    for district in districts:
        if district in text.lower():
            return district.capitalize()
    
    # Check for regions
    for region in regions:
        if region in text.lower():
            return region.capitalize()
    
    return "Unknown"

def extract_disaster_type(text):
    """Extract disaster type from text"""
    disaster_types = ['flood', 'landslide', 'earthquake', 'fire', 'cloudburst']
    
    for disaster in disaster_types:
        if disaster in text.lower():
            return disaster.capitalize()
    
    return "Unknown"

def process_data(input_file, output_dir='data'):
    """Process and save the data"""
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Read the data
    df = pd.read_csv(input_file)
    
    # Clean the messages
    df['clean_message'] = df['message'].apply(clean_text)
    
    # Extract features if they don't exist
    if 'disaster_type' not in df.columns:
        df['disaster_type'] = df['message'].apply(extract_disaster_type)
    
    if 'location' not in df.columns and 'district' not in df.columns:
        df['location'] = df['message'].apply(extract_location)
    elif 'district' in df.columns:
        df['location'] = df['district']
    
    # Create a TF-IDF vectorizer
    vectorizer = TfidfVectorizer(max_features=5000)
    X = vectorizer.fit_transform(df['clean_message'])
    
    # Save the vectorizer
    with open(f'{output_dir}/vectorizer.pkl', 'wb') as f:
        pickle.dump(vectorizer, f)
    
    # Save processed data
    df.to_csv(f'{output_dir}/processed_messages.csv', index=False)
    
    # If we have intent labels, save them separately
    if 'intent' in df.columns:
        df[['message', 'intent']].to_csv(f'{output_dir}/categories.csv', index=False)
    
    print(f"Data processed and saved to {output_dir}/")
    return df, X

if __name__ == "__main__":
    # Process the intent labels dataset
    process_data('disaster_intent_labels.csv')