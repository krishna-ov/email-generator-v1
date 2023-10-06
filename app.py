import streamlit as st
from email_generator import generate_sample

# Streamlit interface
st.title("Email Generator - Testing")

# Dropdown to select a company
company_names = ["Outreach", "Trustible", "Zeotap"]
selected_company_name = st.selectbox("Select a company:", company_names + ["Enter My Own Company"])

# If "Enter My Own Company" is selected, display input fields
if selected_company_name == "Enter My Own Company":
    custom_company_name = st.text_input("Enter Company Name:")
    custom_company_founder = st.text_input("Enter Company Founder:")
    custom_company_description = st.text_area("Enter Company Description:")
    output = generate_sample(custom_company_name, custom_company_founder, custom_company_description)
else:
    output = generate_sample(company_name=selected_company_name)

# Button to generate sample
if st.button("Generate Sample"):
    st.text_area("Output:", value=output, height=500)
