# %%
import pandas as pd
from eupolis import PROC, PNG
from eupolis.plots import (
    plot_wearables_barplot,
    plot_kids_barhplot,
    plot_likert_barplot,
    plot_radar,
)
from eupolis.utils import prepare_kids_data
from eupolis.radar import radar_factory
from textwrap import wrap
from collections import defaultdict

# %%
df = pd.read_excel(PROC / "questionnaire_pireus.xlsx")
df["Gender"] = df["Sex"].apply(lambda x: x.strip().lower())
df[df.columns[15]] = df[df.columns[15]].apply(
    lambda x: [item.strip() for item in x.split(",")] if isinstance(x, str) else []
)
df[df.columns[20]] = df[df.columns[20]].apply(
    lambda x: [item.strip() for item in x.split(";")] if isinstance(x, str) else []
)
df[df.columns[22]] = df[df.columns[22]].apply(
    lambda x: [item.strip() for item in x.split(";")] if isinstance(x, str) else []
)
df[df.columns[23]] = df[df.columns[23]].apply(
    lambda x: [item.strip() for item in x.split(";")] if isinstance(x, str) else []
)
df = df.assign(
    stress=lambda x: x.iloc[:, [42, 47, 49, 52, 53, 55, 59]].apply(
        lambda x: x.sum(), axis=1
    ),
    anxiety=lambda x: x.iloc[:, [43, 45, 48, 50, 56, 60, 61]].apply(
        lambda x: x.sum(), axis=1
    ),
    depression=lambda x: x.iloc[:, [44, 46, 51, 54, 57, 58, 62]].apply(
        lambda x: x.sum(), axis=1
    ),
    peace=lambda x: x.iloc[:, [63, 64, 65]].apply(lambda x: x.mean(), axis=1),
    fear=lambda x: x.iloc[:, [66, 67]].apply(lambda x: x.mean(), axis=1),
    place_attachment=lambda x: x.iloc[:, [86, 87, 88, 89, 90, 91, 92, 93, 94]].apply(
        lambda x: sum(
            [
                x.iloc[0],
                6 - x.iloc[1],
                x.iloc[2],
                x.iloc[3],
                x.iloc[4],
                6 - x.iloc[5],
                x.iloc[6],
                x.iloc[7],
                x.iloc[8],
            ]
        )
        / len(x),
        axis=1,
    ),
    social_cohesion=lambda x: x.iloc[:, [95, 96, 97, 98, 99]].apply(
        lambda x: sum([x.iloc[0], 6 - x.iloc[1], x.iloc[2], 6 - x.iloc[3], x.iloc[4]])
        / len(x),
        axis=1,
    ),
    comfort_of_use=lambda x: x.iloc[:, [73, 77]].apply(lambda x: x.mean(), axis=1),
    friendliness=lambda x: x.iloc[:, [80, 81]].apply(lambda x: x.mean(), axis=1),
    perceived_safety=lambda x: x.iloc[:, [104, 105, 74, 82]].apply(
        lambda x: x.mean(), axis=1
    ),
    quality_nature=lambda x: x.iloc[:, [78, 79]].apply(lambda x: x.mean(), axis=1),
    walkability=lambda x: x.iloc[:, [76]].apply(lambda x: x.mean(), axis=1),
    sense_place=lambda x: x.iloc[:, [83, 106, 107]].apply(lambda x: x.mean(), axis=1),
    multifunctionality=lambda x: x.iloc[:, [75]].apply(lambda x: x.mean(), axis=1),
)

# %%
## Gender
df.groupby("Gender").agg(sex_count=pd.NamedAgg(column="Age", aggfunc="count"))

# %%
## Age
gdf = (
    df.groupby(["Gender", "Age"])
    .agg(count=pd.NamedAgg(column="Age", aggfunc="count"))
    .reset_index()
)

fig = plot_wearables_barplot(gdf=gdf)

# %%
## Martial Status
gdf = (
    df.groupby(["Gender", "Martial status"])
    .agg(count=pd.NamedAgg(column="Martial status", aggfunc="count"))
    .reset_index()
)

fig = plot_wearables_barplot(gdf=gdf)

# %%
## Household income compare to the country average
gdf = df.iloc[:, [101, 4]].groupby("Gender").value_counts().reset_index()

fig = plot_wearables_barplot(gdf=gdf)
# %%
## Education level
gdf = df.iloc[:, [101, 5]].groupby("Gender").value_counts().reset_index()

fig = plot_wearables_barplot(gdf=gdf)

