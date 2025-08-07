import matplotlib.pyplot as plt
from eupolis.utils import process_lst
from eupolis.config import COLORS
import numpy as np
from collections import defaultdict
from matplotlib import ticker
import re
import pandas as pd
from textwrap import wrap


def fmt_percent(x: int, pos) -> str:
    """Takes position and the text of the label and returns a label formatted in percentages.

    Parameters
    ----------
    x
        an integer denoting the label
    pos
        an integer denoting a position on axis

    Returns
    -------
        an string denoting percentages.
    """
    return f"{abs(x)}%"


def plot_barplot(
    dt_ord: dict,
    vertical_lines: list = [25, 50],
    ticks: list = [-50, -25, 0, 25, 50],
    colors: dict = COLORS,
    comparison: bool = False,
) -> plt.Figure:
    """Plots a histogram where bars are horizontal. The bars on the right are for men while the ones on the left for women.

    Parameters
    ----------
    dt_ord
        a dict with keys times of the day and values dictioanries with cohort name and list of frequencies
    colors, optional
        a dict with keys blue and green, by default COLORS
    vertical_lines, optional
        a list with coordinate of the vertical grid, by default [10, 50, 100]
    ticks, optional
        a list of ticks which should be visible on x axis

    Returns
    -------
        barplots for different age cohorts
    """
    fig, axs = plt.subplots(figsize=(3 * len(dt_ord), 4), nrows=1, ncols=len(dt_ord))
    fig.subplots_adjust(wspace=0.3, hspace=0.2, top=0.8, bottom=0.05)
    if len(dt_ord) == 1:
        axs_flat = [axs]
    else:
        axs_flat = axs.flat
    for ax, time in zip(axs_flat, dt_ord):
        dct = defaultdict(defaultdict)
        for _, values in dt_ord[time].items():
            for key, value in values.items():
                dct[key][_] = np.mean(value)

        y_m = [value["before"] for key, value in dct.items() if "_m" in key]
        y_f = [-value["before"] for key, value in dct.items() if "_f" in key]
        if comparison:
            y_m = [
                100 * value["after"] / value.get("before", 1)
                for key, value in dct.items()
                if "_m" in key
            ]
            y_f = [
                100 * (-value["after"]) / value.get("before", 1)
                for key, value in dct.items()
                if "_f" in key
            ]

        xlimit = max(abs(min(y_f)), max(y_m))
        x = {
            0: "Children",
            1: "Teenagers",
            2: "Young Adults",
            3: "Middle Aged",
            4: "Seniors",
        }

        ax.barh(x.keys(), y_m, color=colors["blue"])
        ax.barh(x.keys(), y_f, color=colors["green"])
        ax.set_xticks(ticks)
        ax.set_xticklabels([abs(tick) for tick in ticks])
        for spin in ax.spines:
            if spin != "bottom":
                ax.spines[spin].set_visible(False)
        ax.tick_params(axis="y", which="major", length=0)
        if time == "Morning":
            ax.set_yticks(list(x.keys()), list(x.values()))
        else:
            ax.set_yticks([])
        ax.axvline(x=0, color="white")
        ax.text(
            x=0.75,
            y=1,
            s="Men",
            horizontalalignment="center",
            verticalalignment="center",
            size=8,
            transform=ax.transAxes,
        )
        ax.text(
            x=0.25,
            y=1,
            s="Women",
            horizontalalignment="center",
            verticalalignment="center",
            size=8,
            transform=ax.transAxes,
        )
        for item in vertical_lines:
            ax.axvline(x=item, linestyle="--", color="darkgrey", linewidth=0.5)
            ax.axvline(x=-item, linestyle="--", color="darkgrey", linewidth=0.5)
        ax.set_title(time, horizontalalignment="center", y=1.01, size=10, weight="bold")
        ax.set_xlim(-xlimit - 5, xlimit + 5)
        if comparison:
            for label in ax.get_xticklabels():
                if value := float(label.get_text()) < 0:
                    label.set_text(f"{abs(value)}%")
            ax.xaxis.set_major_formatter(ticker.FuncFormatter(fmt_percent))
        else:
            for label in ax.get_xticklabels():
                if value := float(label.get_text()) < 0:
                    label.set_text(abs(value))
    return fig


