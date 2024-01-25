import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
import joblib

data = pd.concat([pd.read_csv(f'matches_containing_glicko/balanced_matches_{year}.csv') for year in range(2010, 2023)])

data['winner'] = data['winner'].apply(lambda x: 1 if x == 'player1' else 0)

surface_encoded = pd.get_dummies(data['surface'], prefix='surface')

data_combined = pd.concat([data, surface_encoded], axis=1)

feature_columns = ['player1_id', 'player2_id', 'player_1_glicko', 'player_2_glicko'] + list(surface_encoded.columns)
X = data_combined[feature_columns]
y = data['winner']

model = GradientBoostingClassifier(n_estimators=100, random_state=42)
model.fit(X, y) 

model_filename = 'model/tennis_model_trained_glicko_with_surface_gb.joblib'
joblib.dump(model, model_filename)

print(f"Model saved to {model_filename}")