# %%
## Type of housing
gdf = df.iloc[:, [101, 6]].groupby("Gender").value_counts().reset_index()

fig = plot_wearables_barplot(gdf=gdf)

# %%
## Number of members in the household
gdf = df.iloc[:, [101, 7]].groupby("Gender").value_counts().reset_index()

fig = plot_wearables_barplot(gdf=gdf)
# %%
## Do you consider yourself to be a part of minority
df.iloc[:, [101, 8]].groupby("Gender").value_counts().reset_index()

# %%
## Disability -- The only answer seems to be a joke
gdf = df.iloc[:, [101, 10]].groupby("Gender").value_counts().reset_index()

fig = plot_wearables_barplot(gdf=gdf)
# %%
## Employment status
gdf = df.iloc[:, [101, 12]].groupby("Gender").value_counts().reset_index()

fig = plot_wearables_barplot(gdf=gdf, wrap_length=10, font_size=8)

# %%
## What is the number of people under 18 in your household?
gdf = df.iloc[:, [101, 13]].groupby("Gender").value_counts().reset_index()

fig = plot_wearables_barplot(gdf=gdf)
# %%
## How many children under 3 do you have?
gdf = df.iloc[:, [101, 14]].groupby("Gender").value_counts().reset_index()

fig = plot_wearables_barplot(gdf=gdf)

# %%
## Non-communicable diseases the numbers are off but not important in my opinion.
df_15 = prepare_kids_data(df, 15).rename(columns={"female": "Female", "male": "Male"})
df_15.loc[:, "names"] = df_15.loc[:, "names"].apply(lambda x: "\n".join(wrap(x, 30)))
fig = plot_kids_barhplot(df_15, labels_size=6, female_n=16, male_n=8)
fig.legend(
    ncol=2, loc="center", bbox_to_anchor=(0.5, -0.03), fancybox=True, shadow=True
)

# %%
## Do you smoke?
gdf = df.iloc[:, [101, 16]].groupby("Gender").value_counts().reset_index()

fig = plot_wearables_barplot(gdf=gdf)
# %%
## How far away do you live from the demo site?
gdf = df.iloc[:, [101, 17]].groupby("Gender").value_counts().reset_index()

fig = plot_wearables_barplot(gdf=gdf)
# %%
## When do you usually visit the demo site?
gdf = df.iloc[:, [101, 18]].groupby("Gender").value_counts().reset_index()

fig = plot_wearables_barplot(gdf=gdf)
# %%
## How often do you usually visit the demo site?
gdf = df.iloc[:, [101, 19]].groupby("Gender").value_counts().reset_index()

fig = plot_wearables_barplot(gdf=gdf, font_size=8)
fig.savefig(PNG / "greek_q_3.png", dpi=200, bbox_inches="tight")
# %%
## What time during the day you usually visit the demo site?
df_20 = (
    prepare_kids_data(df, 20)
    .rename(columns={"female": "Female", "male": "Male"})
    .fillna(0)
)
df_20.loc[:, "names"] = df_20.loc[:, "names"].apply(lambda x: "\n".join(wrap(x, 30)))
fig = plot_kids_barhplot(df_20, labels_size=6, female_n=16, male_n=8)
fig.legend(
    ncol=2, loc="center", bbox_to_anchor=(0.5, -0.03), fancybox=True, shadow=True
)
# %%
## How much time on average do you spend in the demo site per visit?
gdf = df.iloc[:, [101, 21]].groupby("Gender").value_counts().reset_index()

fig = plot_wearables_barplot(gdf=gdf)
# %%
## What do you usually do during the visits to the demo site?
df_22 = (
    prepare_kids_data(df, 22)
    .rename(columns={"female": "Female", "male": "Male"})
    .fillna(0)
)
df_22.loc[:, "names"] = df_22.loc[:, "names"].apply(lambda x: "\n".join(wrap(x, 30)))
fig = plot_kids_barhplot(df_22, labels_size=6, female_n=16, male_n=8)
fig.legend(
    ncol=2, loc="center", bbox_to_anchor=(0.5, -0.03), fancybox=True, shadow=True
)
fig.savefig(PNG / "greek_activities.png", dpi=200, bbox_inches="tight")
# %%
## What urban furniture do you usually use during your visits to the demo site?
df_23 = (
    prepare_kids_data(df, 23)
    .rename(columns={"female": "Female", "male": "Male"})
    .fillna(0)
)
df_23.loc[:, "names"] = df_23.loc[:, "names"].apply(lambda x: "\n".join(wrap(x, 30)))
fig = plot_kids_barhplot(df_23, labels_size=6, female_n=16, male_n=8)
fig.legend(
    ncol=2, loc="center", bbox_to_anchor=(0.5, -0.03), fancybox=True, shadow=True
)
fig.savefig(PNG / "greek_furnitures.png", dpi=200, bbox_inches="tight")
# %%
## During the last 7 days, on how many days did you do vigorus physical activities?
gdf = df.iloc[:, [101, 24]].groupby("Gender").value_counts().reset_index()

