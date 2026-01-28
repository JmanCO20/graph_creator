import streamlit as st
import requests

st.title("Login Page")

email = st.text_input("email")
password = st.text_input("password", type="password")

if email and password:
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Login", type="primary", width="stretch"):
            pass

    with col2:
        if st.button("Register", type="secondary", width="stretch"):
            pass
else:
    st.error("please enter both email and password")

