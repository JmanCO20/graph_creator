import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv()
API_URL = os.getenv("API_URL")

session = st.session_state.session

st.title("Login Page")

email = st.text_input("email")
password = st.text_input("password", type="password")

if email and password:
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Login", type="primary", width="stretch"):
            response = session.post(API_URL + "/auth/jwt/login", data={"username": email, "password": password})

            if response.status_code == 204:
                st.success("successfully logged in")

                user_response = session.get(API_URL + "/users/me")

                if user_response.status_code == 200:
                    st.session_state.user = user_response.json()
                    st.rerun()
                else:
                    st.error(user_response.text)
            else:
                st.error(response.text)
    with col2:
        if st.button("Register", type="secondary", width="stretch"):
            response = session.post(API_URL + "/auth/register", json={"email": email, "password": password})

            if response.status_code == 201:
                st.success("successfully registered")
            else:
                st.error(response.text)
else:
    st.error("please enter both email and password")