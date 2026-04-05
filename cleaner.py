import pandas as pd

def load_and_clean(filepath):
    df = pd.read_csv(filepath)
    
    # Standardise column names (lowercase, no spaces)
    df.columns = df.columns.str.lower().str.replace(' ', '_')
    
    # Parse dates properly
    df['date'] = pd.to_datetime(df['date'])
    
    # Extract hour and day-of-week for anomaly detection later
    df['hour'] = df['date'].dt.hour
    df['day_of_week'] = df['date'].dt.dayofweek  # 0=Mon, 6=Sun
    
    # Drop rows with no amount
    df = df.dropna(subset=['amount'])
    df['amount'] = df['amount'].abs()  # ensure positive
    
    return df
