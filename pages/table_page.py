import streamlit as st
import pandas as pd
from pages.graph_page import create_graph_w_y_int, create_bar_graph, create_graph_wo_y_int
from dotenv import load_dotenv
import os
from fastapi import HTTPException

load_dotenv()
API_URL = os.getenv("API_URL")

session = st.session_state.session

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
        graph_type = st.multiselect(label="select if you are making a bar graph or line graph", options=["line graph", "bar graph"], max_selections=1, default=st.session_state.graph_type)

        if not graph_type:
            raise ValueError
        elif graph_type[0] == "line graph":
            column_type = float
        else:
            column_type = str

        data_table = table_view_for_graphs(column_type)
        if graph_type[0] == "line graph":
            has_y_int = st.checkbox("does your graph have a set y-int", value=st.session_state.has_y_int)
            if has_y_int:
                y_int = st.number_input("enter y-int", value=st.session_state.y_int)
        else:
            has_y_int = False


    except ValueError:
        st.error("please select a graph type")

    with st.form(key="form", border=False):

        title = st.text_input("Title for graph", value=st.session_state.title)

        y_label = st.text_input("y-axis label", value=st.session_state.y_label)

        x_label = st.text_input("x-axis label", value=st.session_state.x_label)


        if st.form_submit_button("Create Graph"):
            st.session_state.has_y_int = has_y_int
            st.session_state.y_int = y_int if st.session_state.has_y_int else None
            st.session_state.title = title
            st.session_state.y_label = y_label
            st.session_state.x_label = x_label
            st.session_state.df = data_table
            st.session_state.graph_type = graph_type[0]
            st.switch_page("pages/graph_page.py")

def create_graph():
    if has_y_int and graph_type == "line graph":
        try:
            create_graph_w_y_int(df=df, title=title, x_label=x_label, y_label=y_label, y_int=y_int, has_y_int=has_y_int)
        except (SyntaxError, TypeError) as e:
            st.error(e)
            st.error("please enter a valid y-int")
    elif graph_type == "line graph":
        create_graph_wo_y_int(title=title, x_label=x_label, y_label=y_label, df=df, has_y_int=has_y_int)
    else:
        create_bar_graph(title=title, x_label=x_label, y_label=y_label, df=df)

form_questions()

try:
    if not st.session_state.user:
        raise AssertionError
    st.header("Previous Graphs")

    response = session.get(API_URL + "/user/graphs")
    if response.status_code == 200:
        graphs = response.json()
    else:
        st.error(response.text)
        raise HTTPException(response.status_code)

    container = st.container(border=True)

    with container:
        for graph in graphs:
            title = graph["title"]
            graph_type = graph["graph_type"]
            x_label = graph["data"]["x_label"]
            y_label = graph["data"]["y_label"]
            has_y_int = graph["data"]["has_y_int"]
            y_int = graph["data"]["y_int"]
            df = pd.DataFrame(graph["data"]["df"])
            st.write(f"Graph Id: {graph["id"]}")
            create_graph()


except AssertionError:
    pass
except HTTPException:
    st.error("could not retrieve graphs")



