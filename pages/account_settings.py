import streamlit as st

API_URL = st.secrets["API_URL"]

st.title("Account Settings")

st.header(f"Hello {st.session_state.user['email']}")

cookie = st.session_state.session.cookies.get_dict()

col1, col2 = st.columns(2)
with col1:
    if st.button("Logout"):
        response = st.session_state.session.post(f"{API_URL}/auth/jwt/logout", cookies=cookie)
        if response.status_code == 204:
            st.success("successfully logged out")
            st.session_state.user = None
            del st.session_state["session"]
            st.rerun()
        else:
            st.error(response.text)

with col2:
    if st.button("Delete Account"):
        response = st.session_state.session.delete(f"{API_URL}/users/me", cookies=cookie)
        if response.status_code == 204:
            st.success("successfully deleted account")
            st.session_state.user = None
            del st.session_state["session"]
            st.rerun()
        else:
            st.error(response.text)
