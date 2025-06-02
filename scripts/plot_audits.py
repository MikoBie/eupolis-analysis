# %%
import pandas as pd
import matplotlib.pyplot as plt
from eupolis import RAW
from eupolis.utils import rmv_str_frm_lst, get_time_label, mean_lst, max_lst, min_lst
from eupolis.config import COLORS
from collections import defaultdict
import numpy as np

from eupolis.radar import radar_factory

# %%
df = pd.read_excel(RAW / "audits/euPOLIS_sa_form_all.xlsm", sheet_name="Data")
livability_dct = {
    "Multifunctionality": ["multifuncionality"],
    "Friendliness": ["friendlness"],
    "Comfort\n of use": ["temperature", "noise"],
    "Sense of\n safety": ["traffic_safety", "individual_safety"],
    "Sense of\n place": ["uniquness"],
    "Contact \nwith nature": ["contact_with_nature", "quality_of_nature"],
    "Walkability": ["accessibility", "surface", "with_disabilities"],
}

# %%
for factor, cols in livability_dct.items():
    df[factor] = df[cols].apply(lambda x: rmv_str_frm_lst(x).mean(), axis=1)

df["time_day"] = df["time"].map(lambda x: get_time_label(x))
df["location"] = df["location"].apply(lambda x: x.split(" - ")[0])
df = df.query("location == 'Pileparken 6'")

# %%
dt = defaultdict(lambda: defaultdict(float))
for item in livability_dct.keys():
    for _, dft in df.groupby("time_day"):
        dt[_][item] = dft[item].dropna()

dt_ord = {}
dt_ord["Morning"] = dt.pop("Morning")
dt_ord["Afternoon"] = dt.pop("Afternoon")
dt_ord["Evening"] = dt.pop("Evening")

# %%
N = 7
theta = radar_factory(N, frame="polygon")


fig, axs = plt.subplots(
    figsize=(9, 3), nrows=1, ncols=3, subplot_kw=dict(projection="radar")
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
        min_lst(dt_ord[time].values()),
        max_lst(dt_ord[time].values()),
        facecolor=COLORS["blue"],
        alpha=0.25,
        closed=False,
    )
    for t, d in zip(theta, mean_lst(dt_ord[time].values())):
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
    0.965,
    "Livability for different times of the day Pileparken 6",
    horizontalalignment="center",
    color="black",
    weight="bold",
    size="large",
)

plt.show()

# %%
