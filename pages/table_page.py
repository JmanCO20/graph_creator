import streamlit as st
import pandas as pd

API_URL = st.secrets["API_URL"]

cookie = st.session_state.session.cookies.get_dict()

st.title("Table Page")

if st.session_state.graph_update["update"]:
    response = st.session_state.session.get(API_URL + f"/user/update/{st.session_state.graph_update["graph_id"]}", cookies=cookie)
    if response.status_code == 200:
        graphs = response.json()
        st.session_state.labels["frontend"] = graphs["data"]["labels"]
        st.session_state.df = pd.DataFrame(graphs["data"]["df"])
        st.session_state.graph_type = graphs["graph_type"]
        st.session_state.checkboxes["frontend"] = graphs["data"]["checkboxes"]
        st.session_state.trendlines["frontend"] = graphs["data"]["trendlines"]
        st.session_state.window_size["frontend"] = graphs["data"]["window_size"]
        st.session_state.previous_lines = graphs["data"]["previous_lines"]
        st.session_state.sig_figs["frontend"] = graphs["data"]["sig_figs"]
        st.session_state.graph_update["update"] = False

def table_view_for_graphs(graph_type: str = "line graph"):
    if graph_type == "line graph":
        df = st.session_state.df[["x", "x uncertainty", "y", "y uncertainty"]]
    else:
        df = st.session_state.df[["x", "y", "y uncertainty"]]

    df.reset_index(drop=True)
    return df

def form_questions():
    try:
        graph_type = st.multiselect(label="Select if you are making a Bar graph or Line graph", options=["line graph", "bar graph"], max_selections=1, default=st.session_state.graph_type)

        if not graph_type:
            raise ValueError

        dataframe = table_view_for_graphs(graph_type[0])

        st.session_state.df_copy = st.data_editor(
            dataframe.reset_index(drop=True),
            key="editable_table",
            num_rows="dynamic",
            hide_index=True)

        st.session_state.labels["values"]["title"] = st.text_input("Title for graph", value=st.session_state.labels["frontend"]["title"])
        st.session_state.labels["values"]["y_label"] = st.text_input("Y-axis label", value=st.session_state.labels["frontend"]["y_label"])
        st.session_state.labels["values"]["x_label"] = st.text_input("X-axis label", value=st.session_state.labels["frontend"]["x_label"])

        if graph_type[0] == "line graph":
            has_y_int = st.checkbox("Does your graph have a set Y Intercept", value=st.session_state.checkboxes["frontend"]["has_y_int"])
            if has_y_int:
                y_int = st.number_input("Enter Y Intercept value", value=st.session_state.checkboxes["frontend"]["y_int"])
            else:
                y_int = None

            st.session_state.sig_figs["values"] = st.number_input("Enter number of sig figs", value=st.session_state.sig_figs["frontend"])

            st.session_state.trendlines["values"]["upper"] = st.checkbox("Endable upper trendline", value=st.session_state.trendlines["frontend"]["upper"])
            st.session_state.trendlines["values"]["average"] = st.checkbox("Enable average trendline", value=st.session_state.trendlines["frontend"]["average"])
            st.session_state.trendlines["values"]["lower"] = st.checkbox("Enable lower trendline", value=st.session_state.trendlines["frontend"]["lower"])
            wants_legend = st.checkbox("Enable legend", value=st.session_state.checkboxes["frontend"]["legend"])

            wants_set_window = st.checkbox("Set graph window size", value=st.session_state.checkboxes["frontend"]["wants_set_window"])
            if wants_set_window:
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    x_min = st.number_input("Enter X-min", value=st.session_state.window_size["frontend"]["xmin"])
                with col2:
                    x_max = st.number_input("Enter X-max", value=st.session_state.window_size["frontend"]["xmax"])
                with col3:
                    y_min = st.number_input("Enter Y-min", value=st.session_state.window_size["frontend"]["ymin"])
                with col4:
                    y_max = st.number_input("Enter Y-max", value=st.session_state.window_size["frontend"]["ymax"])

        else:
            wants_set_window = False
            has_y_int = False
            y_int = None
            st.session_state.trendlines["values"]["upper"] = False
            st.session_state.trendlines["values"]["lower"] = False
            st.session_state.trendlines["values"]["average"] = False
            wants_legend = False

        st.session_state.checkboxes["values"] = {"has_y_int": has_y_int, "y_int": y_int, "legend": wants_legend if graph_type[0] == "line graph" else False , "wants_set_window": wants_set_window}
        st.session_state.window_size["values"] = {"xmin": x_min, "xmax": x_max, "ymin": y_min, "ymax": y_max} if graph_type[0] == "line graph" and wants_set_window else {"xmin": 0.0, "xmax": None, "ymin": 0.0, "ymax": None}
        st.session_state.graph_type = graph_type[0]
        if st.button("Submit"):
            st.switch_page("pages/graph_page.py")
    except ValueError:
        st.error("Please select a graph type")

form_questions()



