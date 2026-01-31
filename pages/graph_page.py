import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()
API_URL = os.getenv("API_URL")

st.title("Graph Page")



dataframe = st.session_state.df
y_intercept = st.session_state.y_int
graph_title = st.session_state.title
graph_x_label = st.session_state.x_label
graph_y_label = st.session_state.y_label
graph_has_y_int = st.session_state.has_y_int
graph_type = st.session_state.graph_type

session = st.session_state.session

def create_average_line(has_y_int, y_int: int, x, y):
    if has_y_int:
        denom = np.sum(x ** 2)
        if denom == 0:
            m = 0.0
        else:
            m = np.sum(x * (y - y_int)) / denom

        x_line = np.linspace(0, x.max(), 200)
        y_line = m * x_line + y_int
        return x_line, y_line, round(m, 2)
    else:
        m, b = np.polyfit(x, y, 1)
        x_line = np.linspace(0, x.max(), 200)
        y_line = m * x_line + b
        return x_line, y_line, round(m, 2), round(b, 2)


def create_graph_w_y_int(df, title: str, x_label:str, y_label:str, y_int:int, has_y_int: bool):

    fig, ax = plt.subplots()

    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)

    x = df["x"].to_numpy()
    y = df["y"].to_numpy()

    ax.scatter(x=x, y=y, color="blue", alpha=0.8)
    ax.errorbar(xerr=df["x uncertainty"],
                yerr=df["y uncertainty"],
                x=x,
                y=y,
                fmt="none",
                linestyle="none",
                color="grey",
                alpha=0.35
                )
    x_line, y_line, m = create_average_line(has_y_int, y_int, x, y)
    ax.plot(x_line, y_line, color="blue", label=f"y = {m:.3g}x + {y_int:.3g}")

    upper_bound = df["y"] + df["y uncertainty"]
    upper_bound = upper_bound.to_numpy()

    ax.scatter(x=x, y=upper_bound, color="orange", alpha=0.8)


    x_line, y_line, m = create_average_line(has_y_int, y_int, x, upper_bound)
    ax.plot(x_line, y_line, color="orange", label=f"y = {m:.3g}x + {y_int:.3g}")

    lower_bound = df["y"] - df["y uncertainty"]
    lower_bound = lower_bound.to_numpy()

    ax.scatter(x=x, y=lower_bound, color="grey", alpha=0.8)

    x_line, y_line, m = create_average_line(has_y_int, y_int, x, lower_bound)
    ax.plot(x_line, y_line, color="grey", label=f"y = {m:.3g}x + {y_int:.3g}")

    ax.legend()
    st.pyplot(fig)

def create_graph_wo_y_int(title:str, x_label:str, y_label:str, df, has_y_int: bool, y_int: int | None=None,):

    fig, ax = plt.subplots()

    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)

    x = df["x"].to_numpy()
    y = df["y"].to_numpy()

    ax.scatter(x=x, y=y, color="blue", alpha=0.8)
    ax.errorbar(xerr=df["x uncertainty"],
                yerr=df["y uncertainty"],
                x=x,
                y=y,
                fmt="none",
                linestyle="none",
                color="grey",
                alpha=0.35
                )

    x_line, y_line, m, b = create_average_line(has_y_int, y_int, x, y)
    ax.plot(x_line, y_line, color="blue", label=f"y = {m:.3g}x + {b:.3g}")

    upper_bound = df["y"] + df["y uncertainty"]

    ax.scatter(x=x, y=upper_bound, color="orange", alpha=0.8)

    lower_bound = df["y"] - df["y uncertainty"]

    ax.scatter(x=x, y=lower_bound, color="grey", alpha=0.8)

    half_of_upper = len(upper_bound)//2
    half_of_lower = len(lower_bound) - half_of_upper

    points_for_upper_bound = pd.concat([upper_bound[:half_of_upper], lower_bound[half_of_upper:half_of_lower + half_of_upper + 1]])
    points_for_upper_bound = points_for_upper_bound.to_numpy()

    x_line, y_line, m, b = create_average_line(has_y_int, y_int, x, points_for_upper_bound)
    ax.plot(x_line, y_line, color="orange", label=f"y = {m:.3g}x + {b:.3g}")

    points_for_lower_bound = pd.concat([lower_bound[:half_of_lower], upper_bound[half_of_lower:half_of_upper + half_of_lower + 1]], ignore_index=True)
    points_for_lower_bound = points_for_lower_bound.to_numpy()

    x_line, y_line, m, b = create_average_line(has_y_int, y_int, x, points_for_lower_bound)
    ax.plot(x_line, y_line, color="grey", label=f"y = {m:.3g}x + {b:.3g}")

    ax.legend()
    st.pyplot(fig)


def create_bar_graph(title, x_label, y_label, df):
    fig, ax = plt.subplots()

    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)

    x = df["x"].to_numpy()
    y = df["y"].to_numpy()

    ax.bar(x=x, height=y, color="blue", alpha=0.8)
    ax.errorbar(x=x, y=y, xerr=None, yerr=df["y uncertainty"], fmt="none", linestyle="none", color="grey", alpha=0.5)

    st.pyplot(fig)

def save_graph():
    data_dict = {
        "title": graph_title,
        "graph_type": graph_type,
        "df": dataframe.to_dict(orient="records"),
        "x_label": graph_x_label,
        "y_label": graph_y_label,
        "has_y_int": graph_has_y_int,
        "y_int": y_intercept
    }

    response = session.post(API_URL + "/upload", json=data_dict)

    if response.status_code == 200:
        st.success("successfully uploaded graph")
    else:
        st.error(response.text)

try:
    if not len(dataframe["x"]) >= 2 and not len(dataframe["y"]) >= 2:
        raise ValueError

    if st.session_state.has_y_int and graph_type == "line graph":
        try:
            create_graph_w_y_int(df=dataframe, title=graph_title, x_label=graph_x_label, y_label=graph_y_label, y_int=y_intercept, has_y_int=graph_has_y_int)
            if st.session_state.user:
                st.button("Save Graph", on_click=save_graph)
        except (SyntaxError, TypeError):
            st.error("please enter a valid y-int")
    elif graph_type == "line graph":
        create_graph_wo_y_int(df=dataframe, title=graph_title, x_label=graph_x_label, y_label=graph_y_label, has_y_int=graph_has_y_int)
        if st.session_state.user:
            st.button("Save Graph", on_click=save_graph)
    else:
        create_bar_graph(df=dataframe, title=graph_title, x_label=graph_x_label, y_label=graph_y_label)
        if st.session_state.user:
            st.button("Save Graph", on_click=save_graph)

except ValueError:
    st.error("please ensure you have at least 2 data points")
except Exception as e:
    st.error("please ensure you have filled out all the squares on the table")