def plot_groups(
    dt_ord: dict, colors: dict = COLORS, xlimit: int = 10, comparison: bool = False
) -> plt.Figure:
    """Plots barplots for groups.

    Parameters
    ----------
    dt_ord
        a dictionary where keys are groups and vlaues lists of frequencies
    colors, optional
        a dictionary with keys blue and green and values hexes of colors, by default COLORS
    xlimit, optional
        the upper limit of x axis, by default 10

    Returns
    -------
    barplots for times of the day
    """

    fig, axs = plt.subplots(figsize=(3 * len(dt_ord), 4), nrows=1, ncols=len(dt_ord))
    fig.subplots_adjust(wspace=0.3, hspace=0.2, top=0.8, bottom=0.05)
    if len(dt_ord) == 1:
        axs_flat = [axs]
    else:
        axs_flat = axs.flat
    for ax, time in zip(axs_flat, dt_ord):
        map_groups = {
            "family": "Family",
            "pram": "Person with children's pram",
            "group": "Group of people",
            "couple": "Couple",
            "pet": "Person walking a pet",
            "with_disabilities": "Person with disabilities",
            "non_white": "Non-white person",
            "bike": "Person on soft mobility",
            "other": "Other",
        }
        dct_mn = defaultdict(defaultdict)
        for _, values in dt_ord[time].items():
            for key, value in values.items():
                dct_mn[key][_] = np.mean(value)

        dct = {map_groups[key]: float(value["before"]) for key, value in dct_mn.items()}
        if comparison:
            dct = {
                map_groups[key]: 100 * float(value["after"]) / float(value["before"])
                for key, value in dct_mn.items()
            }

        dct = {key: value if value == value else 0 for key, value in dct.items()}
        if time != "Morning":
            ax.set_yticks([])
        for spin in ax.spines:
            if spin in ["top", "right"]:
                ax.spines[spin].set_visible(False)
        ax.barh(dct.keys(), dct.values(), color=colors["blue"])
        ax.set_title(time, horizontalalignment="center", y=1.01, size=10, weight="bold")
        ax.set_xlim(0, xlimit)
        if comparison:
            ax.set_xticks([0, 100, 200])
            for label in ax.get_xticklabels():
                if value := float(label.get_text()) < 0:
                    label.set_text(f"{abs(value)}%")
            ax.xaxis.set_major_formatter(ticker.FuncFormatter(fmt_percent))
        else:
            for label in ax.get_xticklabels():
                if value := float(label.get_text()) < 0:
                    label.set_text(abs(value))
    return fig


