import pandas as pd

def load_and_clean(filepath):
    df = pd.read_csv(filepath)

    # Standardize column names
    df.columns = df.columns.str.lower().str.strip()

    # Convert transaction datetime
    df['trans_date_trans_time'] = pd.to_datetime(df['trans_date_trans_time'])

    # Extract useful features
    df['hour'] = df['trans_date_trans_time'].dt.hour
    df['day_of_week'] = df['trans_date_trans_time'].dt.dayofweek

    # Rename for consistency
    df.rename(columns={
        'amt': 'amount'
    }, inplace=True)

    # Ensure amount is valid
    df = df.dropna(subset=['amount'])
    df['amount'] = df['amount'].abs()

    return df
