import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.metrics import accuracy_score, classification_report
import joblib

data = pd.concat([pd.read_csv(f'matches_containing_glicko/updated_matches_{year}.csv') for year in range(2010, 2023)])

data['winner'] = data['winner'].apply(lambda x: 1 if x == 'player1' else 0)

surface_encoded = pd.get_dummies(data['surface'], prefix='surface')
data_combined = pd.concat([data, surface_encoded], axis=1)

feature_columns = ['player1_id', 'player2_id', 'player_1_glicko', 'player_2_glicko'] + list(surface_encoded.columns)
X = data_combined[feature_columns]
y = data['winner']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

param_dist = {
    'n_estimators': [50, 100, 200],
    'max_depth': [None, 10, 20, 30],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4],
    'max_features': ['auto', 'sqrt', 'log2'],
}

rf = RandomForestClassifier(random_state=42)
rf_random = RandomizedSearchCV(estimator=rf, param_distributions=param_dist, n_iter=100, cv=5, verbose=2, random_state=42, n_jobs=-1)
rf_random.fit(X_train, y_train)

best_params = rf_random.best_params_
print("Best Hyperparameters:", best_params)

best_model = RandomForestClassifier(random_state=42, **best_params)
best_model.fit(X_train, y_train)

y_pred = best_model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
classification_rep = classification_report(y_test, y_pred)

print(f"Accuracy: {accuracy:.2f}")
print("Classification Report:\n", classification_rep)

model_filename = 'model/tennis_model_trained_hyperparameter_tuned_glicko_with_surface.joblib'
joblib.dump(best_model, model_filename)

print(f"Model saved to {model_filename}")
