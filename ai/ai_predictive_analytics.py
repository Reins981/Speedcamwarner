import json
import random
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, KFold
import lightgbm as lgb
import optuna
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

    def train_single_target(X_train, y_train, X_val, y_val, param):
        train_data = lgb.Dataset(X_train, label=y_train)
        valid_data = lgb.Dataset(X_val, label=y_val, reference=train_data)

        model = lgb.train(param, train_data, valid_sets=[valid_data], callbacks=[lgb.log_evaluation(0), lgb.early_stopping(50)])
        return model

    def objective(trial):
        param = {
            'objective': 'regression',
            'metric': 'rmse',
            'boosting_type': 'gbdt',
            'learning_rate': trial.suggest_loguniform('learning_rate', 0.01, 0.1),
            'num_leaves': trial.suggest_int('num_leaves', 20, 300),
            'max_depth': trial.suggest_int('max_depth', 5, 50),
            'min_data_in_leaf': trial.suggest_int('min_data_in_leaf', 10, 100),
            'feature_fraction': trial.suggest_uniform('feature_fraction', 0.5, 1.0),
        }

        kf = KFold(n_splits=3, shuffle=True, random_state=42)
        rmse_list = []

        for train_idx, valid_idx in kf.split(X_train):
            X_tr, X_val = X_train.iloc[train_idx], X_train.iloc[valid_idx]
            y_tr_lat, y_val_lat = y_train.iloc[train_idx, 0], y_train.iloc[valid_idx, 0]
            y_tr_lon, y_val_lon = y_train.iloc[train_idx, 1], y_train.iloc[valid_idx, 1]

            model_lat = train_single_target(X_tr, y_tr_lat, X_val, y_val_lat, param)
            model_lon = train_single_target(X_tr, y_tr_lon, X_val, y_val_lon, param)

            y_pred_lat = model_lat.predict(X_val)
            y_pred_lon = model_lon.predict(X_val)

            rmse_lat = np.sqrt(((y_val_lat - y_pred_lat) ** 2).mean())
            rmse_lon = np.sqrt(((y_val_lon - y_pred_lon) ** 2).mean())

            rmse_list.append((rmse_lat + rmse_lon) / 2)

        return np.mean(rmse_list)

    study = optuna.create_study(direction='minimize')
    study.optimize(objective, n_trials=50)

    best_params = study.best_params
    print(f"Best Parameters: {best_params}")

    # Train final models for latitude and longitude separately
    final_model_lat = lgb.LGBMRegressor(**best_params)
    final_model_lat.fit(X_train, y_train.iloc[:, 0])

    final_model_lon = lgb.LGBMRegressor(**best_params)
    final_model_lon.fit(X_train, y_train.iloc[:, 1])

    # Evaluate the models on the test set
    y_pred_lat = final_model_lat.predict(X_test)
    y_pred_lon = final_model_lon.predict(X_test)

    error_lat = np.sqrt(((y_test.iloc[:, 0] - y_pred_lat) ** 2).mean())
    error_lon = np.sqrt(((y_test.iloc[:, 1] - y_pred_lon) ** 2).mean())

    print(f"Prediction Error (Latitude): {error_lat}")
    print(f"Prediction Error (Longitude): {error_lon}")

    # Save the trained models to files
    joblib.dump(final_model_lat, 'speed_camera_model_lat.pkl')
    joblib.dump(final_model_lon, 'speed_camera_model_lon.pkl')
    print("Models saved as 'speed_camera_model_lat.pkl' and 'speed_camera_model_lon.pkl'")

    return final_model_lat, final_model_lon


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
