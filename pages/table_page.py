import streamlit as st
import pandas as pd
from app.graph_utilities import create_graph_w_y_int, create_bar_graph, create_graph_wo_y_int, load_user_graph
from fastapi import HTTPException

API_URL = st.secrets["API_URL"]

cookie = st.session_state.session.cookies.get_dict()

st.title("Table Page")

def table_view_for_graphs(column_type: type):
    if column_type == float:
        st.session_state.df = pd.DataFrame({
            "x": pd.Series(dtype=float, data=st.session_state.df["x"]),
            "x uncertainty": pd.Series(dtype=float, data=st.session_state.df["x uncertainty"] if "x uncertainty" in st.session_state.df else None),
            "y": pd.Series(dtype=float, data=st.session_state.df["y"]),
            "y uncertainty": pd.Series(dtype=float, data=st.session_state.df["y uncertainty"])
        })
    else:
        st.session_state.df = pd.DataFrame({
            "x": pd.Series(dtype=str, data=st.session_state.df["x"]),
            "y": pd.Series(dtype=float, data=st.session_state.df["y"]),
            "y uncertainty": pd.Series(dtype=float, data=st.session_state.df["y uncertainty"])
        })


    editable_table = st.data_editor(st.session_state.df.reset_index(drop=True), num_rows="dynamic", hide_index=True)

    return editable_table


def form_questions():
    try:
        graph_type = st.multiselect(label="Select if you are making a Bar graph or Line graph", options=["line graph", "bar graph"], max_selections=1, default=st.session_state.graph_type)

        if not graph_type:
            raise ValueError
        elif graph_type[0] == "line graph":
            column_type = float
        else:
            column_type = str

        data_table = table_view_for_graphs(column_type)
        if graph_type[0] == "line graph":
            has_y_int = st.checkbox("Does your graph have a set Y Intercept", value=st.session_state.checkboxes["has_y_int"])
            if has_y_int:
                y_int = st.number_input("Enter Y Intercept value", value=st.session_state.checkboxes["y_int"])
            else:
                y_int = None

            wants_set_window = st.checkbox("Set graph window size", value=st.session_state.checkboxes["wants_set_window"])
            if wants_set_window:
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    x_min = st.number_input("Enter X-min", value=st.session_state.window_size["xmin"])
                with col2:
                    x_max = st.number_input("Enter X-max", value=st.session_state.window_size["xmax"])
                with col3:
                    y_min = st.number_input("Enter Y-min", value=st.session_state.window_size["ymin"])
                with col4:
                    y_max = st.number_input("Enter Y-max", value=st.session_state.window_size["ymax"])

        else:
            wants_set_window = False
            has_y_int = False
            y_int = None

        with st.form(key="form", border=False):
            if graph_type[0] == "line graph":
                wants_upper_trendline = st.checkbox("Endable upper trendline", value=st.session_state.trendlines["upper"])
                wants_average_trendline = st.checkbox("Enable average trendline", value=st.session_state.trendlines["average"])
                wants_lower_trendline = st.checkbox("Enable lower trendline", value=st.session_state.trendlines["lower"])
                wants_legend = st.checkbox("Enable legend", value=st.session_state.checkboxes["legend"])

            title = st.text_input("Title for graph", value=st.session_state.labels["title"])
            y_label = st.text_input("Y-axis label", value=st.session_state.labels["y_label"])
            x_label = st.text_input("X-axis label", value=st.session_state.labels["x_label"])

            if st.form_submit_button("Create Graph"):
                st.session_state.checkboxes = {"has_y_int": has_y_int, "y_int": y_int, "legend": wants_legend if graph_type[0] == "line graph" else False , "wants_set_window": wants_set_window}
                st.session_state.window_size = {"xmin": x_min, "xmax": x_max, "ymin": y_min, "ymax": y_max} if graph_type[0] == "line graph" and wants_set_window else {"xmin": 0.0, "xmax": None, "ymin": 0.0, "ymax": None}
                st.session_state.titles = {"title": title, "x_label": x_label, "y_label": y_label}
                st.session_state.df = data_table
                st.session_state.graph_type = graph_type[0]
                st.session_state.trendlines = {"upper": wants_upper_trendline, "lower": wants_lower_trendline, "average": wants_average_trendline} if graph_type[0] == "line graph" else {"upper": False, "lower": False, "average": False}
                st.switch_page("pages/graph_page.py")
    except ValueError:
        st.error("Please select a graph type")

def create_graph():
    if graph_type == "bar graph":
        create_bar_graph(labels=labels, df=df)
    elif previous_lines.keys() != [None, None, None]:
        load_user_graph(df=df, labels=labels, previous_lines=previous_lines, checkboxes=checkboxes, trendlines=trendlines, window_size=window_size)
    elif checkboxes["has_y_int"]:
        create_graph_w_y_int(df=df, labels=labels, checkboxes=checkboxes, trendlines=trendlines, window_size=window_size)
    else:
        create_graph_wo_y_int(labels=labels, df=df, checkboxes=checkboxes, trendlines=trendlines, window_size=window_size)

form_questions()

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

            st.write(f"Graph Id: {graph["id"]}")
            create_graph()


except AssertionError:
    pass
except HTTPException:
    st.error("Could not retrieve graphs")