def plot_radar(
    dt_ord: dict, theta: np.array, colors: dict = COLORS, plot_between: bool = True
) -> plt.Figure:
    """Plots radar plots.

    Parameters
    ----------
    dt_ord
        a dictionary where keys are groups and vlaues lists of frequencies
    colors, optional
        a dictionary with keys blue and green and values hexes of colors, by default COLORS
    theta
        the result of radar_factory; it an array with coordinates in polar
    plot_between, optional
        whether to plot the range between min and max values, by default set to True

    Returns
    -------
        radar plots
    """
    fig, axs = plt.subplots(
        figsize=(3 * len(dt_ord), 4),
        nrows=1,
        ncols=len(dt_ord),
        subplot_kw=dict(projection="radar"),
    )
    fig.subplots_adjust(wspace=0.5, hspace=0.20, top=0.85, bottom=0.05)
    if len(dt_ord) == 1:
        axs_flat = [axs]
    else:
        axs_flat = axs.flat

    for ax, time in zip(axs_flat, dt_ord):
        ax.set_rgrids([1, 2, 3, 4, 5], size=0)
        ax.set_ylim(0, 5)
        ax.set_title(
            x=0.5,
            y=-0.3,
            label=time,
            weight="bold",
            size="medium",
            horizontalalignment="center",
            verticalalignment="center",
        )
        if len(dt_ord[time].keys()) < 2:
            ax.plot(
                theta,
                [np.mean(item) for item in dt_ord[time]["before"].values()],
                color=colors["blue"],
            )
            if plot_between:
                ax.fill_between(
                    theta,
                    process_lst(dt_ord[time]["before"].values(), min),
                    process_lst(dt_ord[time]["before"].values(), max),
                    facecolor=colors["blue"],
                    alpha=0.25,
                )
            for t, d in zip(
                theta, process_lst(dt_ord[time]["before"].values(), np.mean)
            ):
                ax.text(
                    t, d + 0.3, f"{d:.1f}", horizontalalignment="center", fontsize=6
                )
            ax.set_varlabels(
                dt_ord[time]["before"].keys(),
                kwargs={
                    "fontsize": 6,
                    "verticalalignment": "center",
                    "horizontalalignment": "center",
                },
            )
        else:
            ax.plot(
                theta,
                [np.mean(item) for item in dt_ord[time]["before"].values()],
                color=colors["blue"],
            )
            ax.plot(
                theta,
                [np.mean(item) for item in dt_ord[time]["after"].values()],
                color=colors["green"],
            )

            for t, b, a in zip(
                theta,
                process_lst(dt_ord[time]["before"].values(), np.mean),
                process_lst(dt_ord[time]["after"].values(), np.mean),
            ):
                ax.text(
                    t,
                    max(a, b) + 0.3,
                    f"{a - b:.1f}",
                    horizontalalignment="center",
                    fontsize=6,
                )
            ax.set_varlabels(
                dt_ord[time]["before"].keys(),
                kwargs={
                    "fontsize": 6,
                    "verticalalignment": "center",
                    "horizontalalignment": "center",
                },
            )
        for label in ax.get_xticklabels():
            if label.get_text() == "Multifunctionality":
                label.set_position([0, 0.12])
    return fig


def plot_kids_barhplot(
    df: pd.DataFrame,
    COLORS: dict = COLORS,
    labels_size: int = 10,
    male_n: int = 6,
    female_n: int = 10,
) -> plt.Figure:
    """Plots a horizontal bar plot for the data prepared by `prepare_data`.

    Parameters
    ----------
    df
        a data frame containing the data

    COLORS, optional
        a dictionary with keys blue and green and values hexes of colors, by default COLORS

    Returns
    -------
        a matplotlib figure object.
    """
    fig, axs = plt.subplots(figsize=(6, 4), nrows=1, ncols=2)
    rect = axs[0].barh(
        df["names"], df["Male"], color=COLORS["blue"], label=f"Male (n = {male_n})"
    )
    axs[0].bar_label(rect, padding=1, fmt=lambda x: f"{int(round(x, 0))}%")
    axs[0].tick_params(axis="y", which="major", labelsize=labels_size)
    rect = axs[1].barh(
        df["names"],
        df["Female"],
        color=COLORS["green"],
        label=f"Female (n = {female_n})",
    )
    axs[1].bar_label(rect, padding=1, fmt=lambda x: f"{int(round(x, 0))}%")
    axs[1].set_yticks([])
    for ax in axs:
        for spin in ax.spines:
            if spin != "bottom" and spin != "left":
                ax.spines[spin].set_visible(False)
        ax.xaxis.set_major_formatter(ticker.PercentFormatter())
        ax.set_xlim(0, 100)
    return fig


