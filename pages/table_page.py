import streamlit as st
import pandas as pd

if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=["x", "x uncertainty", "y", "y uncertainty"])

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


form_questions()


