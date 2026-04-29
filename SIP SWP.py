# mutual_fund_calculator_app.py
# Run with: streamlit run mutual_fund_calculator_app.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Mutual Fund SIP & SWP Calculator", layout="wide")

st.title("💰 Mutual Fund SIP & SWP Calculator")
st.markdown("Plan your investments with SIP, Step-Up SIP, SWP & Gauge Chart")

# Sidebar Inputs
st.sidebar.header("📌 Input Details")

calc_type = st.sidebar.selectbox(
    "Choose Calculator",
    ["SIP Calculator", "SWP Calculator"]
)

annual_return = st.sidebar.slider("Expected Annual Return (%)", 1.0, 30.0, 12.0, step=0.1)
monthly_rate = annual_return / 12 / 100

years = st.sidebar.slider("Investment Duration (Years)", 1, 40, 10, step=1)

# ---------------- SIP CALCULATOR ---------------- #
if calc_type == "SIP Calculator":

    monthly_sip = st.sidebar.number_input("Monthly SIP Amount (₹)", 500, 1000000, 5000,step=100)
    step_up = st.sidebar.slider("Annual Step-Up (%)", 0, 50, 10, step=1)

    months = years * 12
    balance = 0
    invested = 0
    records = []

    current_sip = monthly_sip

    for month in range(1, months + 1):
        if month % 12 == 1 and month != 1:
            current_sip *= (1 + step_up / 100)

        balance = (balance + current_sip) * (1 + monthly_rate)
        invested += current_sip

        records.append([month, invested, balance])

    df = pd.DataFrame(records, columns=["Month", "Invested", "Value"])

    wealth = balance
    gain = wealth - invested

    # Results
    col1, col2, col3 = st.columns(3)

    col1.metric("💵 Total Invested", f"₹{invested:,.0f}")
    col2.metric("📈 Wealth Gained", f"₹{gain:,.0f}")
    col3.metric("🏆 Final Value", f"₹{wealth:,.0f}")

    # Gauge Chart
    goal = invested * 2

    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=wealth,
        title={'text': "Portfolio Growth"},
        gauge={
            'axis': {'range': [0, goal]},
            'bar': {'thickness': 0.3},
            'steps': [
                {'range': [0, invested], 'color': "lightgray"},
                {'range': [invested, goal], 'color': "lightgreen"},
            ],
        }
    ))

    st.plotly_chart(fig_gauge, use_container_width=True)

    # Growth Chart
    fig = px.line(df, x="Month", y=["Invested", "Value"],
                  title="SIP Growth Over Time")
    st.plotly_chart(fig, use_container_width=True)

# ---------------- SWP CALCULATOR ---------------- #
else:

    corpus = st.sidebar.number_input("Initial Corpus (₹)", 100000, 100000000, 1000000,step=100)
    monthly_withdrawal = st.sidebar.number_input("Monthly Withdrawal (₹)", 1000, 1000000, 10000,step=100)

    months = years * 12
    balance = corpus
    records = []

    for month in range(1, months + 1):
        balance = balance * (1 + monthly_rate)
        balance -= monthly_withdrawal

        if balance < 0:
            balance = 0

        records.append([month, balance])

        if balance == 0:
            break

    df = pd.DataFrame(records, columns=["Month", "Balance"])

    final_balance = balance

    col1, col2 = st.columns(2)
    col1.metric("🏦 Initial Corpus", f"₹{corpus:,.0f}")
    col2.metric("💰 Remaining Balance", f"₹{final_balance:,.0f}")

    # Gauge Chart
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=final_balance,
        title={'text': "Remaining Corpus"},
        gauge={
            'axis': {'range': [0, corpus]},
            'bar': {'thickness': 0.3},
            'steps': [
                {'range': [0, corpus*0.4], 'color': "red"},
                {'range': [corpus*0.4, corpus*0.7], 'color': "orange"},
                {'range': [corpus*0.7, corpus], 'color': "green"},
            ],
        }
    ))

    st.plotly_chart(fig_gauge, use_container_width=True)

    # Balance Chart
    fig = px.line(df, x="Month", y="Balance",
                  title="SWP Balance Over Time")
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.caption("Created with Python + Streamlit + Plotly")