def plot_kids_barplot(df: pd.DataFrame, COLORS: dict = COLORS) -> plt.Figure:
    """Plots three histogram-like bar plots for the three questions from the
    kids questionnaire. The bars are groupped by gender.

    Parameters
    ----------
    df
        data from the kids questionnaire.

    COLORS, optional
        a dictionary with keys blue and green and values hexes of colors, by default COLORS


    Returns
    -------
        a matplotlib figure object with three subplots.
    """
    rgx = re.compile(r"\d\w\.")

    fig, axs = plt.subplots(figsize=(6, 4), nrows=1, ncols=3)
    for n, ax in enumerate(axs):
        df1 = (
            df.loc[df.Sex == "Female", df.columns[4 + n]]
            .value_counts()
            .reset_index()
            .assign(precent=lambda x: (x["count"] / 11) * 100)
        )
        df2 = (
            df.loc[df.Sex == "Male", df.columns[4 + n]]
            .value_counts()
            .reset_index()
            .assign(precent=lambda x: (x["count"] / 6) * 100)
        )
        rect1 = ax.bar(
            df1.iloc[:, 0].apply(lambda x: x - 0.25).tolist(),
            df1.loc[:, "precent"].tolist(),
            width=0.45,
            color=COLORS["green"],
            label="Female (n = 11)",
        )
        ax.bar_label(
            rect1, padding=0.9, fmt=lambda x: f"{int(round(x, 0))}%", fontsize=6
        )
        rect2 = ax.bar(
            df2.iloc[:, 0].apply(lambda x: x + 0.25).tolist(),
            df2.loc[:, "precent"].tolist(),
            width=0.45,
            color=COLORS["blue"],
            label="Male (n = 6)",
        )
        ax.bar_label(
            rect2, padding=0.9, fmt=lambda x: f"{int(round(x, 0))}%", fontsize=6
        )
        ax.set_xlim(0, 6)
        ax.set_ylim(0, 100)
        ax.yaxis.set_major_formatter(ticker.PercentFormatter())
        ax.set_xticks(range(1, 6))
        for spin in ax.spines:
            if spin != "bottom" and spin != "left":
                ax.spines[spin].set_visible(False)
            elif spin == "left" and n != 0:
                ax.spines[spin].set_visible(False)
        if n != 0:
            ax.set_yticks([])

        title = rgx.sub("", df.columns[4 + n].strip())
        ax.set_title("\n".join(wrap(title, 30)), fontsize=8)
    handles, labels = ax.get_legend_handles_labels()
    fig.legend(
        handles,
        labels,
        ncol=2,
        loc="center",
        bbox_to_anchor=(0.5, -0.03),
        fancybox=True,
        shadow=True,
    )
    return fig


