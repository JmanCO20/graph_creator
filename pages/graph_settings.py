import streamlit as st
from app.graph_utilities import create_graph_w_y_int, create_bar_graph, create_graph_wo_y_int, load_user_graph, update_variables
from fastapi import HTTPException
import pandas as pd

API_URL = st.secrets["API_URL"]
cookie = st.session_state.session.cookies.get_dict()

update_variables()

col1, col2 = st.columns(2)

with col1:
    graph_id = st.text_input("Enter Graph Id")
    if st.button("Update Graph"):
        try:
            if graph_id == "":
                raise ValueError
            response = st.session_state.session.get(f"{API_URL}/user/update/{graph_id}", cookies=cookie)
            if response.status_code == 200:
                st.session_state.graph_update = {"update": True, "graph_id": graph_id}
                st.switch_page("pages/table_page.py")
            elif response.status_code == 404:
                st.error("Graph id does not exist")
            elif response.status_code == 422:
                st.error("Graph please enter a valid graph id")
            else:
                st.error(response.text)
        except ValueError:
            st.error("Please enter a graph id")

with col2:
    graph_id = st.text_input("Enter Graph Id", key="graph_id")
    if st.button("Delete Graph"):
        response = st.session_state.session.delete(f"{API_URL}/graph/{graph_id}", cookies=cookie)
        if response.status_code == 200:
            st.success("successfully deleted graph")
        else:
            st.error(response.text)

def create_graph():
    if graph_type == "bar graph":
        create_bar_graph(labels=labels, df=df)
    elif previous_lines.keys() != [None, None, None]:
        load_user_graph(df=df, labels=labels, previous_lines=previous_lines, checkboxes=checkboxes, trendlines=trendlines, window_size=window_size, sig_figs=sig_figs)
    elif checkboxes["has_y_int"]:
        create_graph_w_y_int(df=df, labels=labels, checkboxes=checkboxes, trendlines=trendlines, window_size=window_size, sig_figs=sig_figs)
    else:
        create_graph_wo_y_int(labels=labels, df=df, checkboxes=checkboxes, trendlines=trendlines, window_size=window_size, sig_figs=sig_figs)


try:
    if not st.session_state.user:
        raise AssertionError
    st.header("Previous Graphs")

    response = st.session_state.session.get(API_URL + "/user/graphs", cookies=cookie)
    if response.status_code == 200:
        graphs = response.json()
    else:
        st.error(response.text)
        response.raise_for_status()

    container = st.container(border=True, height=1000)

    with container:
        for graph in graphs:
            labels = graph["data"]["labels"]
            df = pd.DataFrame(graph["data"]["df"])
            graph_type = graph["graph_type"]
            checkboxes = graph["data"]["checkboxes"]
            trendlines = graph["data"]["trendlines"]
            window_size = graph["data"]["window_size"]
            previous_lines = graph["data"]["previous_lines"]
            sig_figs = graph["data"]["sig_figs"]

            st.write(f"Graph Id: {graph["id"]}")
            create_graph()


except AssertionError:
    pass
except HTTPException:
    st.error("Could not retrieve graphs")