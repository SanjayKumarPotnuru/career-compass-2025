import numpy as np
import pickle

# Load the VotingClassifier pipeline (already includes scaler and classifier)
with open("ml_model/final_ensemble_model.pkl", "rb") as f:
    model_pipeline = pickle.load(f)

def predict_jobs(expected_salary, rating=3.0, top_n=4):
    # Prepare input with [Rating, Salary] as expected by the model
    X_input = np.array([[rating, expected_salary]])

    # Predict class probabilities
    probabilities = model_pipeline.predict_proba(X_input)[0]

    # Get indices of top N job roles
    top_indices = probabilities.argsort()[::-1][:top_n]

    # Get class labels from the model
    job_roles = model_pipeline.named_steps['classifier'].classes_

    # Return top N job roles (normalized to uppercase for matching JSON keys)
    return [job_roles[i].upper() for i in top_indices]
