import pandas as pd
import xgboost as xgb
import joblib

# Load trained model
model = joblib.load("fraud_model/model.pkl")

def predict_fraud_scores(df):
    features = ['amount', 'payment_method', 'device', 'location']
    df_encoded = pd.get_dummies(df[features])

    # Align with training features
    model_features = model.get_booster().feature_names
    for col in model_features:
        if col not in df_encoded:
            df_encoded[col] = 0
    df_encoded = df_encoded[model_features]

    preds = model.predict_proba(df_encoded)[:, 1]
    return preds
