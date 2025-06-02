"""Plot Radar plots from Spatial Audit"""

# %%
import pandas as pd
import matplotlib.pyplot as plt
from eupolis import RAW, PNG
from eupolis.utils import rmv_str_frm_lst, get_time_label, process_lst
from eupolis.config import COLORS, LIVABILITY
from collections import defaultdict
import numpy as np

from eupolis.radar import radar_factory

# %%
df = pd.read_excel(RAW / "audits/euPOLIS_sa_form_all.xlsm", sheet_name="Data")
for factor, cols in LIVABILITY.items():
    df[factor] = df[cols].apply(lambda x: rmv_str_frm_lst(x).mean(), axis=1)
df["time_day"] = df["time"].map(lambda x: get_time_label(x))
N = len(LIVABILITY)
theta = radar_factory(N, frame="polygon")


# %%
def prepare_data(
    df: pd.DataFrame, location: str, livability: dict = LIVABILITY
) -> dict:
    """Prepare data for plotting radar plots. It returns a dictionary where keys are time of the day and values lists of the results.

    Parameters
    ----------
    df
        data frame with Spatial Audits
    location
        the name of the city or place. It uses contains so it does not have to be the whole name
    livability, optional
        dictionary with livability dimmensions as keys. The values are the names of specific columns, by default LIVABILITY

    Returns
    -------
        A dictionary where keys are times of the day and values lists of the results.
    """
    df = df.query(f"location.str.contains('{location}')", engine="python")
    dt = defaultdict(lambda: defaultdict(float))
    for item in livability.keys():
        for _, dft in df.groupby("time_day"):
            dt[_][item] = dft[item].dropna()
    dt_ord = {}
    for key in ["Morning", "Afternoon", "Evening"]:
        if key in dt:
            dt_ord[key] = dt.pop(key)
    return dt_ord


# %%
pireus = prepare_data(df=df, location="Akti")
gladsaxe = prepare_data(df=df, location="Pileparken")
belgrade = prepare_data(df=df, location="Zemunski")
lodz = prepare_data(df=df, location="Łódź")

# %%
dt_ord = pireus
fig, axs = plt.subplots(
    figsize=(9, 4),
    nrows=1,
    ncols=len(dt_ord),
    subplot_kw=dict(projection="radar"),
)
fig.subplots_adjust(wspace=0.5, hspace=0.20, top=0.85, bottom=0.05)

# Plot the four cases from the example data on separate Axes
for ax, time in zip(axs.flat, dt_ord):
    ax.set_rgrids([1, 2, 3, 4, 5], size=0)
    ax.set_ylim(0, 5)
    ax.set_title(
        time,
        weight="bold",
        size="medium",
        position=(0.5, 1),
        horizontalalignment="center",
        verticalalignment="center",
    )
    ax.plot(
        theta, [np.mean(item) for item in dt_ord[time].values()], color=COLORS["blue"]
    )
    ## ax.fill(
    ##     theta,
    ##     dt_ord[time].values(),
    ##     facecolor=COLORS["blue"],
    ##     alpha=0.25,
    ##     label="_nolegend_",
    ##     closed = False
    ## )
    ax.fill_between(
        theta,
        process_lst(dt_ord[time].values(), min),
        process_lst(dt_ord[time].values(), max),
        facecolor=COLORS["blue"],
        alpha=0.25,
    )
    for t, d in zip(theta, process_lst(dt_ord[time].values(), np.mean)):
        ax.text(t, d + 0.3, f"{d:.1f}", horizontalalignment="center", fontsize=6)
    ax.set_varlabels(
        dt_ord[time].keys(),
        kwargs={
            "fontsize": 6,
            "verticalalignment": "center",
            "horizontalalignment": "center",
        },
    )

# add legend relative to top-left plot
labels = ("Before Intervnetion", "After Intervnetion")
# legend = axs[0].legend(labels, loc=(-0.3, 1.4), labelspacing=0.1, fontsize="small")

fig.text(
    0.5,
    0.9,
    "Livability for different times of the day Akti Dilaveri",
    horizontalalignment="center",
    color="black",
    weight="bold",
    size="large",
)
plt.savefig(PNG / "akti-dilaveri.png", dpi=200)
plt.show()
# %%
dt_ord = lodz
fig, axs = plt.subplots(
    figsize=(9, 4),
    nrows=1,
    ncols=len(dt_ord),
    subplot_kw=dict(projection="radar"),
)
fig.subplots_adjust(wspace=0.5, hspace=0.20, top=0.8, bottom=0.05)

# Plot the four cases from the example data on separate Axes
for ax, time in zip(axs.flat, dt_ord):
    ax.set_rgrids([1, 2, 3, 4, 5], size=0)
    ax.set_ylim(0, 5)
    ax.set_title(
        time,
        weight="bold",
        size="medium",
        position=(0.5, 1),
        horizontalalignment="center",
        verticalalignment="center",
    )
    ax.plot(
        theta, [np.mean(item) for item in dt_ord[time].values()], color=COLORS["blue"]
    )
    ## ax.fill(
    ##     theta,
    ##     dt_ord[time].values(),
    ##     facecolor=COLORS["blue"],
    ##     alpha=0.25,
    ##     label="_nolegend_",
    ##     closed = False
    ## )
    ax.fill_between(
        theta,
        process_lst(dt_ord[time].values(), min),
        process_lst(dt_ord[time].values(), max),
        facecolor=COLORS["blue"],
        alpha=0.25,
    )
    for t, d in zip(theta, process_lst(dt_ord[time].values(), np.mean)):
        ax.text(t, d + 0.3, f"{d:.1f}", horizontalalignment="center", fontsize=6)
    ax.set_varlabels(
        dt_ord[time].keys(),
        kwargs={
            "fontsize": 6,
            "verticalalignment": "center",
            "horizontalalignment": "center",
        },
    )

