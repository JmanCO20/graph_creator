import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

df = st.session_state.df
y_int = st.session_state.y_int
title = st.session_state.title
x_label = st.session_state.x_label
y_label = st.session_state.y_label
has_y_int = st.session_state.has_y_int
graph_type = st.session_state.graph_type

def create_average_line(yint: int, x, y):
    if has_y_int:
        denom = np.sum(x ** 2)
        if denom == 0:
            m = 0.0
        else:
            m = np.sum(x * (y - yint)) / denom

        x_line = np.linspace(0, x.max(), 200)
        y_line = m * x_line + yint
        return x_line, y_line, round(m, 2)
    else:
        m, b = np.polyfit(x, y, 1)
        x_line = np.linspace(0, x.max(), 200)
        y_line = m * x_line + b
        return x_line, y_line, round(m, 2), round(b, 2)


def create_graph_w_y_int():

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
    x_line, y_line, m = create_average_line(y_int, x, y)
    ax.plot(x_line, y_line, color="blue", label=f"y = {m:.3g}x + {y_int:.3g}")

    upper_bound = df["y"] + df["y uncertainty"]
    upper_bound = upper_bound.to_numpy()

    ax.scatter(x=x, y=upper_bound, color="orange", alpha=0.8)


    x_line, y_line, m = create_average_line(y_int, x, upper_bound)
    ax.plot(x_line, y_line, color="orange", label=f"y = {m:.3g}x + {y_int:.3g}")

    lower_bound = df["y"] - df["y uncertainty"]
    lower_bound = lower_bound.to_numpy()

    ax.scatter(x=x, y=lower_bound, color="grey", alpha=0.8)

    x_line, y_line, m = create_average_line(y_int, x, lower_bound)
    ax.plot(x_line, y_line, color="grey", label=f"y = {m:.3g}x + {y_int:.3g}")

    ax.legend()
    st.pyplot(fig)

def create_graph_wo_y_int():

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

    x_line, y_line, m, b = create_average_line(y_int, x, y)
    ax.plot(x_line, y_line, color="blue", label=f"y = {m:.3g}x + {b:.3g}")

    upper_bound = df["y"] + df["y uncertainty"]

    ax.scatter(x=x, y=upper_bound, color="orange", alpha=0.8)

    lower_bound = df["y"] - df["y uncertainty"]

    ax.scatter(x=x, y=lower_bound, color="grey", alpha=0.8)

    half_of_upper = len(upper_bound)//2
    half_of_lower = len(lower_bound) - half_of_upper

    points_for_upper_bound = pd.concat([upper_bound[:half_of_upper], lower_bound[half_of_upper:half_of_lower + half_of_upper + 1]])
    points_for_upper_bound = points_for_upper_bound.to_numpy()

    x_line, y_line, m, b = create_average_line(y_int, x, points_for_upper_bound)
    ax.plot(x_line, y_line, color="orange", label=f"y = {m:.3g}x + {b:.3g}")

    points_for_lower_bound = pd.concat([lower_bound[:half_of_lower], upper_bound[half_of_lower:half_of_upper + half_of_lower + 1]], ignore_index=True)
    points_for_lower_bound = points_for_lower_bound.to_numpy()

    x_line, y_line, m, b = create_average_line(y_int, x, points_for_lower_bound)
    ax.plot(x_line, y_line, color="grey", label=f"y = {m:.3g}x + {b:.3g}")

    ax.legend()
    st.pyplot(fig)

def create_bar_graph():
    fig, ax = plt.subplots()

    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)

    x = df["x"].to_numpy()
    y = df["y"].to_numpy()

    ax.bar(x=x, height=y, color="blue", alpha=0.8)
    ax.errorbar(x=x, y=y, xerr=None, yerr=df["y uncertainty"], fmt="none", linestyle="none", color="grey", alpha=0.5)

    st.pyplot(fig)

try:
    if not len(df["x"]) >= 2 and not len(df["y"]) >= 2:
        raise ValueError

    if st.session_state.has_y_int and graph_type == "line graph":
        try:
            create_graph_w_y_int()
        except (SyntaxError, TypeError):
            st.error("please enter a valid y-int")
    elif graph_type == "line graph":
        create_graph_wo_y_int()
    else:
        create_bar_graph()

except ValueError:
    st.error("please ensure you have at least 2 data points")
except Exception as e:
    print(e)
    st.error("please ensure you have filled out all the squares on the table")