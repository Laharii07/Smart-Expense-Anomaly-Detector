import streamlit as st
import pandas as pd
from cleaner import load_and_clean
from report import build_report
import io

st.set_page_config(page_title="Expense Anomaly Detector", layout="wide")
st.title("Smart Expense & Anomaly Detector")

uploaded = st.file_uploader("Upload your Amex CSV", type=["csv"])

if uploaded:
    df = load_and_clean(uploaded)
    st.success(f"Loaded {len(df)} transactions")
    
    flagged = build_report(df)
    st.subheader(f"Flagged: {len(flagged)} issues found")
    st.dataframe(flagged, use_container_width=True)
    
    # Download button
    output = io.BytesIO()
    flagged.to_excel(output, index=False)
    st.download_button("Download Report (.xlsx)", 
                       data=output.getvalue(), 
                       file_name="flagged_expenses.xlsx")
