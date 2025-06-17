import pandas as pd
import xgboost as xgb
import joblib
import numpy as np

# Simulated data
np.random.seed(42)
N = 300

data = {
    'amount': np.random.uniform(10, 5000, N),
    'payment_method': np.random.choice(['card', 'cash', 'upi'], N),
    'device': np.random.choice(['mobile', 'desktop'], N),
    'location': np.random.choice(['delhi', 'mumbai', 'kolkata'], N)
}

df = pd.DataFrame(data)

# ✨ Inject fraud pattern: high amount + cash on desktop → label = 1
df['label'] = 0
df.loc[(df['amount'] > 4000) & (df['payment_method'] == 'cash') & (df['device'] == 'desktop'), 'label'] = 1
df.loc[(df['amount'] < 50) & (df['location'] == 'delhi'), 'label'] = 1  # Another fraud pattern

# Encode + train
X = pd.get_dummies(df[['amount', 'payment_method', 'device', 'location']])
y = df['label']

model = xgb.XGBClassifier(use_label_encoder=False, eval_metric='logloss')
model.fit(X, y)

# Save model
joblib.dump(model, "fraud_model/model.pkl")
print("✅ Improved model saved to fraud_model/model.pkl")
