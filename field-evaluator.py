import streamlit as st
import numpy as np
import pandas as pd

st.title("Learn and test upstream project economics in 30 seconds—no Excel needed”")

# Inputs
production = st.number_input("Production (bbl/year)", value=100000)
price = st.number_input("Oil Price ($/bbl)", value=70)
opex = st.number_input("OPEX ($/bbl)", value=20)
capex = st.number_input("CAPEX ($)", value=5000000)
discount_rate = st.number_input("Discount Rate (%)", value=10) / 100

years = 10

# NPV Calculation
cash_flows = []
for year in range(years):
    revenue = production * (price - opex)
    if year == 0:
        revenue -= capex
    discounted = revenue / ((1 + discount_rate) ** year)
    cash_flows.append(discounted)

npv = sum(cash_flows)

st.subheader(f"NPV: ${round(npv,2)}")

# Sensitivity
prices = np.arange(40, 101, 5)
npvs = []

for p in prices:
    cf = []
    for year in range(years):
        rev = production * (p - opex)
        if year == 0:
            rev -= capex
        cf.append(rev / ((1 + discount_rate) ** year))
    npvs.append(sum(cf))

df = pd.DataFrame({"Oil Price": prices, "NPV": npvs})
st.line_chart(df.set_index("Oil Price"))

# Breakeven (simple)
breakeven = None
for p in prices:
    cf = []
    for year in range(years):
        rev = production * (p - opex)
        if year == 0:
            rev -= capex
        cf.append(rev / ((1 + discount_rate) ** year))
    if sum(cf) > 0:
        breakeven = p
        break

st.subheader(f"Breakeven Price: ${breakeven}")

# Email capture
st.markdown("---")
st.subheader("Get more upstream tools & datasets")

email = st.text_input("Enter your email")

if st.button("Join Early Access"):
    if email:
        st.success("You're on the list!")
        # Connect this to Google Sheets / Airtable later
    else:
        st.error("Please enter a valid email")