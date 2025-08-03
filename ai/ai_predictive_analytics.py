import json
import random
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor  # Replace RandomForestClassifier with RandomForestRegressor
from sklearn.metrics import accuracy_score
import joblib  # Add this import at the top


# Load camera data
def load_camera_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


# Simulate driving data
def simulate_driving_data(camera_data, num_samples=1000):
    samples = []
    for _ in range(num_samples):
        camera = random.choice(camera_data['cameras'])
        coordinates = camera['coordinates'][0]  # Extract the first dictionary in the coordinates list
        sample = {
            'latitude': random.uniform(coordinates['latitude'] - 0.01, coordinates['latitude'] + 0.01),
            'longitude': random.uniform(coordinates['longitude'] - 0.01, coordinates['longitude'] + 0.01),
            'time_of_day': random.choice(['morning', 'afternoon', 'evening', 'night']),
            'day_of_week': random.choice(['weekday', 'weekend']),
            'camera_latitude': coordinates['latitude'],
            'camera_longitude': coordinates['longitude']
        }
        samples.append(sample)
    return pd.DataFrame(samples)


# Train predictive model
def train_model(data):
    X = data[['latitude', 'longitude', 'time_of_day', 'day_of_week']]
    y = data[['camera_latitude', 'camera_longitude']]
    
    # Define all possible categories for 'time_of_day' and 'day_of_week'
    all_time_of_day = ['morning', 'afternoon', 'evening', 'night']
    all_day_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    # Convert categorical variables to dummy variables
    X = pd.get_dummies(X, columns=['time_of_day', 'day_of_week'])

    # Ensure all expected columns are present
    for time in all_time_of_day:
        col = f'time_of_day_{time}'
        if col not in X.columns:
            X[col] = 0

    for day in all_day_of_week:
        col = f'day_of_week_{day}'
        if col not in X.columns:
            X[col] = 0

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestRegressor()  # Use RandomForestRegressor for regression
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    # Calculate prediction error
    error = np.sqrt(((y_test - y_pred) ** 2).mean(axis=0))
    print(f"Prediction Error (Latitude, Longitude): {error}")

    # Save the trained model to a file
    joblib.dump(model, 'speed_camera_model.pkl')
    print("Model saved as 'speed_camera_model.pkl'")

    return model


def predict_speed_camera(model, latitude, longitude, time_of_day, day_of_week):
    """
    Predict the approximate coordinates of the nearest speed camera based on input features.
    """
    # Normalize time_of_day and day_of_week to match training categories
    if ":" in time_of_day:
        time_of_day = "evening" if int(time_of_day.split(":")[0]) > 18 else "morning"

    input_data = {
        'latitude': [latitude],
        'longitude': [longitude],
        'time_of_day': [time_of_day],
        'day_of_week': [day_of_week]
    }

    # Convert input data to DataFrame and encode categorical variables
    input_df = pd.DataFrame(input_data)
    input_df = pd.get_dummies(input_df, columns=['time_of_day', 'day_of_week'])

    # Ensure all expected columns are present and in the correct order
    for col in model.feature_names_in_:
        if col not in input_df.columns:
            input_df[col] = 0
    input_df = input_df[model.feature_names_in_]

    # Predict using the model
    prediction = model.predict(input_df)
    return prediction[0].tolist()  # Return the first predicted coordinates as a list


# Main function
def main():
    camera_data = load_camera_data('training.json')
    driving_data = simulate_driving_data(camera_data)
    model = train_model(driving_data)
    print("Predictive model trained successfully!")


if __name__ == "__main__":
    main()
