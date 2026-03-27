import joblib
import pandas as pd
from feature_extractor import extract_features

model = joblib.load("url_model.pkl")
url = "http://google.com"
features = extract_features(url)
df_features = pd.DataFrame([features])
print("Columns in data:", df_features.columns)
print("Features in model:", model.feature_names_in_)

try:
    prediction = model.predict(df_features)[0]
    proba = model.predict_proba(df_features)[0]
    print(f"Prediction: {prediction}, Proba: {proba}")
except Exception as e:
    print(f"Error: {e}")
