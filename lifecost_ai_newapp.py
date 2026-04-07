import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ==============================
# PAGE CONFIG
# ==============================
st.set_page_config(
    page_title="LifeCost AI - MBA Project",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================
# CUSTOM CSS
# ==============================
st.markdown("""
<style>
/* Main App Background */
.stApp {
    background: linear-gradient(135deg, #eef4ff 0%, #f5f0ff 35%, #eefaf6 100%);
    color: #111827;
    font-family: 'Segoe UI', sans-serif;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
    color: white;
}
[data-testid="stSidebar"] * {
    color: white !important;
}

/* Main container spacing */
.block-container {
    padding-top: 1.2rem;
    padding-bottom: 2rem;
}

/* Hero banner */
.hero-box {
    background: linear-gradient(135deg, #2563eb, #7c3aed);
    padding: 2rem;
    border-radius: 24px;
    color: white;
    box-shadow: 0 10px 30px rgba(37, 99, 235, 0.20);
    margin-bottom: 1.5rem;
}

/* Metric Cards */
.metric-card {
    background: rgba(255,255,255,0.85);
    backdrop-filter: blur(10px);
    border-radius: 18px;
    padding: 1.2rem;
    box-shadow: 0 8px 24px rgba(15, 23, 42, 0.08);
    border: 1px solid rgba(255,255,255,0.55);
    text-align: center;
    margin-bottom: 0.5rem;
}
.metric-title {
    font-size: 0.95rem;
    color: #475569;
    font-weight: 600;
}
.metric-value {
    font-size: 2rem;
    font-weight: 800;
    color: #111827;
    margin-top: 0.3rem;
}

/* Section Box */
.section-box {
    background: rgba(255,255,255,0.82);
    backdrop-filter: blur(12px);
    padding: 1.2rem;
    border-radius: 20px;
    box-shadow: 0 8px 24px rgba(15, 23, 42, 0.08);
    margin-top: 1rem;
    margin-bottom: 1rem;
    border: 1px solid rgba(255,255,255,0.5);
}

/* Headings */
h1, h2, h3 {
    color: #111827 !important;
}
</style>
""", unsafe_allow_html=True)

# ==============================
# CURRENCY CONFIG
# ==============================
currency_data = {
    "INR (₹)": {"rate": 1.0, "symbol": "₹"},
    "USD ($)": {"rate": 0.012, "symbol": "$"},
    "EUR (€)": {"rate": 0.011, "symbol": "€"},
    "GBP (£)": {"rate": 0.0095, "symbol": "£"},
    "JPY (¥)": {"rate": 1.80, "symbol": "¥"},
    "AED (د.إ)": {"rate": 0.044, "symbol": "د.إ"},
    "SGD (S$)": {"rate": 0.016, "symbol": "S$"}
}

# ==============================
# SIDEBAR
# ==============================
st.sidebar.markdown("## ⚙️ Input Controls")

name = st.sidebar.text_input("Enter Your Name", value="Pugazh")
selected_currency = st.sidebar.selectbox("🌍 Select Currency", list(currency_data.keys()))

monthly_income = st.sidebar.number_input("Monthly Income (Base in INR)", min_value=0.0, value=45000.0, step=1000.0)
food = st.sidebar.number_input("Food Expense (INR)", min_value=0.0, value=10000.0, step=500.0)
rent = st.sidebar.number_input("Rent Expense (INR)", min_value=0.0, value=15000.0, step=500.0)
transport = st.sidebar.number_input("Transport Expense (INR)", min_value=0.0, value=5000.0, step=500.0)
utilities = st.sidebar.number_input("Utilities Expense (INR)", min_value=0.0, value=3000.0, step=500.0)
entertainment = st.sidebar.number_input("Entertainment Expense (INR)", min_value=0.0, value=2500.0, step=500.0)
healthcare = st.sidebar.number_input("Healthcare Expense (INR)", min_value=0.0, value=2000.0, step=500.0)

inflation_rate = st.sidebar.slider("📈 Inflation Rate (%)", 0.0, 20.0, 6.0, 0.5)
income_change = st.sidebar.slider("💼 Expected Income Change (%)", -50, 100, 10)
expense_change = st.sidebar.slider("🧾 Expected Expense Change (%)", -50, 100, 8)

# ==============================
# OPTIONAL EXCEL UPLOAD (RESTORED)
# ==============================
st.sidebar.markdown("---")
st.sidebar.markdown("### 📂 Optional Dataset Viewer")
uploaded_file = st.sidebar.file_uploader("Upload an Excel file (optional)", type=["xlsx", "xls"])

uploaded_df = None
if uploaded_file is not None:
    try:
        uploaded_df = pd.read_excel(uploaded_file)
        st.sidebar.success("Excel file uploaded successfully!")
    except Exception as e:
        st.sidebar.error(f"Error reading file: {e}")

# ==============================
# CALCULATIONS
# ==============================
base_expenses = food + rent + transport + utilities + entertainment + healthcare

adjusted_income = monthly_income * (1 + income_change / 100)
adjusted_expenses = base_expenses * (1 + expense_change / 100)
monthly_savings = adjusted_income - adjusted_expenses
savings_ratio = (monthly_savings / adjusted_income * 100) if adjusted_income > 0 else 0

# Currency conversion
conversion_rate = currency_data[selected_currency]["rate"]
currency_symbol = currency_data[selected_currency]["symbol"]

display_income = adjusted_income * conversion_rate
display_expenses = adjusted_expenses * conversion_rate
display_savings = monthly_savings * conversion_rate

# Budget health score
if savings_ratio >= 30:
    budget_health = "Excellent"
    health_score = 90
elif savings_ratio >= 20:
    budget_health = "Good"
    health_score = 75
elif savings_ratio >= 10:
    budget_health = "Average"
    health_score = 55
elif savings_ratio >= 0:
    budget_health = "Risky"
    health_score = 35
else:
    budget_health = "Critical"
    health_score = 15

# Expense DataFrame
expense_data = pd.DataFrame({
    "Category": ["Food", "Rent", "Transport", "Utilities", "Entertainment", "Healthcare"],
    "Amount": [food, rent, transport, utilities, entertainment, healthcare]
})
expense_data["Converted Amount"] = expense_data["Amount"] * conversion_rate

# Forecast DataFrame
years = np.arange(1, 6)
projected_expenses = [adjusted_expenses * ((1 + inflation_rate / 100) ** y) for y in years]
forecast_df = pd.DataFrame({
    "Year": years,
    "Projected Expense": projected_expenses
})
forecast_df["Projected Expense Converted"] = forecast_df["Projected Expense"] * conversion_rate

# ==============================
# HERO SECTION
# ==============================
st.markdown(f"""
<div class="hero-box">
    <h1>💰 LifeCost AI</h1>
    <h3>A Python-Based Personal Inflation & Smart Budget Decision Support System</h3>
    <p style="font-size:1.15rem;">Professional MBA Project Dashboard for Global Budget Planning</p>
</div>
""", unsafe_allow_html=True)

st.markdown(f"# Welcome, {name}! 👋")

# ==============================
# KPI CARDS
# ==============================
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Adjusted Monthly Income</div>
        <div class="metric-value">{currency_symbol}{display_income:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Total Monthly Expense</div>
        <div class="metric-value">{currency_symbol}{display_expenses:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Monthly Savings</div>
        <div class="metric-value">{currency_symbol}{display_savings:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Savings Ratio</div>
        <div class="metric-value">{savings_ratio:.2f}%</div>
    </div>
    """, unsafe_allow_html=True)

# ==============================
# GAUGE CHART
# ==============================
st.markdown('<div class="section-box">', unsafe_allow_html=True)
st.subheader("🧭 Budget Health Score")

gauge = go.Figure(go.Indicator(
    mode="gauge+number",
    value=health_score,
    title={"text": f"Budget Health: {budget_health}"},
    gauge={
        "axis": {"range": [0, 100]},
        "bar": {"color": "#2563eb"},
        "steps": [
            {"range": [0, 25], "color": "#fee2e2"},
            {"range": [25, 50], "color": "#fef3c7"},
            {"range": [50, 75], "color": "#dbeafe"},
            {"range": [75, 100], "color": "#dcfce7"}
        ]
    }
))
gauge.update_layout(height=350)
st.plotly_chart(gauge, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ==============================
# DATA TABLE
# ==============================
st.markdown('<div class="section-box">', unsafe_allow_html=True)
st.subheader("📋 Expense Breakdown Table")
display_table = expense_data[["Category", "Converted Amount"]].copy()
display_table.columns = ["Category", f"Amount ({selected_currency})"]
st.dataframe(display_table, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ==============================
# OPTIONAL UPLOADED DATA PREVIEW
# ==============================
if uploaded_df is not None:
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.subheader("📂 Uploaded Excel Dataset Preview")
    st.dataframe(uploaded_df, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ==============================
# CHARTS ROW 1
# ==============================
colA, colB = st.columns(2)

with colA:
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.subheader("🍩 Expense Distribution (Donut Chart)")
    pie = px.pie(
        expense_data,
        names="Category",
        values="Converted Amount",
        hole=0.5,
        title="Expense Share by Category"
    )
    pie.update_layout(height=450)
    st.plotly_chart(pie, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with colB:
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.subheader("📊 Category-wise Expense Comparison")
    bar_chart = px.bar(
        expense_data,
        x="Category",
        y="Converted Amount",
        text="Converted Amount",
        title="Expense Amount by Category"
    )
    bar_chart.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    bar_chart.update_layout(height=450)
    st.plotly_chart(bar_chart, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ==============================
# CHARTS ROW 2
# ==============================
colC, colD = st.columns(2)

with colC:
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.subheader("📈 5-Year Inflation Forecast (Line Chart)")
    line = px.line(
        forecast_df,
        x="Year",
        y="Projected Expense Converted",
        markers=True,
        title="Projected Expense Growth Over 5 Years"
    )
    line.update_layout(height=450)
    st.plotly_chart(line, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with colD:
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.subheader("🌊 Cumulative Inflation Impact (Area Chart)")
    area = px.area(
        forecast_df,
        x="Year",
        y="Projected Expense Converted",
        title="Cumulative Expense Growth Due to Inflation"
    )
    area.update_layout(height=450)
    st.plotly_chart(area, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ==============================
# SCENARIO COMPARISON
# ==============================
st.markdown('<div class="section-box">', unsafe_allow_html=True)
st.subheader("⚖️ Current vs What-If Scenario Comparison")

current_savings = monthly_income - base_expenses

scenario_df = pd.DataFrame({
    "Metric": ["Income", "Expense", "Savings"],
    "Current": [
        monthly_income * conversion_rate,
        base_expenses * conversion_rate,
        current_savings * conversion_rate
    ],
    "What-If": [
        adjusted_income * conversion_rate,
        adjusted_expenses * conversion_rate,
        monthly_savings * conversion_rate
    ]
})

scenario_long = scenario_df.melt(id_vars="Metric", var_name="Scenario", value_name="Amount")

grouped_bar = px.bar(
    scenario_long,
    x="Metric",
    y="Amount",
    color="Scenario",
    barmode="group",
    text="Amount",
    title="Comparison of Current and Simulated Financial Situation"
)
grouped_bar.update_traces(texttemplate='%{text:.2f}', textposition='outside')
grouped_bar.update_layout(height=500)
st.plotly_chart(grouped_bar, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ==============================
# RADAR + WATERFALL
# ==============================
colE, colF = st.columns(2)

with colE:
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.subheader("🕸️ Expense Pressure Profile (Radar Chart)")

    categories = expense_data["Category"].tolist()
    values = expense_data["Converted Amount"].tolist()

    radar = go.Figure()
    radar.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Expense Profile'
    ))

    radar.update_layout(
        polar=dict(radialaxis=dict(visible=True)),
        showlegend=False,
        height=500,
        title="Financial Pressure by Expense Category"
    )
    st.plotly_chart(radar, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with colF:
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.subheader("💧 Savings Formation Waterfall Analysis")

    waterfall = go.Figure(go.Waterfall(
        name="Budget Flow",
        orientation="v",
        measure=["relative", "relative", "relative", "relative", "relative", "relative", "total"],
        x=["Income", "Food", "Rent", "Transport", "Utilities", "Other", "Net Savings"],
        textposition="outside",
        text=[
            f"{currency_symbol}{display_income:,.2f}",
            f"-{currency_symbol}{food * conversion_rate:,.2f}",
            f"-{currency_symbol}{rent * conversion_rate:,.2f}",
            f"-{currency_symbol}{transport * conversion_rate:,.2f}",
            f"-{currency_symbol}{utilities * conversion_rate:,.2f}",
            f"-{currency_symbol}{(entertainment + healthcare) * conversion_rate:,.2f}",
            f"{currency_symbol}{display_savings:,.2f}"
        ],
        y=[
            display_income,
            -(food * conversion_rate),
            -(rent * conversion_rate),
            -(transport * conversion_rate),
            -(utilities * conversion_rate),
            -((entertainment + healthcare) * conversion_rate),
            0
        ],
    ))

    waterfall.update_layout(
        title="How Income Converts into Savings",
        height=500
    )
    st.plotly_chart(waterfall, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ==============================
# AI RECOMMENDATION
# ==============================
st.markdown('<div class="section-box">', unsafe_allow_html=True)
st.subheader("🤖 AI Budget Recommendation")

if monthly_savings < 0:
    recommendation = (
        "⚠️ Your projected budget is in deficit. Reduce non-essential expenses "
        "such as entertainment and discretionary spending, or improve income."
    )
elif savings_ratio < 10:
    recommendation = (
        "🟡 Your savings are low. Consider controlling food, transport, or rent-related "
        "costs and create a stricter monthly budget."
    )
elif savings_ratio < 20:
    recommendation = (
        "🟢 Your budget is moderately healthy. With minor cost optimization and "
        "inflation planning, you can improve long-term financial stability."
    )
else:
    recommendation = (
        "✅ Excellent budget health! Your savings capacity is strong. Consider investing "
        "a portion of surplus funds for wealth growth and inflation protection."
    )

st.success(recommendation)
st.markdown('</div>', unsafe_allow_html=True)

# ==============================
# FOOTER
# ==============================
st.markdown("---")
st.markdown(
    "<center><b>LifeCost AI</b> | MBA Project Dashboard | Developed using Python, Streamlit, Pandas & Plotly</center>",
    unsafe_allow_html=True
)