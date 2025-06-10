import matplotlib.pyplot as plt
from eupolis.utils import process_lst
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
    fig, axs = plt.subplots(figsize=(3 * len(dt_ord), 4), nrows=1, ncols=len(dt_ord))
    fig.subplots_adjust(wspace=0.3, hspace=0.2, top=0.8, bottom=0.05)
    if len(dt_ord) == 1:
        axs_flat = [axs]
    else:
        axs_flat = axs.flat
    for ax, time in zip(axs_flat, dt_ord):
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
        for label in ax.get_xticklabels():
            if value := float(label.get_text()) < 0:
                label.set_text(abs(value))
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
        for label in ax.get_xticklabels():
            if value := float(label.get_text()) < 0:
                label.set_text(abs(value))
    return fig


def plot_radar(dt_ord: dict, theta: np.array, color: dict = COLORS) -> plt.Figure:
    """Plots radar plots.

    Parameters
    ----------
    dt_ord
        a dictionary where keys are groups and vlaues lists of frequencies
    colors, optional
        a dictionary with keys blue and green and values hexes of colors, by default COLORS
    theta
        the result of radar_factory; it an array with coordinates in polar

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
                color=COLORS["blue"],
            )
            ax.fill_between(
                theta,
                process_lst(dt_ord[time]["before"].values(), min),
                process_lst(dt_ord[time]["before"].values(), max),
                facecolor=COLORS["blue"],
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
                color=COLORS["blue"],
            )
            ax.plot(
                theta,
                [np.mean(item) for item in dt_ord[time]["after"].values()],
                color=COLORS["green"],
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
