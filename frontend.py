import streamlit as st
import requests
import pandas as pd

if "user" not in st.session_state:
    st.session_state.user = None
if "login" not in st.session_state:
    st.session_state.login = False
if "session" not in st.session_state:
    st.session_state.session = requests.Session()
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=["x", "x uncertainty", "y", "y uncertainty"])
if "y_int" not in st.session_state:
    st.session_state.y_int = None
if "has_y_int" not in st.session_state:
    st.session_state.has_y_int = False
if "title" not in st.session_state:
    st.session_state.title = "Title"
if "y_label" not in st.session_state:
    st.session_state.y_label = "y_axis"
if "x_label" not in st.session_state:
    st.session_state.x_label = "x_axis"
if "graph_type" not in st.session_state:
    st.session_state.graph_type = None

if st.session_state.user:
    st.sidebar.header(f"Hello {st.session_state.user['email']}")

table_page = st.Page("pages/table_page.py", title="Table Creator")
graph_page = st.Page("pages/graph_page.py", title="Graph Creator")
login_page = st.Page("pages/login_page.py", title="Login Page")
account_page = st.Page("pages/account_settings.py", title="Account Options")

if st.session_state.user:
    pg = st.navigation([table_page, graph_page, account_page])
else:
    pg = st.navigation([table_page, graph_page, login_page])

pg.run()

