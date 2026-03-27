import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import streamlit.components.v1 as components
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

st.title("Oil & Gas Well Decommissioning Estimator")

# --- Input Section ---
st.header("Well Details")
well_name = st.text_input("Well Name / ID")
operator = st.text_input("Operator")
field = st.text_input("Field / Basin")
well_type = st.selectbox("Well Type", ["Development", "Appraisal", "Exploration"])
vertical_depth = st.number_input("Vertical Depth (m)", min_value=0)
horizontal_depth = st.number_input("Horizontal Depth (m)", min_value=0)
start_prod = st.date_input("Start of Production")
end_prod = st.date_input("End of Production")

st.header("Cost Parameters")
pna_cost_per_meter = st.number_input("Plug & Abandonment Cost per meter (£)", min_value=0.0)
site_remediation_cost = st.number_input("Site Remediation Cost (£)", min_value=0.0)
contingency_pct = st.slider("Contingency (%)", 0, 50, 10)

# --- Calculate Costs ---
total_depth = vertical_depth + horizontal_depth
pna_cost = total_depth * pna_cost_per_meter
total_cost = pna_cost + site_remediation_cost
total_cost_with_contingency = total_cost * (1 + contingency_pct / 100)

# --- Output Section ---
st.header("Estimated Decommissioning Cost")
st.write(f"**P&A Cost:** £{pna_cost:,.2f}")
st.write(f"**Site Remediation Cost:** £{site_remediation_cost:,.2f}")
st.write(f"**Total Cost (with {contingency_pct}% contingency):** £{total_cost_with_contingency:,.2f}")

# --- Visualization ---
st.header("Cost Breakdown")
cost_df = pd.DataFrame({
    "Cost Component": ["Plug & Abandonment", "Site Remediation", "Contingency"],
    "Amount (£)": [pna_cost, site_remediation_cost, total_cost_with_contingency - total_cost]
})
st.bar_chart(cost_df.set_index("Cost Component"))

# --- Email Capture ---
st.header("Sign Up for Updates / Interest Form")
st.write("Leave your details if you want updates or future access to the app.")

# Input fields
first_name = st.text_input("First Name")
last_name = st.text_input("Last Name")
email = st.text_input("Email")

if st.button("Submit"):
    if first_name and last_name and email:
        # --- Google Sheets setup ---
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("decomm.json", scope)
        client = gspread.authorize("streamlit-gsheet-491513-5de83d6f2d9a")

        # Open your Google Sheet by name
        sheet = client.open("streamlit-sheets").sheet1

        # Append data
        sheet.append_row([first_name, last_name, email, str(datetime.now())])
        st.success("Thank you! Your information has been recorded.")
    else:
        st.error("Please fill in all fields.")