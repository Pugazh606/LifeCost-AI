from pyparsing import col
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="LifeCost AI - Smart Cost of Living Analyzer",
    page_icon="💰",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
    <style>
    .main {
        background-color: #0E1117;
        color: #ffffff;
    }

    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }

    /* Main headings */
    h1 {
        color: #ffffff !important;
        font-weight: 800 !important;
    }

    h2 {
        color: #ffffff !important;
        font-weight: 700 !important;
    }

    h3 {
        color: #facc15 !important;   /* Bright golden */
        font-weight: 700 !important;
    }

    h4, h5, h6 {
        color: #fde68a !important;   /* Soft gold */
        font-weight: 600 !important;
    }

    /* Normal text */
    p, div, span, label {
        color: #f9fafb !important;
    }

    /* Metric cards */
    .stMetric {
        background-color: #1f2937;
        padding: 12px;
        border-radius: 12px;
        border: 1px solid #374151;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.25);
    }

    /* Sidebar text */
    section[data-testid="stSidebar"] * {
        color: #ffffff !important;
    }

    /* Dataframe styling fix */
    .stDataFrame {
        background-color: #111827 !important;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------- HELPER FUNCTION FOR CHART THEME ----------------
def apply_chart_theme(fig):
    fig.update_layout(
        paper_bgcolor="#1a1f2e",
        plot_bgcolor="#1a1f2e",
        font=dict(color="white"),
        title_font=dict(color="white"),
        xaxis=dict(
            title_font=dict(color="white"),
            tickfont=dict(color="white"),
            gridcolor="rgba(255,255,255,0.08)"
        ),
        yaxis=dict(
            title_font=dict(color="white"),
            tickfont=dict(color="white"),
            gridcolor="rgba(255,255,255,0.08)"
        ),
        legend=dict(font=dict(color="white"))
    )
    return fig

# ---------------- TITLE ----------------
st.title("💰 LifeCost AI - Smart Cost of Living Analyzer")
st.markdown("### Analyze your monthly budget, spending habits, inflation impact, and financial health intelligently")

# ---------------- SIDEBAR INPUTS ----------------
input_mode = st.sidebar.radio(
    "Choose Data Entry Mode",
    ["Manual Entry", "Excel Upload"]
)

if input_mode == "Manual Entry":

    st.sidebar.header("📥 Enter Monthly Financial Details")

    user_name = st.sidebar.text_input("👤 Enter Your Name", value="Pugazh")

    currency = st.sidebar.selectbox("Select Currency", ["INR (₹)", "USD ($)", "EUR (€)", "GBP (£)"])
    currency_symbol = currency.split("(")[1].replace(")", "")

    monthly_income = st.sidebar.number_input("Monthly Income", 0.0, 50000000.0, 0.0,step=1000.0)
    rent = st.sidebar.number_input("Rent", 0.0, 40000.0, 0.0,step=500.0)
    food = st.sidebar.number_input("Food", 0.0, 10000.0, 0.0,step=100.0)
    transport = st.sidebar.number_input("Transport", 0.0, 5000.0, 0.0,step=100.0)
    utilities = st.sidebar.number_input("Utilities", 0.0, 5000.0, 0.0,step=100.0)
    entertainment = st.sidebar.number_input("Entertainment", 0.0, 5000.0, 0.0,step=100.0)
    healthcare = st.sidebar.number_input("Healthcare", 0.0, 5000.0, 0.0,step=100.0)
    other = st.sidebar.number_input("Other", 0.0, 5000.0, 0.0,step=100.0)

elif input_mode == "Excel Upload":

    uploaded_file = st.sidebar.file_uploader(
        "Upload Excel File",
        type=["xlsx", "xls", "csv"],
        key="excel_uploader"
    )

    if uploaded_file is not None:

        if uploaded_file.name.endswith(".csv"):
            df_uploaded = pd.read_csv(uploaded_file)
        else:
            df_uploaded = pd.read_excel(uploaded_file)

        df_uploaded.columns = df_uploaded.columns.str.lower().str.strip()

        selected_name = st.sidebar.selectbox(
            "👤 Select Name",
            df_uploaded["name"].dropna().unique()
        )

        user_row = df_uploaded[df_uploaded["name"] == selected_name].iloc[0]

        def get(col):
            return pd.to_numeric(user_row.get(col, 0), errors="coerce") or 0

        user_name = user_row.get("name", "User")

        currency_map = {
            "INR": "₹",
            "USD": "$",
            "EUR": "€",
            "GBP": "£",
            "CAD": "C$",
            "AUD": "A$",
            "JPY": "¥",
            "SGD": "S$",
            "AED": "د.إ",
            "MYR": "RM"
        }

        currency_code = str(user_row.get("currency", "INR")).upper()
        currency_symbol = currency_map.get(currency_code, "₹")
        st.sidebar.header("📥 Enter Monthly Financial Details")

        def safe_get(row, col):
            return float(pd.to_numeric(row.get(col, 0), errors="coerce"))

        monthly_income = st.sidebar.number_input("Monthly Income", 0.0, 50000000.0, safe_get(user_row, "income"), step=1000.0)
        rent = st.sidebar.number_input("Rent", 0.0, 500000.0, safe_get(user_row, "rent"), step=500.0)
        food = st.sidebar.number_input("Food", 0.0, 100000.0, safe_get(user_row, "food"), step=100.0)
        transport = st.sidebar.number_input("Transport", 0.0, 100000.0, safe_get(user_row, "transport"), step=100.0)
        utilities = st.sidebar.number_input("Utilities", 0.0, 100000.0, safe_get(user_row, "utilities"), step=100.0)
        entertainment = st.sidebar.number_input("Entertainment", 0.0, 100000.0, safe_get(user_row, "entertainment"), step=100.0)
        healthcare = st.sidebar.number_input("Healthcare", 0.0, 100000.0, safe_get(user_row, "healthcare"), step=100.0)
        other = st.sidebar.number_input("Other", 0.0, 100000.0, safe_get(user_row, "other"), step=100.0)

        inflation_rate = float(user_row.get("inflation", 0))

    else:
        st.warning("📂 Please upload a file")
        st.stop()# ---------------- INFLATION RATE INPUT ----------------
st.sidebar.markdown("---")
st.sidebar.subheader("📈 Inflation Adjustment")

inflation_rate = st.sidebar.slider(
    "Select Inflation Rate (%)",
    min_value=0.0,
    max_value=20.0,
    value=6.0,
    step=0.1
)

# ---------------- OPTIONAL EXCEL UPLOAD ----------------
st.sidebar.markdown("---")
st.sidebar.subheader("📂 Upload Excel File (Optional)")
uploaded_file = st.sidebar.file_uploader("Upload Excel File", type=["xlsx", "xls", "csv"])

excel_data_loaded = False

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith(".csv"):
            df_uploaded = pd.read_csv(uploaded_file)
        else:
            df_uploaded = pd.read_excel(uploaded_file)

        st.sidebar.success("✅ Excel file uploaded successfully!")
        st.sidebar.write("Columns detected:", list(df_uploaded.columns))

        # Try to auto-map first row if matching columns exist
        cols_lower = [col.lower() for col in df_uploaded.columns]

        if "monthly_income" in cols_lower:
            monthly_income = float(df_uploaded.iloc[0, cols_lower.index("monthly_income")])
        if "rent" in cols_lower:
            rent = float(df_uploaded.iloc[0, cols_lower.index("rent")])
        if "food" in cols_lower:
            food = float(df_uploaded.iloc[0, cols_lower.index("food")])
        if "transport" in cols_lower:
            transport = float(df_uploaded.iloc[0, cols_lower.index("transport")])
        if "utilities" in cols_lower:
            utilities = float(df_uploaded.iloc[0, cols_lower.index("utilities")])
        if "entertainment" in cols_lower:
            entertainment = float(df_uploaded.iloc[0, cols_lower.index("entertainment")])
        if "healthcare" in cols_lower:
            healthcare = float(df_uploaded.iloc[0, cols_lower.index("healthcare")])
        if "other" in cols_lower:
            other = float(df_uploaded.iloc[0, cols_lower.index("other")])
        if "name" in cols_lower:
            user_name = str(df_uploaded.iloc[0, cols_lower.index("name")])

        excel_data_loaded = True

    except Exception as e:
        st.sidebar.error(f"❌ Error reading file: {e}")

# ---------------- CALCULATIONS ----------------
base_expenses = rent + food + transport + utilities + entertainment + healthcare + other
inflation_multiplier = 1 + (inflation_rate / 100)
inflation_adjusted_expenses = base_expenses * inflation_multiplier
monthly_savings = monthly_income - base_expenses
inflation_adjusted_savings = monthly_income - inflation_adjusted_expenses

savings_rate = (monthly_savings / monthly_income * 100) if monthly_income > 0 else 0
expense_ratio = (base_expenses / monthly_income * 100) if monthly_income > 0 else 0
inflation_expense_ratio = (inflation_adjusted_expenses / monthly_income * 100) if monthly_income > 0 else 0

# Budget health score (0 to 100)
budget_health_score = max(0, min(100, savings_rate))

# ---------------- PERSONALIZED GREETING ----------------
st.markdown(f"## 👋 Welcome, {user_name}!")

if excel_data_loaded:
    st.info("📂 Your uploaded Excel data has been applied to the dashboard automatically.")

# ---------------- METRICS ----------------
st.markdown("## 📌 Financial Summary")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Monthly Income", f"{currency_symbol}{monthly_income:,.2f}")

with col2:
    st.metric("Base Expenses", f"{currency_symbol}{base_expenses:,.2f}")

with col3:
    st.metric("Monthly Savings", f"{currency_symbol}{monthly_savings:,.2f}")

with col4:
    st.metric("Savings Rate", f"{savings_rate:.2f}%")

# ---------------- INFLATION METRICS ----------------
st.markdown("## 📈 Inflation Impact Summary")

col5, col6, col7, col8 = st.columns(4)

with col5:
    st.metric("Inflation Rate", f"{inflation_rate:.2f}%")

with col6:
    st.metric("Inflation Adjusted Expenses", f"{currency_symbol}{inflation_adjusted_expenses:,.2f}")

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