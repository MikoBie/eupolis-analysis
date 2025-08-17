# %%
import pandas as pd
from eupolis import RAW, PNG
from eupolis.utils import prepare_kids_data, rescale_number
from eupolis.radar import radar_factory
from eupolis.plots import (
    plot_polish_barplot,
    plot_polish_barhplot,
    plot_radar,
    plot_polish_likert_barplot,
)
from textwrap import wrap
from collections import defaultdict
from eupolis.translation import POLISH_Q

# %%
df = pd.read_excel(RAW / "lodz" / "euPOLIS_q_form_lodz.xlsm", sheet_name="Data").rename(
    columns=POLISH_Q
)
df["activities"] = df["activities"].apply(
    lambda x: [item.strip() for item in x.split(";")] if isinstance(x, str) else []
)
df["minority_group"] = df["minority_group"].apply(
    lambda x: [item.strip() for item in x.split(";")] if isinstance(x, str) else []
)
df["furniture"] = df["furniture"].apply(
    lambda x: [item.strip() for item in x.split(";")] if isinstance(x, str) else []
)

df = df.assign(
    multifunctionality1=lambda x: x.loc[:, "facilities1":"facilities6"].apply(
        lambda x: rescale_number(
            value=x.mean() + 4, original_min=1, original_max=7, new_min=1, new_max=5
        ),
        axis=1,
    ),
    multifunctionality2=lambda x: x.loc[:, ["characteristics15"]].apply(
        lambda x: rescale_number(
            value=x.mean(), original_min=1, original_max=7, new_min=1, new_max=5
        ),
        axis=1,
    ),
    multifunctionality=lambda x: (x["multifunctionality1"] + x["multifunctionality2"])
    / 2,
    walkability=lambda x: x.loc[
        :, ["characteristics1", "characteristics2", "characteristics11"]
    ].apply(
        lambda x: rescale_number(
            value=x.mean(), original_min=1, original_max=7, new_min=1, new_max=5
        ),
        axis=1,
    ),
    friendliness=lambda x: x.loc[
        :, ["characteristics3", "characteristics16", "characteristics17"]
    ].apply(
        lambda x: rescale_number(
            value=x.mean(), original_min=1, original_max=7, new_min=1, new_max=5
        ),
        axis=1,
    ),
    safety=lambda x: x.loc[
        :,
        [
            "characteristics4",
            "characteristics5",
            "characteristics6",
            "characteristics7",
            "characteristics8",
            "characteristics23",
        ],
    ].apply(
        lambda x: rescale_number(
            value=x.mean(), original_min=1, original_max=7, new_min=1, new_max=5
        ),
        axis=1,
    ),
    comfort_use=lambda x: x.loc[
        :,
        [
            "characteristics9",
            "characteristics10",
            "characteristics14",
            "characteristics19",
            "characteristics20",
            "characteristics21",
        ],
    ].apply(
        lambda x: rescale_number(
            value=x.mean(), original_min=1, original_max=7, new_min=1, new_max=5
        ),
        axis=1,
    ),
    contact_nature=lambda x: x.loc[
        :, ["characteristics12", "characteristics13", "characteristics18"]
    ].apply(
        lambda x: rescale_number(
            value=x.mean(), original_min=1, original_max=7, new_min=1, new_max=5
        ),
        axis=1,
    ),
    sense_place=lambda x: x.loc[
        :,
        [
            "characteristics22",
            "opinions1",
            "opinions2",
            "opinions3",
            "opinions4",
            "opinions5",
            "opinions6",
            "opinions7",
        ],
    ].apply(
        lambda x: rescale_number(
            value=x.mean(), original_min=1, original_max=7, new_min=1, new_max=5
        ),
        axis=1,
    ),
)

# %%
## Demographics
## Missing age was inputed as 200. This is why for the sex prefer not to say
## the mean is nonsense (the is one person of 45 years of age).
df.groupby("sex").agg(
    age_mean=pd.NamedAgg(column="age", aggfunc="mean"),
    age_sd=pd.NamedAgg(column="age", aggfunc="std"),
    sex_count=pd.NamedAgg(column="age", aggfunc="count"),
)

# %%
## Minority group
gdf = prepare_kids_data(df.rename(columns={"sex": "Sex"}), 48).fillna(0)
gdf["names"] = gdf["names"].apply(lambda x: "\n".join(wrap(x, 30)))

fig = plot_polish_barhplot(df=gdf, female_n=27, male_n=10, other_n=3)
fig.legend(
    ncol=3, loc="center", bbox_to_anchor=(0.64, -0.03), fancybox=True, shadow=True
)
fig.tight_layout()
# %%
## Religious group
gdf = (
    df.groupby(["sex", "religious_group"])
    .agg(count=pd.NamedAgg(column="religious_group", aggfunc="count"))
    .reset_index()
)

fig = plot_polish_barplot(gdf=gdf, wrap_length=11, font_size=8)

# %%
## Education
gdf = (
    df.groupby(["sex", "education"])
    .agg(count=pd.NamedAgg(column="education", aggfunc="count"))
    .reset_index()
)

fig = plot_polish_barplot(gdf=gdf, wrap_length=10, font_size=8)

# %%
## Employment
gdf = (
    df.groupby(["sex", "employment"])
    .agg(count=pd.NamedAgg(column="employment", aggfunc="count"))
    .reset_index()
)

fig = plot_polish_barplot(gdf=gdf, wrap_length=10, font_size=8)

