# Solar-Finance-Planning
“Streamlit-based dashboard for solar power plant financial planning, revenue analysis, and bank loan evaluation with visual insights and Excel export.”

# 🔆 Solar Plant Financial Planning Dashboard

A **Streamlit-based web application** for **financial planning and bank evaluation**
of utility-scale solar power plants.

This tool helps estimate **energy generation, revenue, bank EMI, maintenance cost,
and net profit** using **conservative, bank-friendly assumptions**.

---

## 🚀 Features

- Fixed plant cost: **₹3.5 crore per MW**
- Fixed CUF: **17% (bank conservative)**
- Automatic energy generation calculation
- Daily / Monthly / Annual unit production
- Revenue estimation using custom tariff
- Bank loan & EMI calculation
- Maintenance cost inclusion
- Net profit analysis
- Clean visual dashboard (charts & metrics)
- **Excel export for bank/DPR use**

---

## 🔧 Inputs

- Plant capacity (MW)
- Tariff (₹ per unit)
- Bank loan percentage
- Interest rate (% p.a.)
- Loan tenure (years)

---

## 📊 Outputs

- Daily, monthly, and yearly energy generation
- Monthly and annual revenue
- Loan amount, EMI (monthly & yearly)
- Annual maintenance cost
- Net profit (monthly & yearly)
- Visual charts for easy understanding
- Downloadable Excel report

---

## 🧮 Key Assumptions

| Parameter | Value |
|---------|------|
| Plant Cost | ₹3.5 crore / MW |
| CUF | 17% |
| Specific Yield | ~1490 kWh/kWp/year |
| Maintenance | ₹6 lakh / MW / year |

---

## ▶️ How to Run Locally

### 1️⃣ Install dependencies
```bash
pip install -r requirements.txt