def plot_wearables_barplot(
    gdf: pd.DataFrame, COLORS: dict = COLORS, font_size: int = 10, wrap_length: int = 10
) -> plt.Figure:
    """Plots a bar plot for the wearables data.

    Parameters
    ----------
    df
        data from the wearables questionnaire.

    COLORS, optional
        a dictionary with keys blue and green and values hexes of colors, by default COLORS

    font_size, optional
        the size of the xaxis major tick labels, by default 10

    wrap_length, optional
        the length of the string in line of the xaxis major tick labels, by default 10

    Returns
    -------
        a matplotlib figure object with one subplot.
    """
    gdf = gdf.assign(codes=lambda x: pd.Categorical(x.iloc[:, 1]).codes)
    major_ticks = dict(zip(gdf.codes, gdf.iloc[:, 1]))
    fig, axs = plt.subplots(figsize=(4, 4), nrows=1, ncols=1)
    if isinstance(axs, plt.Axes):
        axs = [axs]

    for (
        n,
        ax,
    ) in enumerate(axs):
        female = (
            gdf[gdf.iloc[:, 0] == "female"]
            .reset_index(drop=True)
            .assign(
                perc=lambda x: x.iloc[:, 2] / x.iloc[:, 2].sum() * 100,
                loc=lambda x: x["codes"] - 0.25,
            )
        )
        male = (
            gdf[gdf.iloc[:, 0] == "male"]
            .reset_index(drop=True)
            .assign(
                perc=lambda x: x.iloc[:, 2] / x.iloc[:, 2].sum() * 100,
                loc=lambda x: x["codes"] + 0.25,
            )
        )
        female_rect = ax.bar(
            female.loc[:, "loc"].tolist(),
            female.loc[:, "perc"].tolist(),
            width=0.45,
            label=f"Female (n = {female['count'].sum()})",
            color=COLORS["green"],
        )
        male_rect = ax.bar(
            male.loc[:, "loc"].tolist(),
            male.loc[:, "perc"].tolist(),
            width=0.45,
            label=f"Male (n = {male['count'].sum()})",
            color=COLORS["blue"],
        )
        ax.bar_label(female_rect, fmt=lambda x: f"{int(round(x, 0))}%")
        ax.bar_label(male_rect, fmt=lambda x: f"{int(round(x, 0))}%")
        ax.set_ylim(0, 100)
        ax.yaxis.set_major_formatter(ticker.PercentFormatter())
        ax.xaxis.set_major_formatter(
            ticker.FuncFormatter(
                lambda x, pos: "\n".join(wrap(str(major_ticks.get(x, "")), wrap_length))
            )
        )
        ax.set_xticks(list(major_ticks))
        ax.tick_params(axis="x", which="major", labelsize=font_size)

        for spin in ax.spines:
            if spin != "bottom" and spin != "left":
                ax.spines[spin].set_visible(False)
            elif spin == "left" and n != 0:
                ax.spines[spin].set_visible(False)
        if n != 0:
            ax.set_yticks([])
    handles, labels = ax.get_legend_handles_labels()
    fig.legend(
        handles,
        labels,
        ncol=2,
        loc="center",
        bbox_to_anchor=(0.5, -0.03),
        fancybox=True,
        shadow=True,
    )
    return fig


def plot_likert_barplot(
    df: pd.DataFrame,
    starting_column: int,
    n_columns: int,
    COLORS: dict = COLORS,
    legend: bool = True,
    min_tick: int = 1,
    max_tick: int = 7,
) -> plt.Figure:
    """Plots a bar plot for the likert data.

    Parameters
    ----------
    df
        data from the likert questionnaire.
    starting_column
        the index of the first column with likert data.
    n_columns
        the number of columns with likert data.
    COLORS, optional
        a dictionary with keys blue and green and values hexes of colors, by default COLORS
    legend, optional
        a boolean indicating whether to show the legend, by default True
    max_tick, optional
        an integer indicating the maximum tick on the x ax, by default 1
    min_tick, optional
        an integer indicating the minimum tick on the x ax, by default 7

    Returns
    -------
        a matplotlib figure object with the maximum of 3 subplots.
    """
    rgx = re.compile(r"^\d+\w\)")
    fig, axs = plt.subplots(figsize=(n_columns * 3, 4), nrows=1, ncols=n_columns)

    axs_flat = [axs] if isinstance(axs, plt.Axes) else axs.flat

    for n, ax in enumerate(axs_flat):
        gdf = (
            df.iloc[:, [2, starting_column + n]]
            .groupby("2 sex")
            .value_counts()
            .reset_index()
        )
        female = (
            gdf[gdf.iloc[:, 0] == "female"]
            .reset_index(drop=True)
            .assign(
                perc=lambda x: x.iloc[:, 2] / x.iloc[:, 2].sum() * 100,
                loc=lambda x: x[x.columns[1]] + 0.25,
            )
        )
        male = (
            gdf[gdf.iloc[:, 0] == "male"]
            .reset_index(drop=True)
            .assign(
                perc=lambda x: x.iloc[:, 2] / x.iloc[:, 2].sum() * 100,
                loc=lambda x: x[x.columns[1]] - 0.25,
            )
        )
        female_rect = ax.bar(
            female.loc[:, "loc"].tolist(),
            female.loc[:, "perc"].tolist(),
            width=0.45,
            label=f"Female (n = {female['count'].sum()})",
            color=COLORS["green"],
        )
        male_rect = ax.bar(
            male.loc[:, "loc"].tolist(),
            male.loc[:, "perc"].tolist(),
            width=0.45,
            label=f"Male (n = {male['count'].sum()})",
            color=COLORS["blue"],
        )
        ax.bar_label(female_rect, fmt=lambda x: f"{int(round(x, 0))}%", fontsize=6)
        ax.bar_label(male_rect, fmt=lambda x: f"{int(round(x, 0))}%", fontsize=6)
        ax.set_ylim(0, 100)
        ax.yaxis.set_major_formatter(ticker.PercentFormatter())
        ax.set_xlim(min_tick - 0.5, max_tick + 0.5)
        ax.set_xticks(list(range(min_tick, max_tick + 1, 1)))

        for spin in ax.spines:
            if spin != "bottom" and spin != "left":
                ax.spines[spin].set_visible(False)
            elif spin == "left" and n not in [0, 3]:
                ax.spines[spin].set_visible(False)
        if n not in [0, 3]:
            ax.set_yticks([])
        ax.set_title(
            "\n".join(
                wrap(
                    rgx.sub(string=gdf.columns[1].replace("_", " "), repl="")
                    .strip()
                    .capitalize(),
                    20,
                )
            ),
            fontsize=10,
            weight="bold",
        )
    handles, labels = ax.get_legend_handles_labels()
    if legend:
        fig.legend(
            handles,
            labels,
            ncol=2,
            loc="center",
            bbox_to_anchor=(0.5, -0.03),
            fancybox=True,
            shadow=True,
        )
    return fig


