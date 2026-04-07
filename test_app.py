import streamlit as st

st.set_page_config(page_title="LifeCost Test", layout="wide")

st.title("✅ Streamlit is working")
st.write("If you can see this, the app is not broken.")
st.selectbox("Currency", ["INR", "USD", "EUR"])