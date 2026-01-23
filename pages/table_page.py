import streamlit as st
import pandas as pd

def table_view():
    if "df" not in st.session_state:
        st.session_state.df = pd.DataFrame({
            "x": pd.Series(dtype=float),
            "x uncertainty": pd.Series(dtype=float),
            "y": pd.Series(dtype=float),
            "y uncertainty": pd.Series(dtype=float)
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

    data_table = table_view()

    st.session_state.has_y_int = st.checkbox("does your graph have a set y-int", value=st.session_state.has_y_int)
    if st.session_state.has_y_int:
        st.session_state.y_int = st.number_input("y-int", value=st.session_state.y_int)
        st.session_state.has_y_int = True

    with st.form(key="form", border=False):

        title = st.text_input("Title for graph", value=st.session_state.title)

        y_label = st.text_input("y-axis label", value=st.session_state.y_label)

        x_label = st.text_input("x-axis label", value=st.session_state.x_label)


        if st.form_submit_button("Create Graph"):
            st.session_state.y_int = st.session_state.y_int if st.session_state.has_y_int else None
            st.session_state.has_y_int = st.session_state.has_y_int
            st.session_state.title = title
            st.session_state.y_label = y_label
            st.session_state.x_label = x_label
            st.session_state.df = data_table
            st.switch_page("pages/graph_page.py")


form_questions()


