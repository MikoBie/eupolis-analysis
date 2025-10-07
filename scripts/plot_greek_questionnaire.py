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
from eupolis.config import DISTANCE

# %%
GREEK = PNG / "mikrolimano_questionnaire"
df1 = pd.read_excel(PROC / "questionnaire_pireus.xlsx")
df1["condition"] = "before"
df2 = pd.read_excel(PROC / "questionnaire_pireus_after.xlsx").rename(
    columns={"Gender": "Sex"}
)
df2["condition"] = "after"
df = pd.concat([df1, df2], ignore_index=True)


# %%
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
df.groupby(["Gender", "condition"]).agg(
    sex_count=pd.NamedAgg(column="Age", aggfunc="count")
).reset_index()

# %%
## Age
gdf = (
    df.groupby(["Gender", "Age", "condition"])
    .agg(count=pd.NamedAgg(column="Age", aggfunc="count"))
    .reset_index()
)

for cond, tdf in gdf.groupby("condition"):
    fig = plot_wearables_barplot(gdf=tdf.drop("condition", axis=1))
    fig.savefig(GREEK / f"age_{cond}.png", dpi=200, bbox_inches="tight")

# %%
## Martial Status
gdf = (
    df.groupby(["Gender", "Martial status", "condition"])
    .agg(count=pd.NamedAgg(column="Martial status", aggfunc="count"))
    .reset_index()
)

for cond, tdf in gdf.groupby("condition"):
    fig = plot_wearables_barplot(gdf=tdf.drop("condition", axis=1))
    fig.savefig(GREEK / f"martial_status_{cond}.png", dpi=200, bbox_inches="tight")

# %%
## Household income compare to the country average
gdf = (
    df.iloc[:, [101, 102, 4]]
    .groupby(["Gender", "condition"])
    .value_counts()
    .reset_index()
)

for cond, tdf in gdf.groupby("condition"):
    fig = plot_wearables_barplot(gdf=tdf.drop("condition", axis=1))
    fig.savefig(
        GREEK / f"household_income_compare_to_the_country_average_{cond}.png",
        dpi=200,
        bbox_inches="tight",
    )
# %%
## Education level
gdf = (
    df.iloc[:, [101, 102, 5]]
    .groupby(["Gender", "condition"])
    .value_counts()
    .reset_index()
)

for (
    cond,
    tdf,
) in gdf.groupby("condition"):
    fig = plot_wearables_barplot(gdf=tdf.drop("condition", axis=1))
    fig.savefig(GREEK / f"education_level_{cond}.png", dpi=200, bbox_inches="tight")

# %%
## Type of housing
gdf = (
    df.iloc[:, [101, 102, 6]]
    .groupby(["Gender", "condition"])
    .value_counts()
    .reset_index()
)

for (
    cond,
    tdf,
) in gdf.groupby("condition"):
    fig = plot_wearables_barplot(gdf=tdf.drop("condition", axis=1))
    fig.savefig(GREEK / f"type_housing_{cond}.png", dpi=200, bbox_inches="tight")

# %%
## Number of members in the household
gdf = (
    df.iloc[:, [101, 102, 7]]
    .groupby(["Gender", "condition"])
    .value_counts()
    .reset_index()
)

for cond, tdf in gdf.groupby("condition"):
    fig = plot_wearables_barplot(gdf=tdf.drop("condition", axis=1))
    fig.savefig(
        GREEK / f"number_of_members_in_the_household_{cond}.png",
        dpi=200,
        bbox_inches="tight",
    )
# %%
## Do you consider yourself to be a part of minority
df.iloc[:, [101, 102, 8]].groupby(["Gender", "condition"]).value_counts().reset_index()

# %%
## Disability -- The only answer seems to be a joke
gdf = (
    df.iloc[:, [101, 102, 10]]
    .groupby(["Gender", "condition"])
    .value_counts()
    .reset_index()
)

for cond, tdf in gdf.groupby("condition"):
    fig = plot_wearables_barplot(gdf=tdf.drop("condition", axis=1))
    fig.savefig(GREEK / f"disability_{cond}.png", dpi=200, bbox_inches="tight")
# %%
## Employment status
gdf = (
    df.iloc[:, [101, 102, 12]]
    .groupby(["Gender", "condition"])
    .value_counts()
    .reset_index()
)

for cond, tdf in gdf.groupby("condition"):
    fig = plot_wearables_barplot(
        gdf=tdf.drop("condition", axis=1), wrap_length=10, font_size=8
    )
    fig.savefig(GREEK / f"employment_status_{cond}.png", dpi=200, bbox_inches="tight")

# %%
## What is the number of people under 18 in your household?
gdf = (
    df.iloc[:, [101, 102, 13]]
    .groupby(["Gender", "condition"])
    .value_counts()
    .reset_index()
)

