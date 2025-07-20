# main.py

import streamlit as st
from claim_Agent import respond_to_user, collect_claim_info, track_claim
from fpdf import FPDF

st.set_page_config(page_title="Insurance Claim Assistant", layout="centered")

st.title("🤖 Insurance Claim Assistant")
st.markdown("Welcome! I'm your AI assistant to help with filing and tracking insurance claims.")

# Session to track chat
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Sidebar actions
st.sidebar.header("📋 Actions")
user_action = st.sidebar.selectbox("Choose an action:", [
    "Chat with Assistant",
    "File a New Claim",
    "Track Claim Status"
])

# 1. Chat with Assistant
if user_action == "Chat with Assistant":
    user_input = st.text_input("Ask me anything about insurance claims 👇")

    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        reply = respond_to_user(user_input, st.session_state.chat_history)
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        st.markdown(f"**Assistant:** {reply}")

# 2. File a New Claim
elif user_action == "File a New Claim":
    st.subheader("\U0001F4D1 Claim Filing Form")
    claim_data = collect_claim_info()

    with st.form("claim_form"):
        name = st.text_input("Full Name")
        policy_number = st.text_input("Policy Number")
        incident_date = st.date_input("Date of Incident")
        claim_type = st.selectbox("Type of Claim", ["Health", "Vehicle", "Property", "Other"])
        description = st.text_area("Description of Incident")
        amount = st.number_input("Amount Claimed (INR)", min_value=0)
        uploaded_files = st.file_uploader(
            "Upload Supporting Documents (photos, PDFs, etc.)",
            type=["jpg", "jpeg", "png", "pdf"],
            accept_multiple_files=True
        )

        # Progress bar logic
        total_fields = 7
        filled_fields = sum([
            bool(name.strip()),
            bool(policy_number.strip()),
            incident_date is not None,
            bool(claim_type),
            bool(description.strip()),
            amount > 0,
            uploaded_files is not None and len(uploaded_files) > 0
        ])
        progress = filled_fields / total_fields
        st.progress(progress, text=f"Form completion: {int(progress*100)}%")

        # Document preview before submission
        if uploaded_files:
            st.markdown("**Preview Uploaded Documents:**")
            for file in uploaded_files:
                file_details = f"- {file.name} ({file.type}, {file.size // 1024} KB)"
                st.write(file_details)
                if file.type.startswith("image"):
                    st.image(file, caption=file.name, use_column_width=True)
                elif file.type == "application/pdf":
                    st.write("PDF ready to upload.")

        submitted = st.form_submit_button("Submit Claim")

    if submitted:
        st.success("\U0001F389 Your claim has been submitted!")
        st.info("Claim ID: C12345 (use this for tracking)")
        if uploaded_files:
            st.markdown("**Uploaded Documents:**")
            for file in uploaded_files:
                file_details = f"- {file.name} ({file.type}, {file.size // 1024} KB)"
                st.write(file_details)
                if file.type.startswith("image"):
                    st.image(file, caption=file.name, use_column_width=True)
                elif file.type == "application/pdf":
                    st.write("PDF uploaded.")
        else:
            st.info("No supporting documents uploaded.")
        # PDF receipt generation
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Insurance Claim Receipt", ln=True, align="C")
        pdf.ln(10)
        pdf.cell(200, 10, txt=f"Claim ID: C12345", ln=True)
        pdf.cell(200, 10, txt=f"Full Name: {name}", ln=True)
        pdf.cell(200, 10, txt=f"Policy Number: {policy_number}", ln=True)
        pdf.cell(200, 10, txt=f"Date of Incident: {incident_date}", ln=True)
        pdf.cell(200, 10, txt=f"Type of Claim: {claim_type}", ln=True)
        pdf.cell(200, 10, txt=f"Amount Claimed: {amount}", ln=True)
        pdf.ln(5)
        pdf.multi_cell(0, 10, txt=f"Description: {description}")
        pdf_output = pdf.output(dest='S').encode('latin1')
        st.download_button(
            label="Download Claim Receipt (PDF)",
            data=pdf_output,
            file_name=f"claim_receipt_C12345.pdf",
            mime="application/pdf"
        )
        # You could optionally call a database or API here to save the data and files

# 3. Track Claim Status
elif user_action == "Track Claim Status":
    st.subheader("🔍 Track Claim")
    claim_id = st.text_input("Enter your Claim ID")

    if st.button("Check Status"):
        status = track_claim(claim_id.strip())
        st.markdown(f"**Status:** {status}")
