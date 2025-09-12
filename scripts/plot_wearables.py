# %%
from eupolis import PROC, PNG
import pandas as pd
from eupolis.plots import (
    plot_wearables_barplot,
    plot_likert_barplot,
    plot_kids_barhplot,
)
from eupolis.utils import prepare_kids_data
from textwrap import wrap

# %%
GREEK = PNG / "mikrolimano_wearables"
df = pd.read_excel(PROC / "wearables_pireus.xlsx")
df[df.columns[20]] = df.loc[:, df.columns[20]].apply(
    lambda x: [item.strip() for item in x.split(";")] if isinstance(x, str) else []
)

# %%
## Demographics
df.groupby("2 sex").agg(
    age_mean=pd.NamedAgg(column="1 age", aggfunc="mean"),
    age_sd=pd.NamedAgg(column="1 age", aggfunc="std"),
    sex_count=pd.NamedAgg(column="1 age", aggfunc="count"),
)

# %%
## How long have you participated in the euPOLIS study?
gdf_4 = df.iloc[:, [2, 4]].groupby("2 sex").value_counts().reset_index()
fig = plot_wearables_barplot(gdf=gdf_4)

fig.savefig(
    GREEK / "how_long_have_you_participated_in_the_eupolis_study.png",
    dpi=200,
    bbox_inches="tight",
)

# %%
## How long have you been using the wearable device provided for the euPOLIS study?
gdf_5 = df.iloc[:, [2, 5]].groupby("2 sex").value_counts().reset_index()
fig = plot_wearables_barplot(gdf=gdf_5)

fig.savefig(
    GREEK
    / "how_long_have_you_been_using_the_wearable_device_provided_for_the_eupolis_study.png",
    dpi=200,
    bbox_inches="tight",
)
# %%
## How frequently did you wear the device?
gdf_6 = df.iloc[:, [2, 6]].groupby("2 sex").value_counts().reset_index()
fig = plot_wearables_barplot(gdf=gdf_6)
fig.savefig(
    GREEK / "how_frequently_did_you_wear_the_device.png", dpi=200, bbox_inches="tight"
)

# %%
## How often did you use the "euPOLIS by BioAssit" app?
gdf_7 = df.iloc[:, [2, 7]].groupby("2 sex").value_counts().reset_index()
fig = plot_wearables_barplot(gdf=gdf_7)
fig.savefig(
    GREEK / "how_often_did_you_use_the_eupolis_by_bioassist_app.png",
    dpi=200,
    bbox_inches="tight",
)

# %%
## How often did you use the "Huwaii" app?
gdf_8 = df.iloc[:, [2, 8]].groupby("2 sex").value_counts().reset_index()
fig = plot_wearables_barplot(gdf=gdf_8)
fig.savefig(
    GREEK / "how_often_did_you_use_the_huwaii_app.png", dpi=200, bbox_inches="tight"
)

# %%
## How much do you agree with the following statements?
fig = plot_likert_barplot(df=df, starting_column=9, n_columns=3, legend=False)
fig.savefig(GREEK / "statements.png", dpi=200, bbox_inches="tight")
fig2 = plot_likert_barplot(df=df, starting_column=12, n_columns=2, legend=True)
fig2.savefig(GREEK / "statements2.png", dpi=200, bbox_inches="tight")

# %%
## How useful for you were different wearable device functions?
fig = plot_likert_barplot(df=df, starting_column=14, n_columns=3, legend=False)
fig.savefig(
    GREEK / "how_useful_for_you_were_different_wearble_device_functions.png",
    dpi=200,
    bbox_inches="tight",
)
fig2 = plot_likert_barplot(df=df, starting_column=17, n_columns=3, legend=True)
fig2.savefig(
    GREEK / "how_useful_for_you_were_different_wearble_device_functions2.png",
    dpi=200,
    bbox_inches="tight",
)

# %%
## Have you noticed any changes in your approach to healt and well-being since joinging the euPOLIS study?
df_11 = prepare_kids_data(df.rename(columns={"2 sex": "Sex"}), 20).rename(
    columns={"female": "Female", "male": "Male"}
)
df_11.loc[:, "names"] = df_11.loc[:, "names"].apply(lambda x: "\n".join(wrap(x, 30)))
fig = plot_kids_barhplot(df_11, labels_size=6)
fig.legend(
    ncol=2, loc="center", bbox_to_anchor=(0.5, -0.03), fancybox=True, shadow=True
)
fig.savefig(
    GREEK
    / "have_you_notice_any_changes_in_your_approach_to_health_and_well-being_since_joining_the_eupolis_study.png",
    dpi=200,
    bbox_inches="tight",
)
# %%
## How much do you agree with the following statements?
fig = plot_likert_barplot(df=df, starting_column=21, n_columns=3, legend=False)
fig.savefig(GREEK / "statements3.png", dpi=200, bbox_inches="tight")
fig2 = plot_likert_barplot(df=df, starting_column=25, n_columns=3, legend=True)
fig2.savefig(GREEK / "statements4.png", dpi=200, bbox_inches="tight")


# %%
## Have you used a similar device in the past?
gdf_28 = df.iloc[:, [2, 28]].groupby("2 sex").value_counts().reset_index()
fig = plot_wearables_barplot(gdf=gdf_28)
fig.savefig(
    GREEK / "have_you_used_a_similar_device_in_the_past.png",
    dpi=200,
    bbox_inches="tight",
)

# %%
## Have you used a health related smartphone app in the past?
gdf_29 = df.iloc[:, [2, 29]].groupby("2 sex").value_counts().reset_index()
fig = plot_wearables_barplot(gdf=gdf_29)
fig.savefig(
    GREEK / "have_you_used_a_health_related_smartphone_app_in_the_past.png",
    dpi=200,
    bbox_inches="tight",
)

# %%
## How important are the following issues when you are thinking about monitoring your health using apps and wearables?
fig = plot_likert_barplot(df=df, starting_column=30, n_columns=3, legend=False)
fig.savefig(
    GREEK
    / "how_important_are_the_following_issues_when_you_are_thinking_about_monitoring_your_health_using_apps_and_wearables.png",
    dpi=200,
    bbox_inches="tight",
)
fig2 = plot_likert_barplot(df=df, starting_column=33, n_columns=3, legend=True)
fig2.savefig(
    GREEK
    / "how_important_are_the_following_issues_when_you_are_thinking_about_monitoring_your_health_using_apps_and_wearables.png",
    dpi=200,
    bbox_inches="tight",
)

# %%
