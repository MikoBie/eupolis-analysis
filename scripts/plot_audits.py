"""Plot Radar plots from Spatial Audit"""

# %%
import pandas as pd
from eupolis import RAW, PNG
from eupolis.utils import (
    rmv_str_frm_lst,
    get_time_label,
    prepare_data,
    share_replace,
    count_proportion,
    rescale_number,
)
from eupolis.plots import plot_radar
from eupolis.config import LIVABILITY, COLORS
from collections import defaultdict

from eupolis.radar import radar_factory

import matplotlib.pyplot as plt

plt.rc("savefig", transparent=False)
# %%
df = pd.read_excel(RAW / "audits/euPOLIS_sa_form_all.xlsm", sheet_name="Data")
df["share_nature"] = df["share_nature"].apply(lambda x: share_replace(x))
df["share_cars"] = df["share_cars"].apply(lambda x: 6 - share_replace(x))
df["multifunctionality_intensity"] = df.iloc[:, [i for i in range(5, 23)]].apply(
    lambda x: count_proportion(x), axis=1
)
df["multifunctionality_intensity"] = df["multifunctionality_intensity"].map(
    lambda x: rescale_number(
        value=x, original_min=0, original_max=1, new_min=1, new_max=5
    )
)
# %%

for factor, cols in LIVABILITY.items():
    df[factor] = df[cols].apply(lambda x: rmv_str_frm_lst(x).mean(), axis=1)
df["time_day"] = df["time"].map(lambda x: get_time_label(x))
N = len(LIVABILITY)
theta = radar_factory(N, frame="polygon")

# %%
pireus = prepare_data(df=df, location="Akti", livability=LIVABILITY)
gladsaxe = prepare_data(
    df=df,
    location="Pileparken",
    livability=LIVABILITY,
    comparison=True,
    after=pd.Timestamp(2025, 5, 1),
)
belgrade = prepare_data(df=df, location="Zemunski", livability=LIVABILITY)
lodz = prepare_data(
    df=df,
    location="Łódź",
    livability=LIVABILITY,
    comparison=True,
    after=pd.Timestamp(2025, 9, 1),
)

# %%
fig = plot_radar(dt_ord=pireus, theta=theta)

fig.suptitle(
    t="Livability for different times of the day Akti Dilaveri\n(before the intervention)",
    horizontalalignment="center",
    y=0.85,
    color="black",
    weight="bold",
    size="large",
)
fig.tight_layout()
fig.savefig(PNG / "radar_akti-dilaveri.png", dpi=200)
for key, value in pireus.items():
    tmp = {key: value}
    fig = plot_radar(dt_ord=tmp, theta=theta)
    fig.tight_layout()
    fig.savefig(PNG / f"radar_akti-dilaveri_{key.lower()}.png", dpi=200)

pireus_all = defaultdict(lambda: defaultdict(defaultdict))
for factor in LIVABILITY:
    pireus_all[""]["before"][factor] = pd.Series(
        [pireus[time_day]["before"][factor].mean() for time_day in pireus]
    )

fig = plot_radar(dt_ord=pireus_all, theta=theta)
fig.suptitle(
    t="Pireus Audits",
    horizontalalignment="center",
    y=0.85,
    color="black",
    weight="bold",
    size="large",
)
fig.tight_layout()
fig.savefig(PNG / "radar_daily_akti-dilaveri.png", dpi=200)


# %%
fig = plot_radar(dt_ord=lodz, theta=theta)

fig.suptitle(
    t="Livability for different times of the day Pasaż Rynkowskiej",
    horizontalalignment="center",
    y=0.85,
    color="black",
    weight="bold",
    size="large",
)
fig.tight_layout()
fig.savefig(PNG / "radar_lodz.png", dpi=200)
for key, value in lodz.items():
    tmp = {key: value}
    fig = plot_radar(dt_ord=tmp, theta=theta)
    fig.tight_layout()
    fig.savefig(PNG / f"radar_lodz_{key.lower()}.png", dpi=200)

lodz_all = defaultdict(lambda: defaultdict(defaultdict))
for factor in LIVABILITY:
    lodz_all[""]["before"][factor] = pd.Series(
        [lodz[time_day]["before"][factor].mean() for time_day in lodz]
    )

fig = plot_radar(dt_ord=lodz_all, theta=theta)
fig.suptitle(
    t="Łódź Audits",
    horizontalalignment="center",
    y=0.85,
    color="black",
    weight="bold",
    size="large",
)
fig.tight_layout()
fig.savefig(PNG / "radar_daily_lodz.png", dpi=200)
# %%
fig = plot_radar(dt_ord=belgrade, theta=theta)

