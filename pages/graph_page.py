import streamlit as st
from app.graph_utilities import create_graph_w_y_int, create_bar_graph, create_graph_wo_y_int, create_graph_from_user

API_URL = st.secrets["API_URL"]

st.title("Graph Page")

cookie = st.session_state.session.cookies.get_dict()

dataframe = st.session_state.df
graph_type = st.session_state.graph_type
checkboxes = st.session_state.checkboxes
labels = st.session_state.labels
wants_trendlines = st.session_state.trendlines
window_size = st.session_state.window_size

def save_graph():
    if st.session_state.save_graph_button:
        data_dict = {
            "labels": labels,
            "graph_type": graph_type,
            "df": dataframe.to_dict(orient="records"),
            "checkboxes": checkboxes,
            "trendlines": wants_trendlines,
            "window_size": window_size,
            "previous_lines": {"upper": None, "average": None, "lower": None}
        }
    else:
        data_dict = {
            "labels": labels,
            "graph_type": graph_type,
            "df": dataframe.to_dict(orient="records"),
            "checkboxes": checkboxes,
            "trendlines": wants_trendlines,
            "window_size": window_size,
            "previous_lines": st.session_state.previous_lines
        }

    response = st.session_state.session.post(API_URL + "/upload", json=data_dict, cookies=cookie)

    if response.status_code == 200:
        st.success("successfully uploaded graph")
        st.session_state.previous_lines = {"upper": None, "average": None, "lower": None}
    else:
        st.error(response.text)

def show_graphs():
    try:
        if not len(dataframe["x"]) >= 2 and not len(dataframe["y"]) >= 2:
            raise ValueError

        if checkboxes["has_y_int"] and graph_type == "line graph":
            try:
                create_graph_w_y_int(df=dataframe, labels=labels, checkboxes=checkboxes, trendlines=st.session_state.trendlines, window_size=window_size)
                if st.session_state.user:
                    st.button("Save Graph", on_click=save_graph, key="save_graph_button")
            except (SyntaxError, TypeError):
                st.error("please enter a valid y-int")
        elif graph_type == "line graph":
            create_graph_wo_y_int(df=dataframe, labels=labels, checkboxes=checkboxes, trendlines=st.session_state.trendlines, window_size=window_size)
            if st.session_state.user:
                st.button("Save Graph", on_click=save_graph, key="save_graph_button")
        else:
            create_bar_graph(df=dataframe, labels=labels)
            if st.session_state.user:
                st.button("Save Graph", on_click=save_graph, key="save_graph_button")

    except ValueError:
        st.error("please ensure you have at least 2 data points")
    except Exception as e:
        st.error(e)
        st.error("please ensure you have filled out all the squares on the table")


show_graphs()
try:
    if graph_type != "line graph":
        raise ValueError

    if not wants_trendlines["upper"]:
        st.subheader("Upper Trendline")
        col1, col2, col3 = st.columns(3)
        with col1:
            slope = st.number_input("Enter Slope Value", key="upper_slope")
        with col2:
            y_int = st.number_input("Enter y-intercept", key="upper_intercept")
        with col3:
            enter = st.button("Enter", key="upper_enter")

    if not wants_trendlines["average"]:
        st.subheader("Average Trendline")
        col1, col2, col3 = st.columns(3)
        with col1:
            slope = st.number_input("Enter Slope Value", key="average_slope")
        with col2:
            y_int = st.number_input("Enter y-intercept", key="average_intercept")
        with col3:
            enter = st.button("Enter", key="average_enter")

    if not wants_trendlines["lower"]:
        st.subheader("Lower Trendline")
        col1, col2, col3 = st.columns(3)
        with col1:
            slope = st.number_input("Enter Slope Value", key="lower_slope")
        with col2:
            y_int = st.number_input("Enter y-intercept", key="lower_intercept")
        with col3:
            enter = st.button("Enter", key="lower_enter")

    if st.session_state.upper_enter:
        st.subheader("Edited Graph")
        graph_attributes = {"slope": st.session_state.upper_slope, "y_int": st.session_state.upper_intercept}
        create_graph_from_user(df=dataframe, labels=labels, wants_legend=checkboxes["legend"],  graph_attributes=graph_attributes, trendlines=wants_trendlines, checkboxes=checkboxes, window_size=window_size)
        if st.session_state.user:
            st.button("Save Edited Graph", on_click=save_graph)
    elif st.session_state.average_enter:
        st.subheader("Edited Graph")
        graph_attributes = {"slope": st.session_state.average_slope, "y_int": st.session_state.average_intercept}
        create_graph_from_user(df=dataframe, labels=labels, wants_legend=checkboxes["legend"], graph_attributes=graph_attributes, trendlines=wants_trendlines, checkboxes=checkboxes, window_size=window_size)
        if st.session_state.user:
            st.button("Save Edited Graph", on_click=save_graph)
    elif st.session_state.lower_enter:
        st.subheader("Edited Graph")
        graph_attributes = {"slope": st.session_state.lower_slope, "y_int": st.session_state.lower_intercept}
        create_graph_from_user(df=dataframe, labels=labels, wants_legend=checkboxes["legend"], graph_attributes=graph_attributes, trendlines=wants_trendlines, checkboxes=checkboxes, window_size=window_size)
        if st.session_state.user:
            st.button("Save Edited Graph", on_click=save_graph)

except ValueError:
    pass