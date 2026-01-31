import streamlit as st
import os
from dotenv import load_dotenv
import requests

load_dotenv()
API_URL = os.getenv("API_URL")

st.title("Account Settings")

st.header(f"Hello {st.session_state.user['email']}")

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Logout"):
        response = st.session_state.session.post(f"{API_URL}/auth/jwt/logout")
        if response.status_code == 204:
            st.success("successfully logged out")
            st.session_state.user = None
            st.session_state.session.remove()
            st.rerun()
        else:
            st.error(response.text)

with col2:
    graph_id = st.text_input("Enter Graph Id")
    if st.button("Delete Graph"):
        response = st.session_state.session.delete(f"{API_URL}/graph/{graph_id}")
        if response.status_code == 200:
            st.success("successfully deleted graph")
        else:
            st.error(response.text)

with col3:
    if st.button("Delete Account"):
        response = st.session_state.session.delete(f"{API_URL}/users/me")
        if response.status_code == 200:
            st.success("successfully deleted account")
            st.session_state.user = None
            st.rerun()
        else:
            st.error(response.text)
