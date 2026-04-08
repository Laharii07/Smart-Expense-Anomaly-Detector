import streamlit as st
from cleaner import load_and_clean
from report import build_report
import io

st.set_page_config(page_title="Fraud Detection App", layout="wide")
st.title("💳 Credit Card Fraud Detection System")

uploaded = st.file_uploader("Upload fraudTest.csv", type=["csv"])

if uploaded:
    df = load_and_clean(uploaded)

    st.success(f"Loaded {len(df)} transactions")

    flagged = build_report(df)

    st.subheader(f"🚨 Flagged Transactions: {len(flagged)}")
    st.dataframe(flagged, use_container_width=True)

    # Download
    output = io.BytesIO()
    flagged.to_excel(output, index=False)

    st.download_button(
        "Download Report",
        data=output.getvalue(),
        file_name="fraud_report.xlsx"
    )
