import matplotlib.pyplot as plt
from eupolis.config import COLORS
import numpy as np


def plot_barplot(
    dt_ord: dict,
    vertical_lines: list = [25, 50],
    ticks: list = [-50, -25, 0, 25, 50],
    colors: dict = COLORS,
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
    fig, axs = plt.subplots(figsize=(9, 4), nrows=1, ncols=len(dt_ord))
    fig.subplots_adjust(wspace=0.3, hspace=0.2, top=0.8, bottom=0.05)
    for ax, time in zip(axs.flat, dt_ord):
        y_m = [np.mean(value) for key, value in dt_ord[time].items() if "_m" in key]
        y_f = [-np.mean(value) for key, value in dt_ord[time].items() if "_f" in key]
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
    return fig


def plot_groups(dt_ord: dict, colors: dict = COLORS, xlimit: int = 10) -> plt.Figure:
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

    fig, axs = plt.subplots(figsize=(9, 4), nrows=1, ncols=len(dt_ord))
    fig.subplots_adjust(wspace=0.3, hspace=0.2, top=0.8, bottom=0.05)
    for ax, time in zip(axs.flat, dt_ord):
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
        dct = {
            map_groups[key]: float(np.mean(value))
            for key, value in dt_ord[time].items()
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
        ax.set_xticks([i for i in range(0, xlimit + 1, 5)])
    return fig
