import os
import django
import pandas as pd

# ✅ Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from fraudml.models import Transaction
from fraudml.ml_model import predict_fraud_scores
from django.utils.dateparse import parse_datetime

# ✅ Path to your CSV file
csv_path = r"E:\Fraud_detector\backend\fraud_model\sample_transaction.csv"

if not os.path.exists(csv_path):
    print(f"❌ CSV not found at: {csv_path}")
    exit()

# ✅ Load CSV
df = pd.read_csv(csv_path)

# ✅ Generate fraud score
try:
    fraud_scores = predict_fraud_scores(df)
    df['fraud_probability'] = fraud_scores
except Exception as e:
    print("❌ Error running ML model:", str(e))
    exit()

# ✅ Save to DB
created = 0
for _, row in df.iterrows():
    try:
        Transaction.objects.create(
            order_id=row['order_id'],
            customer_id=row['customer_id'],
            amount=row['amount'],
            payment_method=row['payment_method'],
            timestamp=parse_datetime(str(row['timestamp'])),
            device=row['device'],
            location=row['location'],
            fraud_probability=row['fraud_probability']
        )
        created += 1
    except Exception as e:
        print(f"⚠️ Skipping row: {e}")

print(f"✅ {created} transactions inserted successfully.")