for cond, tdf in gdf.groupby("condition"):
    fig = plot_wearables_barplot(gdf=tdf.drop("condition", axis=1))
    fig.savefig(
        GREEK / f"what_is_the_number_of_people_under_18_in_your_household_{cond}.png",
        dpi=200,
        bbox_inches="tight",
    )
# %%
## How many children under 3 do you have?
gdf = (
    df.iloc[:, [101, 102, 14]]
    .groupby(["Gender", "condition"])
    .value_counts()
    .reset_index()
)

for cond, tdf in gdf.groupby("condition"):
    fig = plot_wearables_barplot(gdf=tdf.drop("condition", axis=1))
    fig.savefig(
        GREEK / f"how_many_children_under_3_do_you_have_{cond}.png",
        dpi=200,
        bbox_inches="tight",
    )

# %%
## Non-communicable diseases the numbers are off but not important in my opinion.
df_15 = (
    prepare_kids_data(df, 15)
    .rename(columns={"female": "Female", "male": "Male"})
    .fillna(0)
)
df_15.loc[:, "names"] = df_15.loc[:, "names"].apply(lambda x: "\n".join(wrap(x, 30)))
fig = plot_kids_barhplot(df_15, labels_size=6, female_n=16, male_n=8)
fig.legend(
    ncol=2, loc="center", bbox_to_anchor=(0.5, -0.03), fancybox=True, shadow=True
)
fig.savefig(GREEK / "non_communicable_diseases.png", dpi=200, bbox_inches="tight")

# %%
## Do you smoke?
gdf = df.iloc[:, [101, 16]].groupby("Gender").value_counts().reset_index()

fig = plot_wearables_barplot(gdf=gdf)
fig.savefig(GREEK / "do_you_smoke.png", dpi=200, bbox_inches="tight")
# %%
## How far away do you live from the demo site?
gdf = df.iloc[:, [101, 17]].groupby("Gender").value_counts().reset_index()

fig = plot_wearables_barplot(gdf=gdf)
fig.savefig(
    GREEK / "how_far_away_do_you_live_from_the_demo_site.png",
    dpi=200,
    bbox_inches="tight",
)
# %%
## When do you usually visit the demo site?
gdf = df.iloc[:, [101, 18]].groupby("Gender").value_counts().reset_index()

fig = plot_wearables_barplot(gdf=gdf)
fig.savefig(
    GREEK / "how_far_away_do_you_live_from_the_demo_site.png",
    dpi=200,
    bbox_inches="tight",
)
# %%
## How often do you usually visit the demo site?
gdf = df.iloc[:, [101, 19]].groupby("Gender").value_counts().reset_index()

fig = plot_wearables_barplot(gdf=gdf, font_size=8)
fig.savefig(
    GREEK / "how_often_do_you_usually_visit_the_demo_site.png",
    dpi=200,
    bbox_inches="tight",
)
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
fig.savefig(
    GREEK / "what_time_during_the_day_you_usally_visit_the_demo_site.png",
    dpi=200,
    bbox_inches="tight",
)
# %%
## How much time on average do you spend in the demo site per visit?
gdf = df.iloc[:, [101, 21]].groupby("Gender").value_counts().reset_index()

fig = plot_wearables_barplot(gdf=gdf)
fig.savefig(
    GREEK / "how_much_time_on_average_do_spend_in_the_demo_site_per_visit.png",
    dpi=200,
    bbox_inches="tight",
)
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
fig.savefig(
    GREEK / "what_do_you_usally_do_during_the_visits_to_the_demo_site.png",
    dpi=200,
    bbox_inches="tight",
)
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
fig.savefig(
    GREEK
    / "what_urban_furniture_do_you_usually_use_during_your_visits_to_the_demo_site.png",
    dpi=200,
    bbox_inches="tight",
)
# %%
## During the last 7 days, on how many days did you do vigorus physical activities?
gdf = df.iloc[:, [101, 24]].groupby("Gender").value_counts().reset_index()

fig = plot_wearables_barplot(gdf=gdf)
fig.savefig(
    GREEK
    / "during_the_last_7_days_on_how_many_days_did_you_do_vigorus_physical_activities.png",
    dpi=200,
    bbox_inches="tight",
)
# %%
## How much time did you usually spend doing vigorous physical activities on one of these days?
gdf = df.iloc[:, [101, 25]].groupby("Gender").value_counts().reset_index()

fig = plot_wearables_barplot(gdf=gdf)
fig.savefig(
    GREEK
    / "how_much_time_did_you_usually_spend_doing_vigorous_physical_activities_on_one_of_those_days.png",
    dpi=200,
    bbox_inches="tight",
)
# %%
## During the last 7 days, on how many daysi did you do moderate physical activies?
gdf = df.iloc[:, [101, 26]].groupby("Gender").value_counts().reset_index()

