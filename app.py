import streamlit as st
import pickle
import pandas as pd

# Load model and column structure
model = pickle.load(open("lead_model.pkl", "rb"))
model_columns = pickle.load(open("model_columns.pkl", "rb"))

st.title("🔍 Predictive Lead Conversion AI")
st.markdown("Enter lead details below to check if the user is likely to convert.")

# --- Input Fields ---
total_visits = st.number_input("Total Visits", min_value=0, value=5)
time_spent = st.number_input("Total Time Spent on Website", min_value=0, value=10)
page_views = st.number_input("Page Views Per Visit", min_value=0, value=2)

lead_origin = st.selectbox("Lead Origin", [
    "Landing Page Submission", "Lead Add Form", "API", "Lead Import"
])

lead_source = st.selectbox("Lead Source", [
    "Google", "Direct Traffic", "Olark Chat", "Organic Search", 
    "Reference", "Welingak Website", "Referral Sites", "Facebook"
])

do_not_email = st.selectbox("Do Not Email", ["No", "Yes"])
do_not_call = st.selectbox("Do Not Call", ["No", "Yes"])

# --- Manual One-Hot Encoding ---
input_dict = {
    'TotalVisits': total_visits,
    'Total Time Spent on Website': time_spent,
    'Page Views Per Visit': page_views,
    'Do Not Email_Yes': 1 if do_not_email == 'Yes' else 0,
    'Do Not Call_Yes': 1 if do_not_call == 'Yes' else 0,
}

# Encode categorical fields
for col in model_columns:
    if "Lead Origin_" in col:
        input_dict[col] = 1 if col.split("_")[1] == lead_origin else 0
    elif "Lead Source_" in col:
        input_dict[col] = 1 if col.split("_")[1] == lead_source else 0

# Add missing columns as 0
for col in model_columns:
    if col not in input_dict:
        input_dict[col] = 0

# Create DataFrame
input_df = pd.DataFrame([input_dict])
input_df = input_df[model_columns]  # reorder columns

# --- Prediction ---
if st.button("Predict Conversion"):
    result = model.predict(input_df)[0]
    st.success("✅ Predicted Conversion: YES" if result == 1 else "❌ Predicted Conversion: NO")
