import numpy as np
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def create_average_line(has_y_int, y_int: int, x, y, window_size: dict[str, float]):
    if has_y_int:
        denom = np.sum(x ** 2)
        if denom == 0:
            m = 0.0
        else:
            m = np.sum(x * (y - y_int)) / denom

        x_line = np.linspace(0, window_size["xmax"], 300)
        y_line = m * x_line + y_int
        return x_line, y_line, round(m, 2)
    else:
        m, b = np.polyfit(x, y, 1)
        x_line = np.linspace(0, window_size["xmax"], 300)
        y_line = m * x_line + b
        return x_line, y_line, round(m, 2), round(b, 2)

def creating_trendlines(trendlines: dict[str, bool], checkboxes: dict[str, bool | float], ax: plt.Axes, x, y, upper_bound, lower_bound, window_size: dict[str, float], half_of_upper: int | None=None, half_of_lower: int | None=None):
    try:
        if not checkboxes["has_y_int"]:
            raise ValueError
        if trendlines["average"]:
            x_line, y_line, m = create_average_line(checkboxes["has_y_int"], checkboxes["y_int"], x, y, window_size)
            st.session_state.previous_lines["average"] = None
            ax.plot(x_line, y_line, color="blue", label=f"y = {m:.3g}x + {checkboxes["y_int"]:.3g}")
        if trendlines["upper"]:
            x_line, y_line, m = create_average_line(checkboxes["has_y_int"], checkboxes["y_int"], x, upper_bound, window_size)
            st.session_state.previous_lines["upper"] = None
            ax.plot(x_line, y_line, color="orange", label=f"y = {m:.3g}x + {checkboxes["y_int"]:.3g}")
        if trendlines["lower"]:
            x_line, y_line, m = create_average_line(checkboxes["has_y_int"], checkboxes["y_int"], x, lower_bound, window_size)
            st.session_state.previous_lines["lower"] = None
            ax.plot(x_line, y_line, color="grey", label=f"y = {m:.3g}x + {checkboxes["y_int"]:.3g}")
    except ValueError:
        pass

    try:
        if checkboxes["has_y_int"]:
            raise ValueError
        if trendlines["average"]:
            x_line, y_line, m, b = create_average_line(checkboxes["has_y_int"], checkboxes["y_int"], x, y, window_size)
            st.session_state.previous_lines["average"] = None
            ax.plot(x_line, y_line, color="blue", label=f"y = {m:.3g}x + {b:.3g}")

        if trendlines["upper"]:
            points_for_upper_bound = pd.concat([upper_bound[:half_of_upper], lower_bound[half_of_upper:half_of_lower + half_of_upper + 1]])
            st.session_state.previous_lines["upper"] = None
            points_for_upper_bound = points_for_upper_bound.to_numpy()

            x_line, y_line, m, b = create_average_line(checkboxes["has_y_int"], checkboxes["y_int"], x, points_for_upper_bound, window_size)
            ax.plot(x_line, y_line, color="orange", label=f"y = {m:.3g}x + {b:.3g}")

        if trendlines["lower"]:
            points_for_lower_bound = pd.concat( [lower_bound[:half_of_lower], upper_bound[half_of_lower:half_of_upper + half_of_lower + 1]], ignore_index=True)
            st.session_state.previous_lines["lower"] = None
            points_for_lower_bound = points_for_lower_bound.to_numpy()

            x_line, y_line, m, b = create_average_line(checkboxes["has_y_int"], checkboxes["y_int"], x, points_for_lower_bound, window_size)
            ax.plot(x_line, y_line, color="grey", label=f"y = {m:.3g}x + {b:.3g}")
    except ValueError:
        pass


def create_graph_w_y_int(df, labels: dict[str, str], checkboxes: dict[str, bool | float], trendlines: dict[str, bool], window_size: dict[str, float]):

    fig, ax = plt.subplots()

    ax.set_title(labels["title"])
    ax.set_xlabel(labels["x_label"])
    ax.set_ylabel(labels["y_label"])

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

    upper_bound = df["y"] + df["y uncertainty"]
    upper_bound = upper_bound.to_numpy()

    lower_bound = df["y"] - df["y uncertainty"]
    lower_bound = lower_bound.to_numpy()

    ax.scatter(x=x, y=upper_bound, color="orange", alpha=0.8)
    ax.scatter(x=x, y=lower_bound, color="grey", alpha=0.8)

    creating_trendlines(trendlines=trendlines,
                        checkboxes=checkboxes,
                        ax=ax,
                        x=x,
                        y=y,
                        upper_bound=upper_bound,
                        lower_bound=lower_bound,
                        window_size=window_size
                        )

    if checkboxes["wants_set_window"]:
        ax.set_xlim(left=window_size["xmin"], right=window_size["xmax"])
        ax.set_ylim(bottom=window_size["ymin"], top=window_size["ymax"])

    if checkboxes["legend"]:
        ax.legend()

    st.pyplot(fig)

def create_graph_wo_y_int(labels: dict[str, str], df, checkboxes: dict[str, bool | float], trendlines: dict[str, bool], window_size: dict[str, float]):

    fig, ax = plt.subplots()

    ax.set_title(labels["title"])
    ax.set_xlabel(labels["x_label"])
    ax.set_ylabel(labels["y_label"])

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

    upper_bound = df["y"] + df["y uncertainty"]
    lower_bound = df["y"] - df["y uncertainty"]

    ax.scatter(x=x, y=upper_bound, color="orange", alpha=0.8)
    ax.scatter(x=x, y=lower_bound, color="grey", alpha=0.8)

    half_of_upper = len(upper_bound)//2
    half_of_lower = len(lower_bound) - half_of_upper

    creating_trendlines(trendlines=trendlines,
                        checkboxes=checkboxes,
                        ax=ax,
                        x=x,
                        y=y,
                        upper_bound=upper_bound,
                        lower_bound=lower_bound,
                        half_of_upper=half_of_upper,
                        half_of_lower=half_of_lower,
                        window_size=window_size
                        )

    if checkboxes["wants_set_window"]:
        ax.set_xlim(left=window_size["xmin"], right=window_size["xmax"])
        ax.set_ylim(bottom=window_size["ymin"], top=window_size["ymax"])

    if checkboxes["legend"]:
        ax.legend()

    st.pyplot(fig)


