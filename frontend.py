import streamlit as st
import requests
import pandas as pd

if "user" not in st.session_state:
    st.session_state.user = None
if "session" not in st.session_state:
    st.session_state.session = requests.Session()
if "df_copy" not in st.session_state:
    st.session_state.df_copy = {"x": None, "y": None, "x uncertainty": 0, "y uncertainty": 0}
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame({"x": pd.Series(dtype=float, data=st.session_state.df_copy["x"]),
                                        "x uncertainty": pd.Series(dtype=float, data=st.session_state.df_copy["x uncertainty"] if "x uncertainty" in st.session_state.df_copy else 0),
                                        "y": pd.Series(dtype=float, data=st.session_state.df_copy["y"]),
                                        "y uncertainty": pd.Series(dtype=float, data=st.session_state.df_copy["y uncertainty"])
                                        })
if "checkboxes" not in st.session_state:
    st.session_state.checkboxes = {"frontend": {"has_y_int": False, "y_int": None, "legend": True, "wants_set_window": False},
                                   "values": {"has_y_int": False, "y_int": None, "legend": True, "wants_set_window": False}
                                   }
if "sig_figs" not in st.session_state:
    st.session_state.sig_figs = {"frontend": 3,
                                 "values": 3
                                 }
if "labels" not in st.session_state:
    st.session_state.labels = {"frontend": {"title": "Title", "x_label": "x_label", "y_label": "y_label"},
                               "values": {"title": "Title", "x_label": "x_label", "y_label": "y_label"}
                               }
if "graph_type" not in st.session_state:
    st.session_state.graph_type = None
if "trendlines" not in st.session_state:
    st.session_state.trendlines = {"frontend":{"upper": False, "lower": False, "average": False},
                                   "values": {"upper": False, "lower": False, "average": False}
                                   }
if "previous_lines" not in st.session_state:
    st.session_state.previous_lines = {"upper": None, "lower": None, "average": None}
if "window_size" not in st.session_state:
    st.session_state.window_size = {"frontend": {"xmin": 0.0, "xmax": None, "ymin": 0.0, "ymax": None},
                                    "values": {"xmin": 0.0, "xmax": None, "ymin": 0.0, "ymax": None}
                                    }
if "graph_update" not in st.session_state:
    st.session_state.graph_update = {"update": False, "graph_id": None}

if "average_enter" not in st.session_state:
    st.session_state.average_enter = False
if "upper_enter" not in st.session_state:
    st.session_state.upper_enter = False
if "lower_enter" not in st.session_state:
    st.session_state.lower_enter = False


if st.session_state.user:
    st.sidebar.header(f"Hello {st.session_state.user['email']}")

table_page = st.Page("pages/table_page.py", title="Table Creator")
graph_page = st.Page("pages/graph_page.py", title="Graph Creator")
login_page = st.Page("pages/login_page.py", title="Login Page")
account_page = st.Page("pages/account_settings.py", title="Account Options")
graph_settings = st.Page("pages/graph_settings.py", title="Graph Settings")

if st.session_state.user:
    pg = st.navigation([table_page, graph_page, account_page, graph_settings])
else:
    pg = st.navigation([table_page, graph_page, login_page])

pg.run()

