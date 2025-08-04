# %%
import pandas as pd
from eupolis import PROC
from eupolis.plots import plot_wearables_barplot, plot_kids_barhplot
from eupolis.utils import prepare_kids_data
from textwrap import wrap

# %%
df = pd.read_excel(PROC / "questionnaire_pireus.xlsx")
df["Gender"] = df["Gender"].apply(lambda x: x.strip().lower())
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
gdf = df.iloc[:, [1, 4]].groupby("Gender").value_counts().reset_index()

fig = plot_wearables_barplot(gdf=gdf)
# %%
## Education level
gdf = df.iloc[:, [1, 5]].groupby("Gender").value_counts().reset_index()

fig = plot_wearables_barplot(gdf=gdf)

# %%
## Type of housing
gdf = df.iloc[:, [1, 6]].groupby("Gender").value_counts().reset_index()

fig = plot_wearables_barplot(gdf=gdf)

# %%
## Number of members in the household
gdf = df.iloc[:, [1, 7]].groupby("Gender").value_counts().reset_index()

fig = plot_wearables_barplot(gdf=gdf)
# %%
## Do you consider yourself to be a part of minority
df.iloc[:, [1, 8]].groupby("Gender").value_counts().reset_index()

# %%
## Disability -- The only answer seems to be a joke
gdf = df.iloc[:, [1, 10]].groupby("Gender").value_counts().reset_index()

fig = plot_wearables_barplot(gdf=gdf)
# %%
## Employment status
gdf = df.iloc[:, [1, 12]].groupby("Gender").value_counts().reset_index()

fig = plot_wearables_barplot(gdf=gdf)

# %%
## What is the number of people under 18 in your household?
gdf = df.iloc[:, [1, 13]].groupby("Gender").value_counts().reset_index()

fig = plot_wearables_barplot(gdf=gdf)
# %%
## How many children under 3 do you have?
gdf = df.iloc[:, [1, 14]].groupby("Gender").value_counts().reset_index()

fig = plot_wearables_barplot(gdf=gdf)

# %%
## Non-communicable diseases the numbers are off but not important in my opinion.
df_15 = prepare_kids_data(df.rename(columns={"Gender": "Sex"}), 15).rename(
    columns={"female": "Female", "male": "Male"}
)
df_15.loc[:, "names"] = df_15.loc[:, "names"].apply(lambda x: "\n".join(wrap(x, 30)))
fig = plot_kids_barhplot(df_15, labels_size=6, female_n=16, male_n=8)
fig.legend(
    ncol=2, loc="center", bbox_to_anchor=(0.5, -0.03), fancybox=True, shadow=True
)

# %%
## Do you smoke?
gdf = df.iloc[:, [1, 16]].groupby("Gender").value_counts().reset_index()

fig = plot_wearables_barplot(gdf=gdf)
# %%
## How far away do you live from the demo site?
gdf = df.iloc[:, [1, 17]].groupby("Gender").value_counts().reset_index()

fig = plot_wearables_barplot(gdf=gdf)
# %%
## When do you usually visit the demo site?
gdf = df.iloc[:, [1, 18]].groupby("Gender").value_counts().reset_index()

fig = plot_wearables_barplot(gdf=gdf)
# %%
## How often do you usually visit the demo site?
gdf = df.iloc[:, [1, 19]].groupby("Gender").value_counts().reset_index()

fig = plot_wearables_barplot(gdf=gdf)
# %%
## What time during the day you usually visit the demo site?
df_20 = prepare_kids_data(df.rename(columns={"Gender": "Sex"}), 20).rename(
    columns={"female": "Female", "male": "Male"}
)
df_20.loc[:, "names"] = df_20.loc[:, "names"].apply(lambda x: "\n".join(wrap(x, 30)))
fig = plot_kids_barhplot(df_20, labels_size=6, female_n=16, male_n=8)
fig.legend(
    ncol=2, loc="center", bbox_to_anchor=(0.5, -0.03), fancybox=True, shadow=True
)
# %%
## How much time on average do you spend in the demo site per visit?
gdf = df.iloc[:, [1, 21]].groupby("Gender").value_counts().reset_index()

fig = plot_wearables_barplot(gdf=gdf)
# %%
## What do you usually do during the visits to the demo site?
df_22 = prepare_kids_data(df.rename(columns={"Gender": "Sex"}), 22).rename(
    columns={"female": "Female", "male": "Male"}
)
df_22.loc[:, "names"] = df_22.loc[:, "names"].apply(lambda x: "\n".join(wrap(x, 30)))
fig = plot_kids_barhplot(df_22, labels_size=6, female_n=16, male_n=8)
fig.legend(
    ncol=2, loc="center", bbox_to_anchor=(0.5, -0.03), fancybox=True, shadow=True
)
# %%
## What urban furniture do you usually use during your visits to the demo site?
df_23 = prepare_kids_data(df.rename(columns={"Gender": "Sex"}), 23).rename(
    columns={"female": "Female", "male": "Male"}
)
df_23.loc[:, "names"] = df_23.loc[:, "names"].apply(lambda x: "\n".join(wrap(x, 30)))
fig = plot_kids_barhplot(df_23, labels_size=6, female_n=16, male_n=8)
fig.legend(
    ncol=2, loc="center", bbox_to_anchor=(0.5, -0.03), fancybox=True, shadow=True
)
# %%
