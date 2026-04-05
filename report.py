def build_report(df):
    from detectors import find_duplicates, check_policy, detect_anomalies
    
    all_flags = pd.concat([
        find_duplicates(df),
        check_policy(df),
        detect_anomalies(df)
    ]).drop_duplicates()
    
    return all_flags[['date', 'amount', 'category', 'merchant', 'flag_reason']]
