# Duplicate Check

def find_duplicates(df):
    dupes = df[df.duplicated(subset=['date', 'amount'], keep=False)].copy()
    dupes['flag_reason'] = 'Duplicate: same date & amount'
    return dupes

# Policy Filter

POLICY_LIMITS = {
    'meals': 25,
    'entertainment': 50,
    'travel': 200,
    'accommodation': 150,
    'office_supplies': 75,
}

def check_policy(df):
    df['category_lower'] = df['category'].str.lower()
    flagged = []
    for category, limit in POLICY_LIMITS.items():
        mask = (df['category_lower'] == category) & (df['amount'] > limit)
        subset = df[mask].copy()
        subset['flag_reason'] = f'Policy breach: {category} limit £{limit}'
        flagged.append(subset)
    return pd.concat(flagged) if flagged else pd.DataFrame()

  
# Anomaly Detection (Isolation Forest)
from sklearn.ensemble import IsolationForest
import numpy as np

def detect_anomalies(df, contamination=0.05):
    features = df[['amount', 'hour', 'day_of_week']].fillna(0)
    model = IsolationForest(contamination=contamination, random_state=42)
    df['anomaly_score'] = model.fit_predict(features)
    anomalies = df[df['anomaly_score'] == -1].copy()
    anomalies['flag_reason'] = 'AI anomaly: unusual pattern'
    return anomalies
