# train_model.py

import pandas as pd
import pickle
import os

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier
from xgboost import XGBClassifier
from sklearn.metrics import classification_report
from imblearn.over_sampling import SMOTE
from sklearn.pipeline import Pipeline

def train_and_save_model(data_path="ml_model/data/tech_jobs.csv", model_path="ml_model/final_ensemble_model.pkl"):
    # Load dataset
    df = pd.read_csv(data_path)

    # Feature and target selection
    features = ['Rating', 'Salary']
    target = 'Job Roles'

    X = df[features]
    y = df[target]

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Handle imbalance
    smote = SMOTE(random_state=42)
    X_resampled, y_resampled = smote.fit_resample(X_train, y_train)

    # Models
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    gb = GradientBoostingClassifier(n_estimators=100, random_state=42)
    xgb = XGBClassifier(eval_metric='mlogloss', random_state=42)

    # Ensemble Voting Classifier
    voting_clf = VotingClassifier(
        estimators=[('rf', rf), ('gb', gb), ('xgb', xgb)],
        voting='soft'
    )

    # Pipeline
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('classifier', voting_clf)
    ])

    # Train
    pipeline.fit(X_resampled, y_resampled)

    # Evaluate
    y_pred = pipeline.predict(X_test)
    print("\nClassification Report:\n")
    print(classification_report(y_test, y_pred))

    # Save model
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    with open(model_path, "wb") as f:
        pickle.dump(pipeline, f)
    print(f"\n✅ Model saved to '{model_path}'")

# Run when script is executed directly
if __name__ == "__main__":
    train_and_save_model()