fig = plot_wearables_barplot(gdf=gdf)
fig.savefig(
    GREEK
    / "during_the_last_7_days_on_how_many_days_did_you_do_moderte_physical_activities.png",
    dpi=200,
    bbox_inches="tight",
)
# %%
## How much time did you usually spend doing moderate physical activities on one of these days?
gdf = df.iloc[:, [101, 27]].groupby("Gender").value_counts().reset_index()

fig = plot_wearables_barplot(gdf=gdf)
fig.savefig(
    GREEK
    / "how_much_time_did_you_usually_spend_doing_moderate_physical_activities_on_one_of_those_days.png",
    dpi=200,
    bbox_inches="tight",
)
# %%
## During the last 7 days, on how many days did you walk for at least 10 minutes at a time?
gdf = df.iloc[:, [101, 28]].groupby("Gender").value_counts().reset_index()

fig = plot_wearables_barplot(gdf=gdf)
fig.savefig(
    GREEK
    / "during_the_last_7_days_on_how_many_days_did_you_walk_for_at_least_10_minutes_at_a_time.png",
    dpi=200,
    bbox_inches="tight",
)
# %%
## How much time did you usually spend walking on one of these days?
gdf = df.iloc[:, [101, 29]].groupby("Gender").value_counts().reset_index()

fig = plot_wearables_barplot(gdf=gdf)
fig.savefig(
    GREEK / "how_time_did_you_usually_spend_walking_on_one_of_these_days.png",
    dpi=200,
    bbox_inches="tight",
)
# %%
## During the last 7 days, on how many days did you pend sitting one of these days?
gdf = df.iloc[:, [101, 30]].groupby("Gender").value_counts().reset_index()

fig = plot_wearables_barplot(gdf=gdf)
fig.savefig(
    GREEK
    / "during_the_last_7_days_on_how_many_days_did_you_spend_sitting_on_one_of_these_days.png",
    dpi=200,
    bbox_inches="tight",
)

# %%
## At home, how much green space (trees, grasses, flowers, etc.) can you see through the following window(s)?
gdf = df.iloc[:, [101, 31]].groupby("Gender").value_counts().reset_index()

fig = plot_wearables_barplot(gdf=gdf, font_size=7, wrap_length=20)
fig.savefig(
    GREEK / "at_home_how_much_green_space_can_you_see_though_the_following_windows.png",
    dpi=200,
    bbox_inches="tight",
)
# %%
## How often (during the day) do you look out through the window(s)?
gdf = df.iloc[:, [101, 32]].groupby("Gender").value_counts().reset_index()

fig = plot_wearables_barplot(gdf=gdf, wrap_length=15, font_size=7)
fig.savefig(
    GREEK / "how_often_during_the_day_do_you_look_out_through_the_windows.png",
    dpi=200,
    bbox_inches="tight",
)
# %%
## Quality of life
gdf = df.copy()
gdf.insert(2, "2 sex", gdf["Gender"])
fig = plot_likert_barplot(df=gdf, starting_column=34, n_columns=2)
fig.savefig(GREEK / "quality_of_life.png", dpi=200, bbox_inches="tight")

# %%
## Quality of life
gdf = df.copy()
gdf.insert(2, "2 sex", gdf["Gender"])
fig = plot_likert_barplot(
    df=gdf, starting_column=36, n_columns=3, legend=False, max_tick=5
)
fig.savefig(GREEK / "quality_of_life_1.png", dpi=200, bbox_inches="tight")
fig2 = plot_likert_barplot(
    df=gdf, starting_column=39, n_columns=3, legend=False, max_tick=5
)
fig2.savefig(GREEK / "quality_of_life_2.png", dpi=200, bbox_inches="tight")
fig3 = plot_likert_barplot(df=gdf, starting_column=42, n_columns=1, max_tick=5)
fig3.savefig(GREEK / "quality_of_life_3.png", dpi=200, bbox_inches="tight")
# %%
gdf = df.copy()
gdf.insert(2, "2 sex", gdf["Gender"])
fig = plot_likert_barplot(
    df=gdf, starting_column=69, n_columns=3, legend=False, max_tick=5
)
fig.savefig(GREEK / "expectations.png", dpi=200, bbox_inches="tight")
fig = plot_likert_barplot(
    df=gdf, starting_column=72, n_columns=2, legend=True, max_tick=5
)
fig.savefig(GREEK / "expectations_2.png", dpi=200, bbox_inches="tight")
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
fig = plot_radar(
    dt_ord=pireus_all, theta=theta, plot_between=False, std=True, distance=DISTANCE
)
fig.suptitle(
    t="Pireus Questionnaire",
    horizontalalignment="center",
    y=0.85,
    color="black",
    weight="bold",
    size="large",
)
fig.tight_layout()
fig.savefig(GREEK / "radar_daily_akti-dilaveri_questionnaire.png", dpi=200)
# %%