def plot_polish_barplot(
    gdf: pd.DataFrame, wrap_length: int = 10, font_size: int = 10, COLORS: dict = COLORS
) -> plt.Figure:
    """Plot a barplot for three category gender.

    Parameters
    ----------
    gdf
        data from polish questionnaire
    wrap_length, optional
        lenght of a string in ax major ticks, by default 10
    font_size, optional
        size of the font of a string in ax major ticks, by default 10
    COLORS, optional
        a dictionary with keys blue and green and values hexes of colors, by default COLORS

    Returns
    -------
        a matplotlib figure object
    """
    gdf = gdf.assign(codes=lambda x: pd.Categorical(x.iloc[:, 1]).codes)
    major_ticks = dict(zip(gdf.codes, gdf.iloc[:, 1]))
    location = {"female": -0.25, "male": 0, "prefer not to say": 0.25}
    fig, axs = plt.subplots(figsize=(4, 4), nrows=1, ncols=1)
    if isinstance(axs, plt.Axes):
        axs = [axs]
    for _, dfg in gdf.groupby("sex"):
        dfg = dfg.reset_index(drop=True).assign(
            perc=lambda x: x.loc[:, "count"] / x.loc[:, "count"].sum() * 100,
            loc=lambda x: x["codes"] + location[_],
        )
        rect = axs[0].bar(
            dfg.loc[:, "loc"].tolist(),
            dfg.loc[:, "perc"].tolist(),
            width=0.2,
            label=f"{_.capitalize()} (n = {dfg.loc[:, 'count'].sum()})",
            color=COLORS[_],
        )
        axs[0].bar_label(rect, fmt=lambda x: f"{int(round(x, 0))}%")
    axs[0].set_xticks(list(major_ticks))
    axs[0].yaxis.set_major_formatter(ticker.PercentFormatter())
    axs[0].xaxis.set_major_formatter(
        ticker.FuncFormatter(
            lambda x, pos: "\n".join(wrap(str(major_ticks.get(x, "")), wrap_length))
        )
    )
    for spin in axs[0].spines:
        if spin != "bottom" and spin != "left":
            axs[0].spines[spin].set_visible(False)
    axs[0].set_xticks(list(major_ticks))
    axs[0].set_ylim(0, 100)
    axs[0].tick_params(axis="x", which="major", labelsize=font_size)
    fig.legend(
        ncol=2, loc="center", bbox_to_anchor=(0.5, -0.07), fancybox=True, shadow=True
    )
