import streamlit as st
import pandas as pd
from io import BytesIO

# --------------------------------------------------
# FIXED ASSUMPTIONS (BANK FRIENDLY)
# --------------------------------------------------
PLANT_COST_PER_MW = 3.5e7        # ₹3.5 crore per MW
CUF = 0.17                      # 17%
SPECIFIC_YIELD = CUF * 8760     # kWh/kWp/year
MAINTENANCE_PER_MW = 6e5        # ₹6 lakh per MW per year

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Solar Plant Financial Planner",
    layout="wide"
)

st.title("🔆 Solar Power Plant – Financial Planning Dashboard")
st.caption("Simple | Visual | Bank-Ready | Fixed Assumptions")

# --------------------------------------------------
# SIDEBAR INPUTS
# --------------------------------------------------
st.sidebar.header("🔧 Project Inputs")

capacity_mw = st.sidebar.number_input(
    "Plant Capacity (MW)",
    min_value=0.1,
    value=2.0,
    step=0.1
)

tariff = st.sidebar.number_input(
    "Tariff (₹ per unit)",
    value=3.5
)

loan_percent = st.sidebar.slider(
    "Bank Loan (%)",
    min_value=0,
    max_value=90,
    value=70
)

interest_rate = st.sidebar.number_input(
    "Bank Interest Rate (% p.a.)",
    value=9.0
)

loan_years = st.sidebar.number_input(
    "Loan Tenure (Years)",
    value=15
)

# --------------------------------------------------
# CALCULATIONS
# --------------------------------------------------
total_cost = capacity_mw * PLANT_COST_PER_MW
loan_amount = total_cost * loan_percent / 100
equity = total_cost - loan_amount

annual_units = capacity_mw * 1000 * SPECIFIC_YIELD
monthly_units = annual_units / 12
daily_units = annual_units / 365

annual_revenue = annual_units * tariff
monthly_revenue = annual_revenue / 12

monthly_rate = interest_rate / (12 * 100)
total_months = loan_years * 12

if loan_amount > 0:
    emi_monthly = (
        loan_amount * monthly_rate * (1 + monthly_rate) ** total_months
        / ((1 + monthly_rate) ** total_months - 1)
    )
else:
    emi_monthly = 0

emi_yearly = emi_monthly * 12

maintenance_yearly = capacity_mw * MAINTENANCE_PER_MW
maintenance_monthly = maintenance_yearly / 12

net_profit_yearly = annual_revenue - emi_yearly - maintenance_yearly
net_profit_monthly = net_profit_yearly / 12

# --------------------------------------------------
# VISUAL SUMMARY (TOP CARDS)
# --------------------------------------------------
st.header("📌 Project Snapshot")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Plant Capacity", f"{capacity_mw} MW")
c2.metric("CUF (Fixed)", "17 %")
c3.metric("Project Cost", f"₹ {total_cost/1e7:.2f} Cr")
c4.metric("Equity Required", f"₹ {equity/1e7:.2f} Cr")

st.divider()

# --------------------------------------------------
# ENERGY PRODUCTION
# --------------------------------------------------
st.header("⚡ Energy Production")

e1, e2, e3 = st.columns(3)
e1.metric("Daily Units", f"{daily_units:,.0f} kWh")
e2.metric("Monthly Units", f"{monthly_units:,.0f} kWh")
e3.metric("Annual Units", f"{annual_units:,.0f} kWh")

energy_df = pd.DataFrame({
    "Period": ["Daily", "Monthly", "Annual"],
    "Units (kWh)": [daily_units, monthly_units, annual_units]
})

st.bar_chart(energy_df.set_index("Period"))

st.divider()

# --------------------------------------------------
# REVENUE & COSTS
# --------------------------------------------------
st.header("💰 Revenue & Expenses")

r1, r2, r3 = st.columns(3)
r1.metric("Monthly Revenue", f"₹ {monthly_revenue/1e5:.2f} L")
r2.metric("Annual Revenue", f"₹ {annual_revenue/1e7:.2f} Cr")
r3.metric("Annual Maintenance", f"₹ {maintenance_yearly/1e5:.2f} L")

st.divider()

# --------------------------------------------------
# BANK LOAN & PROFIT
# --------------------------------------------------
st.header("🏦 Bank Loan & Profitability")

b1, b2, b3 = st.columns(3)
b1.metric("Loan Amount", f"₹ {loan_amount/1e7:.2f} Cr")
b2.metric("Monthly EMI", f"₹ {emi_monthly/1e5:.2f} L")
b3.metric("Annual EMI", f"₹ {emi_yearly/1e7:.2f} Cr")

p1, p2 = st.columns(2)
p1.metric("Net Profit (Monthly)", f"₹ {net_profit_monthly/1e5:.2f} L")
p2.metric("Net Profit (Annual)", f"₹ {net_profit_yearly/1e7:.2f} Cr")

finance_df = pd.DataFrame({
    "Category": ["Revenue", "EMI", "Maintenance", "Net Profit"],
    "Amount (₹)": [
        annual_revenue,
        emi_yearly,
        maintenance_yearly,
        net_profit_yearly
    ]
})

st.bar_chart(finance_df.set_index("Category"))

st.divider()

# --------------------------------------------------
# EXCEL EXPORT (BANK FRIENDLY)
# --------------------------------------------------
st.header("📤 Download Bank Report (Excel)")

excel_buffer = BytesIO()

with pd.ExcelWriter(excel_buffer, engine="xlsxwriter") as writer:

    pd.DataFrame({
        "Parameter": [
            "Plant Capacity (MW)",
            "CUF (%)",
            "Specific Yield (kWh/kWp/year)",
            "Total Cost (₹)",
            "Loan Amount (₹)",
            "Equity (₹)",
            "Tariff (₹/unit)"
        ],
        "Value": [
            capacity_mw,
            17,
            round(SPECIFIC_YIELD, 1),
            total_cost,
            loan_amount,
            equity,
            tariff
        ]
    }).to_excel(writer, sheet_name="Project Summary", index=False)

    pd.DataFrame({
        "Daily Units": [daily_units],
        "Monthly Units": [monthly_units],
        "Annual Units": [annual_units]
    }).to_excel(writer, sheet_name="Energy Production", index=False)

    pd.DataFrame({
        "Annual Revenue": [annual_revenue],
        "Annual EMI": [emi_yearly],
        "Maintenance Cost": [maintenance_yearly],
        "Net Profit": [net_profit_yearly]
    }).to_excel(writer, sheet_name="Financials", index=False)

st.download_button(
    "📥 Download Excel Report",
    excel_buffer.getvalue(),
    "Solar_Plant_Financial_Report.xlsx",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

st.success("✅ Simple, visual & bank-ready financial planning completed")