fig = plot_wearables_barplot(gdf=gdf)
# %%
## How much time did you usually spend doing vigorous physical activities on one of these days?
gdf = df.iloc[:, [101, 25]].groupby("Gender").value_counts().reset_index()

fig = plot_wearables_barplot(gdf=gdf)
# %%
## During the last 7 days, on how many daysi did you do moderate physical activies?
gdf = df.iloc[:, [101, 26]].groupby("Gender").value_counts().reset_index()

fig = plot_wearables_barplot(gdf=gdf)
# %%
## How much time did you usually spend doing moderate physical activities on one of these days?
gdf = df.iloc[:, [101, 27]].groupby("Gender").value_counts().reset_index()

fig = plot_wearables_barplot(gdf=gdf)
# %%
## During the last 7 days, on how many days did you walk for at least 10 minutes at a time?
gdf = df.iloc[:, [101, 28]].groupby("Gender").value_counts().reset_index()

fig = plot_wearables_barplot(gdf=gdf)
# %%
## How much time did you usually spend walking on one of these days?
gdf = df.iloc[:, [101, 29]].groupby("Gender").value_counts().reset_index()

fig = plot_wearables_barplot(gdf=gdf)
# %%
## During the last 7 days, on how many days did you pend sitting one of these days?
gdf = df.iloc[:, [101, 30]].groupby("Gender").value_counts().reset_index()

fig = plot_wearables_barplot(gdf=gdf)

# %%
## At home, how much green space (trees, grasses, flowers, etc.) can you see through the following window(s)?
gdf = df.iloc[:, [101, 31]].groupby("Gender").value_counts().reset_index()

fig = plot_wearables_barplot(gdf=gdf, font_size=7, wrap_length=20)
# %%
## How often (during the day) do you look out through the window(s)?
gdf = df.iloc[:, [101, 32]].groupby("Gender").value_counts().reset_index()

fig = plot_wearables_barplot(gdf=gdf, wrap_length=15, font_size=7)
# %%
## Quality of life
gdf = df.copy()
gdf.insert(2, "2 sex", gdf["Gender"])
fig = plot_likert_barplot(df=gdf, starting_column=34, n_columns=2)

# %%
## Quality of life
gdf = df.copy()
gdf.insert(2, "2 sex", gdf["Gender"])
fig = plot_likert_barplot(
    df=gdf, starting_column=36, n_columns=3, legend=False, max_tick=5
)
fig2 = plot_likert_barplot(
    df=gdf, starting_column=39, n_columns=3, legend=False, max_tick=5
)
fig3 = plot_likert_barplot(df=gdf, starting_column=42, n_columns=1, max_tick=5)
# %%
gdf = df.copy()
gdf.insert(2, "2 sex", gdf["Gender"])
fig = plot_likert_barplot(
    df=gdf, starting_column=69, n_columns=3, legend=False, max_tick=5
)
fig = plot_likert_barplot(
    df=gdf, starting_column=72, n_columns=2, legend=True, max_tick=5
)
# %%
## LIVABILITY
LIVABILITY = {
    "Mulitfunctionality": "multifunctionality",
    "Friendliness": "friendliness",
    "Comfort\n of use": "comfort_of_use",
    "Sense of\n safety": "perceived_safety",
    "Sense of\n place": "sense_place",
    "Contact \nwith nature": "quality_nature",
    "Walkability": "walkability",
}
pireus_all = defaultdict(lambda: defaultdict(defaultdict))

for key, value in LIVABILITY.items():
    pireus_all[""]["before"][key] = df.loc[:, value]

theta = radar_factory(len(LIVABILITY), frame="polygon")
fig = plot_radar(dt_ord=pireus_all, theta=theta, plot_between=False, std=True)
fig.suptitle(
    t="Pireus Questionnaire",
    horizontalalignment="center",
    y=0.85,
    color="black",
    weight="bold",
    size="large",
)
fig.tight_layout()
fig.savefig(PNG / "radar_daily_akti-dilaveri_questionnaire.png", dpi=200)
# %%
