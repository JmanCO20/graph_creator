import streamlit as st

table_page = st.Page("pages/table_page.py", title="Table Creator")
graph_page = st.Page("pages/graph_page.py", title="Graph Creator")

pg = st.navigation([table_page, graph_page])

pg.run()