def create_bar_graph(labels: dict[str, str], df):
    fig, ax = plt.subplots()

    ax.set_title(labels["title"])
    ax.set_xlabel(labels["x_label"])
    ax.set_ylabel(labels["y_label"])

    x = df["x"].to_numpy()
    y = df["y"].to_numpy()

    ax.bar(x=x, height=y, color="blue", alpha=0.8)
    ax.errorbar(x=x, y=y, xerr=None, yerr=df["y uncertainty"], fmt="none", linestyle="none", color="grey", alpha=0.5)

    st.pyplot(fig)

def draw_lines(previous_lines: dict[str, tuple], ax: plt.Axes, window_size: dict[str, float]):
    for key in previous_lines.keys():
        if previous_lines[key] is not None:
            x_line = np.linspace(0, window_size["xmax"], 200)
            y_line = previous_lines[key][0] * x_line + previous_lines[key][1]
            ax.plot(x_line, y_line, color=previous_lines[key][2], label=f"y = {previous_lines[key][0]:.3g}x + {previous_lines[key][1]:.3g}")

def load_user_graph(df, labels: dict[str, str], previous_lines: dict[str, tuple], checkboxes: dict[str, bool | float], trendlines: dict[str, bool], window_size: dict[str, float]):
    fig, ax = plt.subplots()

    ax.set_title(labels["title"])
    ax.set_xlabel(labels["x_label"])
    ax.set_ylabel(labels["y_label"])

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

    upper_bound = df["y"] + df["y uncertainty"]
    lower_bound = df["y"] - df["y uncertainty"]

    if checkboxes["has_y_int"]:
        upper_bound = upper_bound.to_numpy()
        lower_bound = lower_bound.to_numpy()
    else:
        half_of_upper = len(upper_bound) // 2
        half_of_lower = len(lower_bound) - half_of_upper

    ax.scatter(x=x, y=upper_bound, color="orange", alpha=0.8)
    ax.scatter(x=x, y=lower_bound, color="grey", alpha=0.8)

    creating_trendlines(trendlines=trendlines,
                        checkboxes=checkboxes,
                        ax=ax,
                        x=x,
                        y=y,
                        upper_bound=upper_bound,
                        lower_bound=lower_bound,
                        half_of_upper=half_of_upper if not checkboxes["has_y_int"] else None,
                        half_of_lower=half_of_lower if not checkboxes["has_y_int"] else None,
                        window_size=window_size
                        )

    draw_lines(previous_lines, ax, window_size)

    if checkboxes["wants_set_window"]:
        ax.set_xlim(left=window_size["xmin"], right=window_size["xmax"])
        ax.set_ylim(bottom=window_size["ymin"], top=window_size["ymax"])

    if checkboxes["legend"]:
        ax.legend()

    st.pyplot(fig)

def create_graph_from_user(df, labels: dict[str, str], wants_legend: bool, graph_attributes: dict[str, float], trendlines: dict[str, bool], checkboxes: dict[str, bool | float], window_size: dict[str, float]):

    fig, ax = plt.subplots()

    ax.set_title(labels["title"])
    ax.set_xlabel(labels["x_label"])
    ax.set_ylabel(labels["y_label"])

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
    upper_bound = df["y"] + df["y uncertainty"]
    lower_bound = df["y"] - df["y uncertainty"]

    if checkboxes["has_y_int"]:
        upper_bound = upper_bound.to_numpy()
        lower_bound = lower_bound.to_numpy()
    else:
        half_of_upper = len(upper_bound) // 2
        half_of_lower = len(lower_bound) - half_of_upper

    ax.scatter(x=x, y=upper_bound, color="orange", alpha=0.8)
    ax.scatter(x=x, y=lower_bound, color="grey", alpha=0.8)

    creating_trendlines(trendlines=trendlines,
                        checkboxes=checkboxes,
                        ax=ax,
                        x=x,
                        y=y,
                        upper_bound=upper_bound,
                        lower_bound=lower_bound,
                        half_of_upper=half_of_upper if not checkboxes["has_y_int"] else None,
                        half_of_lower=half_of_lower if not checkboxes["has_y_int"] else None,
                        window_size=window_size
                        )

    if st.session_state.upper_enter:
        st.session_state.previous_lines["upper"] = [graph_attributes["slope"], graph_attributes["y_int"], "orange"]
        draw_lines(st.session_state.previous_lines, ax, window_size)

    if st.session_state.average_enter:
        st.session_state.previous_lines["average"] = [graph_attributes["slope"], graph_attributes["y_int"], "blue"]
        draw_lines(st.session_state.previous_lines, ax, window_size)

    if st.session_state.lower_enter:
        st.session_state.previous_lines["lower"] = [graph_attributes["slope"], graph_attributes["y_int"], "grey"]
        draw_lines(st.session_state.previous_lines, ax, window_size)

    if checkboxes["wants_set_window"]:
        ax.set_xlim(left=window_size["xmin"], right=window_size["xmax"])
        ax.set_ylim(bottom=window_size["ymin"], top=window_size["ymax"])

    if wants_legend:
        ax.legend()

    st.pyplot(fig)