# add legend relative to top-left plot
labels = ("Before Intervnetion", "After Intervnetion")
# legend = axs[0].legend(labels, loc=(-0.3, 1.4), labelspacing=0.1, fontsize="small")

fig.text(
    0.5,
    0.9,
    "Livability for different times of the day Pasaż Rynkowskiej",
    horizontalalignment="center",
    color="black",
    weight="bold",
    size="large",
)
plt.savefig(PNG / "lodz.png", dpi=200)
plt.show()

# %%
dt_ord = gladsaxe
fig, axs = plt.subplots(
    figsize=(9, 4),
    nrows=1,
    ncols=len(dt_ord),
    subplot_kw=dict(projection="radar"),
)
fig.subplots_adjust(wspace=0.5, hspace=0.20, top=0.85, bottom=0.05)

# Plot the four cases from the example data on separate Axes
for ax, time in zip(axs.flat, dt_ord):
    ax.set_rgrids([1, 2, 3, 4, 5], size=0)
    ax.set_ylim(0, 5)
    ax.set_title(
        time,
        weight="bold",
        size="medium",
        position=(0.5, 1),
        horizontalalignment="center",
        verticalalignment="center",
    )
    ax.plot(
        theta, [np.mean(item) for item in dt_ord[time].values()], color=COLORS["blue"]
    )
    ## ax.fill(
    ##     theta,
    ##     dt_ord[time].values(),
    ##     facecolor=COLORS["blue"],
    ##     alpha=0.25,
    ##     label="_nolegend_",
    ##     closed = False
    ## )
    ax.fill_between(
        theta,
        process_lst(dt_ord[time].values(), min),
        process_lst(dt_ord[time].values(), max),
        facecolor=COLORS["blue"],
        alpha=0.25,
    )
    for t, d in zip(theta, process_lst(dt_ord[time].values(), np.mean)):
        ax.text(t, d + 0.3, f"{d:.1f}", horizontalalignment="center", fontsize=6)
    ax.set_varlabels(
        dt_ord[time].keys(),
        kwargs={
            "fontsize": 6,
            "verticalalignment": "center",
            "horizontalalignment": "center",
        },
    )

# add legend relative to top-left plot
labels = ("Before Intervnetion", "After Intervnetion")
# legend = axs[0].legend(labels, loc=(-0.3, 1.4), labelspacing=0.1, fontsize="small")

fig.text(
    0.5,
    0.9,
    "Livability for different times of the day Pileparken 6",
    horizontalalignment="center",
    color="black",
    weight="bold",
    size="large",
)
plt.savefig(PNG / "gladsaxe.png", dpi=200)
plt.show()
# %%
dt_ord = belgrade
fig, axs = plt.subplots(
    figsize=(9, 4),
    nrows=1,
    ncols=len(dt_ord),
    subplot_kw=dict(projection="radar"),
)
fig.subplots_adjust(wspace=0.5, hspace=0.20, top=0.85, bottom=0.05)

# Plot the four cases from the example data on separate Axes
for ax, time in zip(axs.flat, dt_ord):
    ax.set_rgrids([1, 2, 3, 4, 5], size=0)
    ax.set_ylim(0, 5)
    ax.set_title(
        time,
        weight="bold",
        size="medium",
        position=(0.5, 1),
        horizontalalignment="center",
        verticalalignment="center",
    )
    ax.plot(
        theta, [np.mean(item) for item in dt_ord[time].values()], color=COLORS["blue"]
    )
    ## ax.fill(
    ##     theta,
    ##     dt_ord[time].values(),
    ##     facecolor=COLORS["blue"],
    ##     alpha=0.25,
    ##     label="_nolegend_",
    ##     closed = False
    ## )
    ax.fill_between(
        theta,
        process_lst(dt_ord[time].values(), min),
        process_lst(dt_ord[time].values(), max),
        facecolor=COLORS["blue"],
        alpha=0.25,
    )
    for t, d in zip(theta, process_lst(dt_ord[time].values(), np.mean)):
        ax.text(t, d + 0.3, f"{d:.1f}", horizontalalignment="center", fontsize=6)
    ax.set_varlabels(
        dt_ord[time].keys(),
        kwargs={
            "fontsize": 6,
            "verticalalignment": "center",
            "horizontalalignment": "center",
        },
    )

# add legend relative to top-left plot
labels = ("Before Intervnetion", "After Intervnetion")
# legend = axs[0].legend(labels, loc=(-0.3, 1.4), labelspacing=0.1, fontsize="small")

fig.text(
    0.5,
    0.9,
    "Livability for different times of the day Zemunski Kej",
    horizontalalignment="center",
    color="black",
    weight="bold",
    size="large",
)
plt.savefig(PNG / "belgrade.png", dpi=200)
plt.show()
# %%
