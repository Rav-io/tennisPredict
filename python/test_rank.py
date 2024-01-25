import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
import numpy as np

def predict_by_rank(player1_id, player2_id, player1_rank_points, player2_rank_points, surface):
    model_filename = 'tennis_model_trained_with_surface.joblib'
    model = joblib.load(model_filename)

    surface = surface.capitalize()

    test_data = pd.DataFrame({
        'player1_id': [player1_id],
        'player2_id': [player2_id],
        'player1_rank_points': [player1_rank_points],
        'player2_rank_points': [player2_rank_points],
        'surface': [surface]
    })

    surface_encoder = LabelEncoder()
    test_data['surface_encoded'] = surface_encoder.fit_transform(test_data['surface'])
    surface_encoded = pd.get_dummies(test_data['surface_encoded'], prefix='surface')

    test_data = pd.concat([test_data, surface_encoded], axis=1)

    surface_columns = ['surface_Carpet', 'surface_Clay', 'surface_Grass', 'surface_Hard']
    for column in surface_columns:
        if column not in test_data.columns:
            test_data[column] = False

    feature_columns = ['player1_id', 'player2_id', 'player1_rank_points', 'player2_rank_points'] + surface_columns

    test_features = test_data[feature_columns]

    try:
        test_probabilities = model.predict_proba(test_features)

        player1_win_probability = float(test_probabilities[0, 1])
        player2_win_probability = float(test_probabilities[0, 0])
        
        player1_win_probability = round(player1_win_probability * 100, 2)
        player2_win_probability = round(player2_win_probability * 100, 2)

        return player1_win_probability, player2_win_probability

    except Exception as e:
        print("Error:", str(e))
        return None, None
    
def predict_by_rank_gb(player1_id, player2_id, player1_rank_points, player2_rank_points, surface):
    model_filename = 'tennis_model_trained_with_surface_gb.joblib'
    model = joblib.load(model_filename)

    surface = surface.capitalize()

    test_data = pd.DataFrame({
        'player1_id': [player1_id],
        'player2_id': [player2_id],
        'player1_rank_points': [player1_rank_points],
        'player2_rank_points': [player2_rank_points],
        'surface': [surface]
    })

    surface_encoder = LabelEncoder()
    test_data['surface_encoded'] = surface_encoder.fit_transform(test_data['surface'])
    surface_encoded = pd.get_dummies(test_data['surface_encoded'], prefix='surface')

    test_data = pd.concat([test_data, surface_encoded], axis=1)

    surface_columns = ['surface_Carpet', 'surface_Clay', 'surface_Grass', 'surface_Hard']
    for column in surface_columns:
        if column not in test_data.columns:
            test_data[column] = False

    feature_columns = ['player1_id', 'player2_id', 'player1_rank_points', 'player2_rank_points'] + surface_columns

    test_features = test_data[feature_columns]

    try:
        test_probabilities = model.predict_proba(test_features)

        player1_win_probability = float(test_probabilities[0, 1])
        player2_win_probability = float(test_probabilities[0, 0])
        
        player1_win_probability = round(player1_win_probability * 100, 2)
        player2_win_probability = round(player2_win_probability * 100, 2)

        return player1_win_probability, player2_win_probability

    except Exception as e:
        print("Error:", str(e))
        return None, None
    
    
'''model_filename = 'tennis_model_trained_with_surface_gb.joblib'
model = joblib.load(model_filename)
test_data = pd.read_csv('./matches_containing_glicko/balanced_matches_2023.csv')
surface_encoder = LabelEncoder()
test_data['surface_encoded'] = surface_encoder.fit_transform(test_data['surface'])
surface_encoded = pd.get_dummies(test_data['surface_encoded'], prefix='surface')
test_data = pd.concat([test_data, surface_encoded], axis=1)
surface_columns = ['surface_Carpet', 'surface_Clay', 'surface_Grass', 'surface_Hard']
for column in surface_columns:
    if column not in test_data.columns:
        test_data[column] = False
feature_columns = ['player1_id', 'player2_id', 'player1_rank_points', 'player2_rank_points'] + surface_columns
X_test = test_data[feature_columns]
y_test = test_data['winner'].apply(lambda x: 1 if x == 'player1' else 0)
X_test = X_test.fillna(0)
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Test Accuracy: {accuracy * 100:.2f}%")'''
