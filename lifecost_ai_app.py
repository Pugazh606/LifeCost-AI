import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(page_title="LifeCost AI", page_icon="💰", layout="wide")

# -----------------------------
# Custom CSS for Premium Design
# -----------------------------
st.markdown("""
    <style>
    .main {
        background-color: #f5f7fa;
    }

    .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }

    .header-box {
        background: linear-gradient(135deg, #1f4e79, #4facfe);
        padding: 25px;
        border-radius: 18px;
        color: white;
        text-align: center;
        box-shadow: 0px 6px 18px rgba(0,0,0,0.15);
        margin-bottom: 20px;
    }

    .metric-card {
        background-color: white;
        padding: 18px;
        border-radius: 16px;
        box-shadow: 0px 4px 14px rgba(0,0,0,0.08);
        text-align: center;
        margin-bottom: 15px;
    }

    .section-box {
        background-color: white;
        padding: 20px;
        border-radius: 18px;
        box-shadow: 0px 4px 14px rgba(0,0,0,0.08);
        margin-bottom: 20px;
    }

    .recommend-box {
        background: #eef7ff;
        padding: 15px;
        border-left: 6px solid #4facfe;
        border-radius: 10px;
        margin-bottom: 10px;
        font-size: 16px;
    }

    .small-note {
        font-size: 14px;
        color: #555;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------
# Currency Options
# -----------------------------
currency_options = {
    "INR (₹)": "₹",
    "USD ($)": "$",
    "EUR (€)": "€",
    "GBP (£)": "£",
    "JPY (¥)": "¥",
    "AED (د.إ)": "د.إ",
    "SGD (S$)": "S$",
    "AUD (A$)": "A$",
    "CAD (C$)": "C$",
    "CNY (¥)": "¥"
}

# -----------------------------
# Helper Functions
# -----------------------------
def calculate_budget_health_score(income, total_expense, savings, emi, entertainment):
    savings_ratio = savings / income if income > 0 else 0
    expense_ratio = total_expense / income if income > 0 else 1
    emi_ratio = emi / income if income > 0 else 0
    entertainment_ratio = entertainment / income if income > 0 else 0

    score = 100

    # Savings score
    if savings_ratio >= 0.30:
        score += 0
    elif savings_ratio >= 0.20:
        score -= 5
    elif savings_ratio >= 0.10:
        score -= 15
    else:
        score -= 30

    # Expense burden
    if expense_ratio > 0.90:
        score -= 25
    elif expense_ratio > 0.80:
        score -= 15
    elif expense_ratio > 0.70:
        score -= 8

    # EMI burden
    if emi_ratio > 0.30:
        score -= 20
    elif emi_ratio > 0.20:
        score -= 10
    elif emi_ratio > 0.10:
        score -= 5

    # Entertainment burden
    if entertainment_ratio > 0.10:
        score -= 10
    elif entertainment_ratio > 0.07:
        score -= 5

    return max(0, min(100, score))

def generate_recommendations(income, savings, total_expense, emi, entertainment, food, rent):
    recommendations = []
    savings_ratio = savings / income if income > 0 else 0
    emi_ratio = emi / income if income > 0 else 0
    entertainment_ratio = entertainment / income if income > 0 else 0
    food_ratio = food / income if income > 0 else 0
    rent_ratio = rent / income if income > 0 else 0

    if savings_ratio < 0.20:
        recommendations.append("Increase your monthly savings target to at least 20% of your income.")
    if emi_ratio > 0.25:
        recommendations.append("Your EMI burden is high. Consider reducing or restructuring loans.")
    if entertainment_ratio > 0.08:
        recommendations.append("Entertainment spending is relatively high. Optimize non-essential expenses.")
    if food_ratio > 0.20:
        recommendations.append("Food expenses are high. Review grocery and dining habits.")
    if rent_ratio > 0.35:
        recommendations.append("Rent is above the recommended limit. Consider affordable housing options.")
    if total_expense > income:
        recommendations.append("Your expenses exceed your income. Immediate cost control is necessary.")
    if not recommendations:
        recommendations.append("Your budget looks healthy. Maintain this discipline and continue saving.")

    return recommendations

def forecast_expenses(total_expense, inflation_rate, months=12):
    forecast = []
    for month in range(1, months + 1):
        future_expense = total_expense * ((1 + inflation_rate / 12) ** month)
        forecast.append([month, future_expense])
    return pd.DataFrame(forecast, columns=["Month", "Forecasted Expense"])

def get_financial_status(score):
    if score >= 80:
        return "Excellent ✅"
    elif score >= 65:
        return "Good 👍"
    elif score >= 50:
        return "Moderate ⚠️"
    else:
        return "Risky ❌"

# -----------------------------
# Sidebar Inputs
# -----------------------------
st.sidebar.title("⚙️ LifeCost AI Settings")

currency_label = st.sidebar.selectbox("Select Currency", list(currency_options.keys()))
currency_symbol = currency_options[currency_label]

name = st.sidebar.text_input("Name", "Pugazh")
income = st.sidebar.number_input(f"Monthly Income ({currency_symbol})", min_value=0.0, value=45000.0, step=1000.0)
rent = st.sidebar.number_input(f"Rent ({currency_symbol})", min_value=0.0, value=12000.0, step=500.0)
food = st.sidebar.number_input(f"Food ({currency_symbol})", min_value=0.0, value=7000.0, step=500.0)
transport = st.sidebar.number_input(f"Transport ({currency_symbol})", min_value=0.0, value=3000.0, step=500.0)
healthcare = st.sidebar.number_input(f"Healthcare ({currency_symbol})", min_value=0.0, value=2000.0, step=500.0)
emi = st.sidebar.number_input(f"EMI / Loans ({currency_symbol})", min_value=0.0, value=5000.0, step=500.0)
education = st.sidebar.number_input(f"Education ({currency_symbol})", min_value=0.0, value=2500.0, step=500.0)
utilities = st.sidebar.number_input(f"Utilities ({currency_symbol})", min_value=0.0, value=2500.0, step=500.0)
entertainment = st.sidebar.number_input(f"Entertainment ({currency_symbol})", min_value=0.0, value=2000.0, step=500.0)
other_expenses = st.sidebar.number_input(f"Other Expenses ({currency_symbol})", min_value=0.0, value=1500.0, step=500.0)
inflation_rate = st.sidebar.slider("Annual Inflation Rate", min_value=0.0, max_value=0.20, value=0.06, step=0.01)

st.sidebar.markdown("---")
st.sidebar.subheader("🔮 What-If Simulation")
whatif_income_change = st.sidebar.slider("Income Change (%)", -50, 50, 0)
whatif_expense_change = st.sidebar.slider("Expense Change (%)", -50, 50, 0)
whatif_inflation_change = st.sidebar.slider("Inflation Change (%)", -10, 10, 0)

# -----------------------------
# Apply What-If
# -----------------------------
adjusted_income = income * (1 + whatif_income_change / 100)

expense_items = [rent, food, transport, healthcare, emi, education, utilities, entertainment, other_expenses]
adjusted_expense_items = [x * (1 + whatif_expense_change / 100) for x in expense_items]
adjusted_inflation = max(0, inflation_rate + (whatif_inflation_change / 100))

categories = ["Rent", "Food", "Transport", "Healthcare", "EMI", "Education", "Utilities", "Entertainment", "Other Expenses"]
total_expense = sum(adjusted_expense_items)
savings = adjusted_income - total_expense
savings_ratio = (savings / adjusted_income) * 100 if adjusted_income > 0 else 0

essential_expense = adjusted_expense_items[0] + adjusted_expense_items[1] + adjusted_expense_items[2] + adjusted_expense_items[3] + adjusted_expense_items[6]
min_emergency_fund = essential_expense * 3
ideal_emergency_fund = essential_expense * 6

budget_score = calculate_budget_health_score(adjusted_income, total_expense, savings, adjusted_expense_items[4], adjusted_expense_items[7])
financial_status = get_financial_status(budget_score)

recommendations = generate_recommendations(
    adjusted_income, savings, total_expense,
    adjusted_expense_items[4], adjusted_expense_items[7],
    adjusted_expense_items[1], adjusted_expense_items[0]
)

forecast_df = forecast_expenses(total_expense, adjusted_inflation, months=12)

expense_df = pd.DataFrame({
    "Category": categories,
    "Amount": adjusted_expense_items
})

# -----------------------------
# Header
# -----------------------------
st.markdown(f"""
    <div class="header-box">
        <h1>💰 LifeCost AI</h1>
        <h3>Smart Personal Inflation & Budget Decision Support System</h3>
        <p>Welcome, <b>{name}</b> | Global Financial Planning Dashboard 🌍</p>
    </div>
""", unsafe_allow_html=True)

# -----------------------------
# KPI Metrics
# -----------------------------
st.markdown("## 📌 Key Financial Overview")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f'<div class="metric-card"><h4>Income</h4><h2>{currency_symbol}{adjusted_income:,.2f}</h2></div>', unsafe_allow_html=True)

with col2:
    st.markdown(f'<div class="metric-card"><h4>Total Expense</h4><h2>{currency_symbol}{total_expense:,.2f}</h2></div>', unsafe_allow_html=True)

with col3:
    st.markdown(f'<div class="metric-card"><h4>Monthly Savings</h4><h2>{currency_symbol}{savings:,.2f}</h2></div>', unsafe_allow_html=True)

with col4:
    st.markdown(f'<div class="metric-card"><h4>Savings Ratio</h4><h2>{savings_ratio:.2f}%</h2></div>', unsafe_allow_html=True)

# -----------------------------
# Score + Status
# -----------------------------
st.markdown("## 📊 Budget Health Score & Financial Status")
col5, col6 = st.columns([1, 1])

with col5:
    score_color = "green" if budget_score >= 75 else "orange" if budget_score >= 50 else "red"
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=budget_score,
        title={'text': "Budget Health Score"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': score_color},
            'steps': [
                {'range': [0, 50], 'color': "#ffcccc"},
                {'range': [50, 75], 'color': "#fff3cd"},
                {'range': [75, 100], 'color': "#d4edda"}
            ]
        }
    ))
    st.plotly_chart(fig_gauge, use_container_width=True)

with col6:
    st.markdown(f"""
        <div class="section-box">
            <h3>📍 Financial Status</h3>
            <h2>{financial_status}</h2>
            <p class="small-note">This status is based on your savings ratio, EMI burden, and overall expense behavior.</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div class="section-box">
            <h3>🚨 Emergency Fund Recommendation</h3>
            <p><b>Minimum (3 Months):</b> {currency_symbol}{min_emergency_fund:,.2f}</p>
            <p><b>Ideal (6 Months):</b> {currency_symbol}{ideal_emergency_fund:,.2f}</p>
        </div>
    """, unsafe_allow_html=True)

# -----------------------------
# Expense Analysis Charts
# -----------------------------
st.markdown("## 📈 Expense Analysis Dashboard")

col7, col8 = st.columns(2)

with col7:
    fig_pie = px.pie(expense_df, names="Category", values="Amount", hole=0.4, title="Expense Distribution (Donut Chart)")
    st.plotly_chart(fig_pie, use_container_width=True)

with col8:
    fig_bar = px.bar(expense_df, x="Category", y="Amount", title="Category-wise Expense Comparison", text_auto=".2s")
    fig_bar.update_layout(xaxis_tickangle=-30)
    st.plotly_chart(fig_bar, use_container_width=True)

# -----------------------------
# Savings vs Expense
# -----------------------------
st.markdown("## 💸 Savings vs Expenses")

savings_expense_df = pd.DataFrame({
    "Type": ["Expenses", "Savings"],
    "Amount": [total_expense, max(savings, 0)]
})

col9, col10 = st.columns(2)

with col9:
    fig_donut = px.pie(
        savings_expense_df,
        names="Type",
        values="Amount",
        hole=0.5,
        title="Savings vs Expenses"
    )
    st.plotly_chart(fig_donut, use_container_width=True)

with col10:
    current_vs_future = pd.DataFrame({
        "Scenario": ["Current Monthly Expense", "Projected 12th Month Expense"],
        "Amount": [total_expense, forecast_df.iloc[-1]["Forecasted Expense"]]
    })
    fig_compare = px.bar(current_vs_future, x="Scenario", y="Amount", title="Current vs Future Expense Comparison", text_auto=".2s")
    st.plotly_chart(fig_compare, use_container_width=True)

# -----------------------------
# Radar Chart
# -----------------------------
st.markdown("## 🕸️ Spending Pattern Radar Chart")

fig_radar = go.Figure()
fig_radar.add_trace(go.Scatterpolar(
    r=adjusted_expense_items,
    theta=categories,
    fill='toself',
    name='Spending Pattern'
))
fig_radar.update_layout(
    polar=dict(radialaxis=dict(visible=True)),
    showlegend=False,
    title="Spending Pattern Across Categories"
)
st.plotly_chart(fig_radar, use_container_width=True)

# -----------------------------
# Forecast Chart
# -----------------------------
st.markdown("## 📅 12-Month Inflation-Based Forecast")

fig_line = px.line(
    forecast_df,
    x="Month",
    y="Forecasted Expense",
    markers=True,
    title="Projected Monthly Expenses Over the Next 12 Months"
)
st.plotly_chart(fig_line, use_container_width=True)

# -----------------------------
# Forecast Table
# -----------------------------
st.markdown("## 📋 Forecast Table")
st.dataframe(forecast_df, use_container_width=True)

# -----------------------------
# Smart Recommendations
# -----------------------------
st.markdown("## 🤖 Smart Recommendations")
for i, rec in enumerate(recommendations, 1):
    st.markdown(f'<div class="recommend-box"><b>{i}.</b> {rec}</div>', unsafe_allow_html=True)

# -----------------------------
# Financial Summary
# -----------------------------
st.markdown("## 📝 Financial Summary")
st.markdown(f"""
<div class="section-box">
<b>User Name:</b> {name}<br>
<b>Selected Currency:</b> {currency_label}<br>
<b>Adjusted Monthly Income:</b> {currency_symbol}{adjusted_income:,.2f}<br>
<b>Total Monthly Expense:</b> {currency_symbol}{total_expense:,.2f}<br>
<b>Monthly Savings:</b> {currency_symbol}{savings:,.2f}<br>
<b>Savings Ratio:</b> {savings_ratio:.2f}%<br>
<b>Budget Health Score:</b> {budget_score}/100<br>
<b>Financial Status:</b> {financial_status}<br>
<b>Minimum Emergency Fund:</b> {currency_symbol}{min_emergency_fund:,.2f}<br>
<b>Ideal Emergency Fund:</b> {currency_symbol}{ideal_emergency_fund:,.2f}<br>
<b>Applied Annual Inflation Rate:</b> {adjusted_inflation * 100:.2f}%<br>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# Optional Dataset Upload
# -----------------------------
st.markdown("## 📂 Optional Dataset Viewer")
uploaded_file = st.file_uploader("Upload an Excel file (optional)", type=["xlsx"])

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file)
        st.success("Excel file uploaded successfully!")
        st.dataframe(df, use_container_width=True)
    except Exception as e:
        st.error(f"Error reading file: {e}")