# %%
## Hosehold memebers
gdf = (
    df.groupby(["sex", "household_members"])
    .agg(count=pd.NamedAgg(column="household_members", aggfunc="count"))
    .reset_index()
)

fig = plot_polish_barplot(gdf=gdf, wrap_length=10, font_size=8)
# %%
## Hosehold memebers under 18
gdf = (
    df.groupby(["sex", "under18"])
    .agg(count=pd.NamedAgg(column="under18", aggfunc="count"))
    .reset_index()
)

fig = plot_polish_barplot(gdf=gdf, wrap_length=10, font_size=8)
# %%
## Hosehold memebers under 3
gdf = (
    df.groupby(["sex", "under3"])
    .agg(count=pd.NamedAgg(column="under3", aggfunc="count"))
    .reset_index()
)

fig = plot_polish_barplot(gdf=gdf, wrap_length=10, font_size=8)
# %%
## Martial status
gdf = (
    df.groupby(["sex", "martial_status"])
    .agg(count=pd.NamedAgg(column="martial_status", aggfunc="count"))
    .reset_index()
)

fig = plot_polish_barplot(gdf=gdf, wrap_length=15, font_size=8)

# %%
## Distance to the demo site
gdf = (
    df.groupby(["sex", "distance"])
    .agg(count=pd.NamedAgg(column="distance", aggfunc="count"))
    .reset_index()
)

fig = plot_polish_barplot(gdf=gdf, wrap_length=10, font_size=8)

# %%
## On which days do you visit the demo site?
gdf = (
    df.groupby(["sex", "when"])
    .agg(count=pd.NamedAgg(column="when", aggfunc="count"))
    .reset_index()
)

fig = plot_polish_barplot(gdf=gdf, wrap_length=10)
# %%
## How often do you visit the demo site?
gdf = (
    df.groupby(["sex", "often"])
    .agg(count=pd.NamedAgg(column="often", aggfunc="count"))
    .reset_index()
)

fig = plot_polish_barplot(gdf=gdf, wrap_length=10, font_size=8)
# %%
## What time during the day you usually visit the demo site?
gdf = (
    df.groupby(["sex", "time"])
    .agg(count=pd.NamedAgg(column="time", aggfunc="count"))
    .reset_index()
)

fig = plot_polish_barplot(gdf=gdf, wrap_length=10, font_size=8)

# %%
## How much time do you usually spend in the demo site during your visits?
gdf = (
    df.groupby(["sex", "spend"])
    .agg(count=pd.NamedAgg(column="spend", aggfunc="count"))
    .reset_index()
)

fig = plot_polish_barplot(gdf=gdf, wrap_length=10, font_size=8)
# %%
## What do you do usually do in the demo site?
gdf = prepare_kids_data(df.rename(columns={"sex": "Sex"}), 6).fillna(0)
gdf["names"] = gdf["names"].apply(lambda x: "\n".join(wrap(x, 30)))

fig = plot_polish_barhplot(df=gdf, female_n=27, male_n=10, other_n=3)
fig.legend(
    ncol=3, loc="center", bbox_to_anchor=(0.64, -0.03), fancybox=True, shadow=True
)
fig.tight_layout()
fig.savefig(PNG / "polish_activities.png", dpi=200, bbox_inches="tight")
# %%
## What urban furnitures do you usually use when in the demo site?
gdf = prepare_kids_data(df.rename(columns={"sex": "Sex"}), 7).fillna(0)
gdf["names"] = gdf["names"].apply(lambda x: "\n".join(wrap(x, 30)))

fig = plot_polish_barhplot(df=gdf, female_n=27, male_n=10, other_n=3)
fig.legend(
    ncol=3, loc="center", bbox_to_anchor=(0.5, -0.03), fancybox=True, shadow=True
)
fig.tight_layout()
fig.savefig(PNG / "polish_furnitures.png", dpi=200, bbox_inches="tight")
# %%
## LIVABILITY
LIVABILITY = {
    "Mulitfunctionality": "multifunctionality",
    "Friendliness": "friendliness",
    "Comfort\n of use": "comfort_use",
    "Sense of\n safety": "safety",
    "Sense of\n place": "sense_place",
    "Contact \nwith nature": "contact_nature",
    "Walkability": "walkability",
}

pireus_all = defaultdict(lambda: defaultdict(defaultdict))

for key, value in LIVABILITY.items():
    pireus_all[""]["before"][key] = df.loc[:, value]

theta = radar_factory(len(LIVABILITY), frame="polygon")
fig = plot_radar(dt_ord=pireus_all, theta=theta, plot_between=False, std=True)
fig.suptitle(
    t="Łódź Questionnaire",
    horizontalalignment="center",
    y=0.85,
    color="black",
    weight="bold",
    size="large",
)
fig.tight_layout()
fig.savefig(PNG / "radar_daily_lodz_questionnaire.png", dpi=200)
# %%
## How satisfied are you?
fig = plot_polish_likert_barplot(df=df, starting_column=53, n_columns=3, legend=False)
fig2 = plot_polish_likert_barplot(df=df, starting_column=56, n_columns=3, legend=False)
fig3 = plot_polish_likert_barplot(df=df, starting_column=59, n_columns=2, legend=True)

# %%
## LIFESTYLE
fig = plot_polish_likert_barplot(df=df, starting_column=61, n_columns=3, legend=False)
fig2 = plot_polish_likert_barplot(df=df, starting_column=64, n_columns=3, legend=False)
fig3 = plot_polish_likert_barplot(df=df, starting_column=68, n_columns=2, legend=True)
# %%
