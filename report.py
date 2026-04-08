def build_report(df):
    from detectors import find_duplicates, check_policy, detect_anomalies, actual_fraud

    all_flags = pd.concat([
        find_duplicates(df),
        check_policy(df),
        detect_anomalies(df),
        actual_fraud(df)
    ]).drop_duplicates()

    return all_flags[[
        'trans_date_trans_time',
        'cc_num',
        'merchant',
        'category',
        'amount',
        'city',
        'state',
        'flag_reason'
    ]]