fig.suptitle(
    t="Livability for different times of the day Zamunski Kej\n(before the intervention)",
    horizontalalignment="center",
    y=0.85,
    color="black",
    weight="bold",
    size="large",
)
fig.tight_layout()
fig.savefig(PNG / "radar_belgrade.png", dpi=200)
for key, value in belgrade.items():
    tmp = {key: value}
    fig = plot_radar(dt_ord=tmp, theta=theta)
    fig.tight_layout()
    fig.savefig(PNG / f"radar_belgrade_{key.lower()}.png", dpi=200)

belgrade_all = defaultdict(lambda: defaultdict(defaultdict))
for factor in LIVABILITY:
    belgrade_all[""]["before"][factor] = pd.Series(
        [belgrade[time_day]["before"][factor].mean() for time_day in belgrade]
    )

fig = plot_radar(dt_ord=belgrade_all, theta=theta)
fig.tight_layout()
fig.savefig(PNG / "radar_daily_belgrade.png", dpi=200)
# %%
fig = plot_radar(dt_ord=gladsaxe, theta=theta)

fig.suptitle(
    t="Livability for different times of the day Pileparken 6",
    horizontalalignment="center",
    y=0.85,
    color="black",
    weight="bold",
    size="large",
)
fig.tight_layout()
fig.savefig(PNG / "radar_gladsaxe_compare.png", dpi=200)

for key, value in gladsaxe.items():
    tmp = {key: value}
    fig = plot_radar(dt_ord=tmp, theta=theta)
    fig.tight_layout()
    fig.savefig(PNG / f"radar_gladsaxe_{key.lower()}_compare.png", dpi=200)

gladsaxe_all = defaultdict(lambda: defaultdict(defaultdict))
for factor in LIVABILITY:
    gladsaxe_all[""]["before"][factor] = pd.Series(
        [gladsaxe[time_day]["before"][factor].mean() for time_day in gladsaxe]
    )
    gladsaxe_all[""]["after"][factor] = pd.Series(
        [gladsaxe[time_day]["after"][factor].mean() for time_day in gladsaxe]
    )

fig = plot_radar(dt_ord=gladsaxe_all, theta=theta)
fig.tight_layout()
fig.savefig(PNG / "radar_daily_gladsaxe_compare.png", dpi=200)
# %%
gladsaxe = prepare_data(
    df=df.query("date < @pd.Timestamp(2025,5,1)"),
    location="Pileparken",
    livability=LIVABILITY,
)
fig = plot_radar(dt_ord=gladsaxe, theta=theta)

fig.suptitle(
    t="Livability for different times of the day Pileparken 6",
    horizontalalignment="center",
    y=0.85,
    color="black",
    weight="bold",
    size="large",
)
fig.tight_layout()
fig.savefig(PNG / "radar_gladsaxe.png", dpi=200)

for key, value in gladsaxe.items():
    tmp = {key: value}
    fig = plot_radar(dt_ord=tmp, theta=theta)
    fig.tight_layout()
    fig.savefig(PNG / f"radar_gladsaxe_{key.lower()}.png", dpi=200)

gladsaxe_all = defaultdict(lambda: defaultdict(defaultdict))
for factor in LIVABILITY:
    gladsaxe_all[""]["before"][factor] = pd.Series(
        [gladsaxe[time_day]["before"][factor].mean() for time_day in gladsaxe]
    )

fig = plot_radar(dt_ord=gladsaxe_all, theta=theta)
fig.tight_layout()
fig.savefig(PNG / "radar_daily_gladsaxe.png", dpi=200)

# %%
gladsaxe = prepare_data(
    df=df.query("date > @pd.Timestamp(2025,5,1)"),
    location="Pileparken",
    livability=LIVABILITY,
)
fig = plot_radar(dt_ord=gladsaxe, theta=theta, colors=COLORS)

fig.suptitle(
    t="Livability for different times of the day Pileparken 6",
    horizontalalignment="center",
    y=0.85,
    color="black",
    weight="bold",
    size="large",
)
fig.tight_layout()
fig.savefig(PNG / "radar_gladsaxe_after.png", dpi=200)

for key, value in gladsaxe.items():
    tmp = {key: value}
    fig = plot_radar(dt_ord=tmp, theta=theta, colors=COLORS)
    fig.tight_layout()
    fig.savefig(PNG / f"radar_gladsaxe_{key.lower()}_after.png", dpi=200)

gladsaxe_all = defaultdict(lambda: defaultdict(defaultdict))
for factor in LIVABILITY:
    gladsaxe_all[""]["before"][factor] = pd.Series(
        [gladsaxe[time_day]["before"][factor].mean() for time_day in gladsaxe]
    )

fig = plot_radar(dt_ord=gladsaxe_all, theta=theta, colors=COLORS)
fig.tight_layout()
fig.savefig(PNG / "radar_daily_gladsaxe_after.png", dpi=200)

# %%
