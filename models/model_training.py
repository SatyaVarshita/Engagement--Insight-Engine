import json
import pickle
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

def load_training_data(file_path="data/training_data.json"):
    """Load training data from JSON file."""
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

def prepare_features_and_labels(data):
    """Extract features and labels from training data."""
    features = []
    resume_labels = []
    project_labels = []
    event_labels = []
    
    for sample in data:
        # Extract features
        feature_dict = sample["features"]
        feature_vector = [
            1 if feature_dict["resume_uploaded"] else 0,
            feature_dict["karma"],
            feature_dict["projects_added"],
            feature_dict["batch_avg_projects"],
            feature_dict["batch_resume_uploaded_pct"],
            feature_dict["event_fomo_score"]
        ]
        features.append(feature_vector)
        
        # Extract labels
        label_dict = sample["label"]
        resume_labels.append(label_dict["should_nudge_resume"])
        project_labels.append(label_dict["should_nudge_project"])
        event_labels.append(label_dict["should_nudge_event"])
    
    return np.array(features), np.array(resume_labels), np.array(project_labels), np.array(event_labels)

def train_models():
    """Train and save nudge prediction models."""
    # Load training data
    data = load_training_data()
    
    # Prepare features and labels
    X, y_resume, y_project, y_event = prepare_features_and_labels(data)
    
    # Split data into training and testing sets
    X_train, X_test, y_resume_train, y_resume_test = train_test_split(X, y_resume, test_size=0.2, random_state=42)
    _, _, y_project_train, y_project_test = train_test_split(X, y_project, test_size=0.2, random_state=42)
    _, _, y_event_train, y_event_test = train_test_split(X, y_event, test_size=0.2, random_state=42)
    
    # Train resume nudge model
    resume_model = RandomForestClassifier(n_estimators=100, random_state=42)
    resume_model.fit(X_train, y_resume_train)
    
    # Train project nudge model
    project_model = RandomForestClassifier(n_estimators=100, random_state=42)
    project_model.fit(X_train, y_project_train)
    
    # Train event nudge model
    event_model = RandomForestClassifier(n_estimators=100, random_state=42)
    event_model.fit(X_train, y_event_train)
    
    # Evaluate models
    print("Resume Nudge Model Performance:")
    y_resume_pred = resume_model.predict(X_test)
    print(classification_report(y_resume_test, y_resume_pred))
    
    print("Project Nudge Model Performance:")
    y_project_pred = project_model.predict(X_test)
    print(classification_report(y_project_test, y_project_pred))
    
    print("Event Nudge Model Performance:")
    y_event_pred = event_model.predict(X_test)
    print(classification_report(y_event_test, y_event_pred))
    
    # Save models
    models = {
        "resume_model": resume_model,
        "project_model": project_model,
        "event_model": event_model,
        "feature_names": ["resume_uploaded", "karma", "projects_added", 
                         "batch_avg_projects", "batch_resume_uploaded_pct", "event_fomo_score"]
    }
    
    with open("models/nudge_models.pkl", "wb") as f:
        pickle.dump(models, f)
    
    print("Models trained and saved to models/nudge_models.pkl")

if __name__ == "__main__":
    train_models()
    