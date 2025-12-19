# app.py

import streamlit as st
from auth.login import send_otp, verify_user
from dashboards.police import police_dashboard
from dashboards.organization import organization_dashboard

st.set_page_config(page_title="Missing Child Finder", layout="centered")
st.title("🧒 Missing Child Finder System")

# ---------- SESSION STATE ----------
if "otp" not in st.session_state:
    st.session_state.otp = None
if "email" not in st.session_state:
    st.session_state.email = None
if "role" not in st.session_state:
    st.session_state.role = None

# ---------- LOGIN ----------
if st.session_state.role is None:
    st.subheader("Secure Login (Email OTP)")

    email = st.text_input("Enter registered email")

    if st.button("Send OTP"):
        role = verify_user(email)
        if role:
            st.session_state.otp = send_otp(email)
            st.session_state.email = email
            st.success("OTP sent to your email")
        else:
            st.error("Unauthorized email")

    if st.session_state.otp:
        entered_otp = st.text_input("Enter OTP")

        if st.button("Verify OTP"):
            if entered_otp == st.session_state.otp:
                st.session_state.role = verify_user(st.session_state.email)
                st.success("Login successful")
                st.rerun()   # ✅ IMPORTANT LINE
            else:
                st.error("Invalid OTP")

# ---------- DASHBOARDS ----------
else:
    if st.session_state.role == "police":
        police_dashboard()
    elif st.session_state.role == "organization":
        organization_dashboard()
    else:
        st.error("Invalid role")

    if st.button("Logout"):
        st.session_state.role = None
        st.session_state.otp = None
        st.session_state.email = None
        st.rerun()   # ✅ redirect back to login
