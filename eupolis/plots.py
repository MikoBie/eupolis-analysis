import matplotlib.pyplot as plt
from eupolis.config import COLORS
import numpy as np


def plot_barplot(
    dt_ord: dict,
    vertical_lines: list = [25, 50],
    ticks: list = [-50, -25, 0, 25, 50],
    colors: dict = COLORS,
):
    """Plots a histogram where bars are horizontal. The bars on the right are for men while the ones on the left for women.

    Parameters
    ----------
    f_lst
        a list with values for women. It should be of lenght 5.
    m_lst
        a list with values for women. It should be of lenght 5.
    colors, optional
        a dict with keys blue and green, by default COLORS
    vertical_lines, optional
        a list with coordinate of the vertical grid, by default [10, 50, 100]
    """
    fig, axs = plt.subplots(figsize=(9, 4), nrows=1, ncols=len(dt_ord))
    fig.subplots_adjust(wspace=0.3, hspace=0.2, top=0.85, bottom=0.05)
    for ax, time in zip(axs.flat, dt_ord):
        y_m = [np.mean(value) for key, value in dt_ord[time].items() if "_m" in key]
        y_f = [-np.mean(value) for key, value in dt_ord[time].items() if "_f" in key]
        text_x = vertical_lines[0]
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
            text_x,
            y=4.6,
            s="Men",
            horizontalalignment="center",
            verticalalignment="center",
        )
        ax.text(
            -text_x,
            y=4.6,
            s="Women",
            horizontalalignment="center",
            verticalalignment="center",
        )
        for item in vertical_lines:
            ax.axvline(x=item, linestyle="--", color="darkgrey", linewidth=0.5)
            ax.axvline(x=-item, linestyle="--", color="darkgrey", linewidth=0.5)
        ax.set_title(time, horizontalalignment="center")
        ax.set_xlim(min(y_f) - 10, max(y_m) + 10)
    return fig
