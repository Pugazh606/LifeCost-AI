# ==========================================================
# LifeCost AI - COMPLETE FINAL FULL CODE
# Final Version with BIG Line Chart + BIG Scatter Plot
# BIG Radar Chart + BIG Waterfall Chart
# Save as: lifecost_ai_app.py
# Run: streamlit run lifecost_ai_app.py
# ==========================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ==========================================================
# PAGE CONFIG
# ==========================================================
st.markdown("""
<style>

/* BACKGROUND GRADIENT */
.main {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    color: white;
}

/* GLASS CARD EFFECT */
.stMetric, .css-1r6slb0, .css-12w0qpk {
    background: rgba(255, 255, 255, 0.08) !important;
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border-radius: 16px;
    padding: 15px;
    border: 1px solid rgba(255, 255, 255, 0.15);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.25);
}

/* SECTION HEADINGS */
h1 {
    font-size: 2.2rem;
    font-weight: 700;
}

h2 {
    font-size: 1.6rem;
    font-weight: 600;
    margin-top: 10px;
}

h3 {
    font-size: 1.3rem;
    font-weight: 500;
}

/* SIDEBAR GLASS */
section[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(10px);
    border-right: 1px solid rgba(255,255,255,0.1);
}

/* BUTTON STYLE */
.stButton>button {
    background: rgba(255,255,255,0.1);
    border-radius: 10px;
    border: 1px solid rgba(255,255,255,0.2);
    color: white;
}

/* TABLE GLASS */
.css-1d391kg {
    background: rgba(255,255,255,0.05) !important;
    border-radius: 10px;
}

/* SCROLLBAR */
::-webkit-scrollbar {
    width: 8px;
}
::-webkit-scrollbar-thumb {
    background: rgba(255,255,255,0.2);
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# ==========================================================
# STYLE FUNCTION
# ==========================================================
def style(fig, h=420):
    fig.update_layout(
        height=h,
        paper_bgcolor="#0E1117",
        plot_bgcolor="#111827",
        font=dict(color="white"),
        title_font=dict(size=18,color="white"),
        margin=dict(l=20,r=20,t=60,b=20)
    )
    return fig

# ==========================================================
# SIDEBAR
# ==========================================================
st.sidebar.title("📥 Manual Entry / Upload Panel")

currency = st.sidebar.selectbox(
    "💱 Select Currency",
    ["INR (₹)", "USD ($)", "EUR (€)", "GBP (£)", "JPY (¥)"]
)
symbol = currency.split("(")[1].replace(")", "")

uploaded_file = st.sidebar.file_uploader(
    "📂 Upload Excel / CSV File",
    type=["xlsx","csv"]
)

# ==========================================================
# DEFAULT VALUES
# ==========================================================
name = "Pugazh"
income = 50000.0
rent = 15000.0
food = 7000.0
transport = 3000.0
utilities = 4000.0
entertainment = 2500.0
healthcare = 2000.0
other = 1500.0

# ==========================================================
# FILE READ
# ==========================================================
df = None

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.sidebar.success("✅ File Uploaded")

        if "Name" in df.columns:
            selected_name = st.sidebar.selectbox(
                "👤 Select Person",
                df["Name"].astype(str).unique()
            )

            row = df[df["Name"].astype(str)==selected_name].iloc[0]

            name = selected_name
            income = float(row.get("Income", income))
            rent = float(row.get("Rent", rent))
            food = float(row.get("Food", food))
            transport = float(row.get("Transport", transport))
            utilities = float(row.get("Utilities", utilities))
            entertainment = float(row.get("Entertainment", entertainment))
            healthcare = float(row.get("Healthcare", healthcare))
            other = float(row.get("Other", other))

    except:
        st.sidebar.error("Invalid file format")

# ==========================================================
# MANUAL ENTRY
# ==========================================================
name = st.sidebar.text_input("👤 Name", value=name)
income = st.sidebar.number_input("💰 Monthly Income", value=income)
rent = st.sidebar.number_input("🏠 Rent", value=rent)
food = st.sidebar.number_input("🍔 Food", value=food)
transport = st.sidebar.number_input("🚗 Transport", value=transport)
utilities = st.sidebar.number_input("💡 Utilities", value=utilities)
entertainment = st.sidebar.number_input("🎬 Entertainment", value=entertainment)
healthcare = st.sidebar.number_input("🏥 Healthcare", value=healthcare)
other = st.sidebar.number_input("📦 Other", value=other)

# ==========================================================
# INFLATION
# ==========================================================
st.sidebar.markdown("---")
st.sidebar.subheader("📈 Inflation Controls")

past_inf = st.sidebar.slider("Past Inflation %",0.0,20.0,4.0,0.1)
current_inf = st.sidebar.slider("Current Inflation %",0.0,20.0,6.0,0.1)
future_inf = st.sidebar.slider("Expected Future Inflation %",0.0,20.0,8.0,0.1)

# ==========================================================
# CALCULATIONS
# ==========================================================
base_expense = rent+food+transport+utilities+entertainment+healthcare+other
past_expense = base_expense/(1+current_inf/100)*(1+past_inf/100)
future_expense = base_expense*(1+future_inf/100)

savings = income-base_expense
savings_rate = (savings/income*100) if income>0 else 0
expense_ratio = (base_expense/income*100) if income>0 else 0
health_score = max(0,min(100,savings_rate))

expense_df = pd.DataFrame({
"Category":["Rent","Food","Transport","Utilities","Entertainment","Healthcare","Other"],
"Amount":[rent,food,transport,utilities,entertainment,healthcare,other]
})

# ---------------- TITLE ----------------
st.title("💰 LifeCost AI - Smart Cost of Living Analyzer")
st.markdown("### Analyze your monthly budget, spending habits, inflation impact, and financial health intelligently")

# ---------------- PERSONALIZED GREETING ----------------
user_name = "Pugazh"
st.markdown(f"## 👋 Welcome, {user_name}!")



# ==========================================================
# KPI
# ==========================================================
# ---------------- METRICS ----------------
st.markdown("## 📌 Financial Summary")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Monthly Income", f"{symbol}{monthly_income:,.2f}")

with col2:
    st.metric("Base Expenses", f"{symbol}{base_expenses:,.2f}")

with col3:
    st.metric("Monthly Savings", f"{symbol}{monthly_savings:,.2f}")

with col4:
    st.metric("Savings Rate", f"{savings_rate:.2f}%")

# ---------------- INFLATION METRICS ----------------
st.markdown("## 📈 Inflation Impact Summary")

col5, col6, col7, col8 = st.columns(4)

with col5:
    st.metric("Inflation Rate", f"{inflation_rate:.2f}%")

with col6:
    st.metric("Inflation Adjusted Expenses", f"{symbol}{inflation_adjusted_expenses:,.2f}")

with col7:
    st.metric("Adjusted Savings", f"{currency_symbol}{inflation_adjusted_savings:,.2f}")

with col8:
    st.metric("Adjusted Expense Ratio", f"{inflation_expense_ratio:.2f}%")

# ---------------- DATAFRAME FOR EXPENSES ----------------
expense_df = pd.DataFrame({
    "Category": ["Rent", "Food", "Transport", "Utilities", "Entertainment", "Healthcare", "Other"],
    "Amount": [rent, food, transport, utilities, entertainment, healthcare, other]
})

expense_df["Inflation Adjusted Amount"] = expense_df["Amount"] * inflation_multiplier
expense_df["Amount"] = pd.to_numeric(expense_df["Amount"], errors="coerce").fillna(0)
expense_df["Inflation Adjusted Amount"] = pd.to_numeric(expense_df["Inflation Adjusted Amount"], errors="coerce").fillna(0)

# ---------------- CHARTS SECTION ----------------
st.markdown("---")
st.markdown("## 📊 Financial Analytics Dashboard")

# Row 1: Key Overview + Expense Distribution
colA, colB = st.columns(2)

with colA:
    st.markdown("### 📊 Key Financial Overview")
    overview_df = pd.DataFrame({
        "Metric": ["Income", "Base Expenses", "Inflation Adjusted Expenses", "Savings", "Adjusted Savings"],
        "Amount": [monthly_income, base_expenses, inflation_adjusted_expenses, monthly_savings, inflation_adjusted_savings]
    })

    fig_overview = px.bar(
        overview_df,
        x="Metric",
        y="Amount",
        text="Amount",
        title="Key Financial Overview",
        color="Metric",
        color_discrete_sequence=["#facc15", "#fb923c", "#f87171", "#4ade80", "#60a5fa"]
    )
    fig_overview.update_traces(
        texttemplate='%{text:.2f}',
        textposition='outside',
        textfont_color="white"
    )
    fig_overview.update_layout(height=430, showlegend=False)
    fig_overview = apply_chart_theme(fig_overview)
    st.plotly_chart(fig_overview, use_container_width=True)

with colB:
    st.markdown("### 🥧 Expense Distribution")
    pie_data = expense_df[expense_df["Amount"] > 0]

    if pie_data.empty:
        st.warning("No expense data available for pie chart.")
    else:
        pie_chart = px.pie(
            pie_data,
            names="Category",
            values="Amount",
            hole=0.45,
            title="Expense Distribution",
            color_discrete_sequence=px.colors.sequential.Sunset
        )
        pie_chart.update_traces(
            textfont=dict(color="white"),
            insidetextfont=dict(color="white"),
            outsidetextfont=dict(color="white")
        )
        pie_chart = apply_chart_theme(pie_chart)
        st.plotly_chart(pie_chart, use_container_width=True)

# Row 2: Expense Comparison + Budget Health Gauge
colC, colD = st.columns(2)

with colC:
    st.markdown("### 📈 Category-wise Expense Analysis")
    fig_expense = px.bar(
        expense_df.sort_values("Amount", ascending=False),
        x="Category",
        y=["Amount", "Inflation Adjusted Amount"],
        barmode="group",
        text_auto=".2f",
        title="Base vs Inflation Adjusted Expenses",
        color_discrete_sequence=["#f59e0b", "#60a5fa"]
    )
    fig_expense.update_layout(height=450)
    fig_expense = apply_chart_theme(fig_expense)
    st.plotly_chart(fig_expense, use_container_width=True)

with colD:
    st.markdown("### 🎯 Budget Health Score")
    gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=budget_health_score,
        title={"text": "Budget Health Score (%)", "font": {"color": "white"}},
        number={"font": {"color": "white"}},
        gauge={
            "axis": {"range": [0, 100], "tickcolor": "white"},
            "bar": {"color": "#22c55e"},
            "bgcolor": "#1a1f2e",
            "borderwidth": 2,
            "bordercolor": "white",
            "steps": [
                {"range": [0, 40], "color": "#7f1d1d"},
                {"range": [40, 70], "color": "#78350f"},
                {"range": [70, 100], "color": "#14532d"}
            ]
        }
    ))
    gauge.update_layout(
        paper_bgcolor="#1a1f2e",
        font={"color": "white"},
        height=450
    )
    st.plotly_chart(gauge, use_container_width=True)

# Row 3: Line Comparison
st.markdown("### 📉 Income vs Expense vs Savings Comparison")
comparison_df = pd.DataFrame({
    "Financial Metric": ["Income", "Base Expenses", "Inflation Expenses", "Savings", "Adjusted Savings"],
    "Value": [monthly_income, base_expenses, inflation_adjusted_expenses, monthly_savings, inflation_adjusted_savings]
})

fig_compare = px.line(
    comparison_df,
    x="Financial Metric",
    y="Value",
    markers=True,
    text="Value",
    title="Income vs Expenses vs Savings",
    color_discrete_sequence=["#facc15"]
)
fig_compare.update_traces(textposition="top center", textfont_color="white", line=dict(width=4))
fig_compare.update_layout(height=450)
fig_compare = apply_chart_theme(fig_compare)
st.plotly_chart(fig_compare, use_container_width=True)

# Row 4: Radar Chart
st.markdown("### 🕸️ Expense Pattern Radar Chart")

fig_radar = go.Figure()
fig_radar.add_trace(go.Scatterpolar(
    r=expense_df["Amount"],
    theta=expense_df["Category"],
    fill='toself',
    name='Base Expenses',
    line=dict(color='#f59e0b')
))
fig_radar.add_trace(go.Scatterpolar(
    r=expense_df["Inflation Adjusted Amount"],
    theta=expense_df["Category"],
    fill='toself',
    name='Inflation Adjusted',
    line=dict(color='#60a5fa')
))

fig_radar.update_layout(
    polar=dict(
        bgcolor="#1a1f2e",
        radialaxis=dict(
            visible=True,
            tickfont=dict(color="white"),
            gridcolor="rgba(255,255,255,0.08)"
        ),
        angularaxis=dict(
            tickfont=dict(color="white"),
            gridcolor="rgba(255,255,255,0.08)"
        )
    ),
    paper_bgcolor="#1a1f2e",
    font=dict(color="white"),
    title="Expense Distribution Radar Analysis",
    height=500
)
st.plotly_chart(fig_radar, use_container_width=True)

# Row 5: Savings vs Expense Ratio Scatter
st.markdown("### 🔍 Savings vs Expense Ratio Insight")
insight_df = pd.DataFrame({
    "Type": ["Savings Rate", "Expense Ratio", "Inflation Expense Ratio"],
    "Percentage": [savings_rate, expense_ratio, inflation_expense_ratio]
})

fig_scatter = px.scatter(
    insight_df,
    x="Type",
    y="Percentage",
    size="Percentage",
    color="Type",
    text="Percentage",
    title="Savings Rate vs Expense Ratios",
    color_discrete_sequence=["#4ade80", "#fb923c", "#60a5fa"]
)
fig_scatter.update_traces(textposition="top center", textfont_color="white")
fig_scatter.update_layout(height=450, showlegend=False)
fig_scatter = apply_chart_theme(fig_scatter)
st.plotly_chart(fig_scatter, use_container_width=True)

# Row 6: Waterfall Chart
st.markdown("### 🌊 Income to Savings Waterfall Analysis")

waterfall = go.Figure(go.Waterfall(
    name="Financial Flow",
    orientation="v",
    measure=["absolute", "relative", "relative", "relative", "relative", "relative", "relative", "relative", "total"],
    x=["Income", "Rent", "Food", "Transport", "Utilities", "Entertainment", "Healthcare", "Other", "Savings"],
    y=[monthly_income, -rent, -food, -transport, -utilities, -entertainment, -healthcare, -other, 0],
    connector={"line": {"color": "white"}},
    increasing={"marker": {"color": "#22c55e"}},
    decreasing={"marker": {"color": "#ef4444"}},
    totals={"marker": {"color": "#f59e0b"}}
))
waterfall.update_layout(
    title="How Income Converts into Savings",
    paper_bgcolor="#1a1f2e",
    plot_bgcolor="#1a1f2e",
    font=dict(color="white"),
    height=500
)
st.plotly_chart(waterfall, use_container_width=True)

# ---------------- AI RECOMMENDATIONS ----------------
st.markdown("---")
st.markdown("## 🤖 AI-Based Financial Recommendations")

if savings_rate >= 30:
    st.success("✅ Excellent! Your savings rate is strong. You are maintaining a healthy financial lifestyle.")
elif 15 <= savings_rate < 30:
    st.info("ℹ️ Good job! Your savings are decent, but there is room for improvement by optimizing optional expenses.")
else:
    st.warning("⚠️ Your savings rate is low. Consider reducing entertainment, transport, or other discretionary expenses.")

# Detailed recommendations
highest_expense = expense_df.loc[expense_df["Amount"].idxmax(), "Category"]
highest_expense_value = expense_df["Amount"].max()

st.markdown("### 🔎 Insights")
st.write(f"- **{user_name}**, your highest spending category is **{highest_expense}** ({currency_symbol}{highest_expense_value:,.2f}).")
st.write(f"- Your expense ratio is **{expense_ratio:.2f}%** of your income.")
st.write(f"- Your inflation-adjusted expense ratio is **{inflation_expense_ratio:.2f}%**.")
st.write(f"- Your current budget health score is **{budget_health_score:.2f}/100**.")

if inflation_adjusted_savings < 0:
    st.error("🚨 After inflation adjustment, your budget may go into deficit. You should reduce discretionary expenses immediately.")
elif inflation_expense_ratio > 80:
    st.warning("⚠️ Inflation is significantly increasing your expense burden. Consider revising your monthly budget.")
else:
    st.success("✅ Your financial plan is still sustainable even after inflation adjustment.")

# ==========================================================
# EXCEL FORMAT
# ==========================================================
st.markdown("## 📂 Excel Upload Recommended Format")

sample = pd.DataFrame({
"Name":["Pugazh"],
"Income":[50000],
"Rent":[15000],
"Food":[7000],
"Transport":[3000],
"Utilities":[4000],
"Entertainment":[2500],
"Healthcare":[2000],
"Other":[1500]
})

st.dataframe(sample, use_container_width=True)

if df is not None:
    st.markdown("## 📄 Uploaded Dataset Preview")
    st.dataframe(df, use_container_width=True)

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown("### 🌟 LifeCost AI helps you make smarter financial decisions with visual analytics, inflation intelligence, and premium dashboard insights.")
st.caption("Developed for MBA Project Presentation | Streamlit + Python + Plotly")