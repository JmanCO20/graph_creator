import streamlit as st

table_page = st.Page("pages/table_page.py", title="Table Creator")
graph_page = st.Page("pages/graph_page.py", title="Graph Creator")
login_page = st.Page("pages/login_page.py", title="Login Page")

pg = st.navigation([table_page, graph_page, login_page])

login = st.sidebar.button("Login")
if login:
    st.switch_page("pages/login_page.py")


pg.run()