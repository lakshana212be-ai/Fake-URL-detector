import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

def train_model():
    print("Loading dataset...")
    try:
        df = pd.read_csv("dataset.csv")
    except FileNotFoundError:
        print("dataset.csv not found. Please run data_generator.py first.")
        return
        
    # Features and labels
    feature_cols = [c for c in df.columns if c not in ['url', 'label']]
    X = df[feature_cols]
    y = df['label']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Training Random Forest model...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy: {accuracy * 100:.2f}%")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    # Save model
    print("Saving model to url_model.pkl...")
    joblib.dump(model, "url_model.pkl")
    print("Model saved successfully.")

if __name__ == "__main__":
    train_model()
