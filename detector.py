# Duplicate Check

def find_duplicates(df):
    dupes = df[df.duplicated(subset=['trans_date_trans_time', 'amount', 'cc_num'], keep=False)].copy()
    dupes['flag_reason'] = 'Duplicate transaction (same time, amount, card)'
    return dupes

# Policy Filter

POLICY_LIMITS = {
    'personal_care': 30,
    'health_fitness': 50,
    'misc_pos': 100,
}

def check_policy(df):
    df['category_lower'] = df['category'].str.lower()
    flagged = []

    for category, limit in POLICY_LIMITS.items():
        mask = (df['category_lower'] == category) & (df['amount'] > limit)
        subset = df[mask].copy()
        subset['flag_reason'] = f'Policy breach: {category} > {limit}'
        flagged.append(subset)

    return pd.concat(flagged) if flagged else pd.DataFrame()
  
# Anomaly Detection (Isolation Forest)

from sklearn.ensemble import IsolationForest

def detect_anomalies(df, contamination=0.05):
    features = df[['amount', 'hour', 'day_of_week', 'city_pop']].fillna(0)

    model = IsolationForest(contamination=contamination, random_state=42)
    df['anomaly'] = model.fit_predict(features)

    anomalies = df[df['anomaly'] == -1].copy()
    anomalies['flag_reason'] = 'AI anomaly detected'

    return anomalies
# Checking Fraud

def actual_fraud(df):
    frauds = df[df['is_fraud'] == 1].copy()
    frauds['flag_reason'] = 'Actual Fraud (labelled)'
    return frauds
