# %%
from eupolis import PROC
import pandas as pd
from eupolis.plots import (
    plot_wearables_barplot,
    plot_likert_barplot,
    plot_kids_barhplot,
)
from eupolis.utils import prepare_kids_data

# %%
df = pd.read_excel(PROC / "wearables_pireus.xlsx")
df[df.columns[20]] = df.loc[:, df.columns[20]].apply(
    lambda x: x.split(";") if isinstance(x, str) else []
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


# %%
## How long have you been using the wearable device provided for the euPOLIS study?
gdf_5 = df.iloc[:, [2, 5]].groupby("2 sex").value_counts().reset_index()
fig = plot_wearables_barplot(gdf=gdf_5)

# %%
## How frequently did you wear the device?
gdf_6 = df.iloc[:, [2, 6]].groupby("2 sex").value_counts().reset_index()
fig = plot_wearables_barplot(gdf=gdf_6)

# %%
## How often did you use the "euPOLIS by BioAssit" app?
gdf_7 = df.iloc[:, [2, 7]].groupby("2 sex").value_counts().reset_index()
fig = plot_wearables_barplot(gdf=gdf_7)

# %%
## How often did you use the "Huwaii" app?
gdf_8 = df.iloc[:, [2, 8]].groupby("2 sex").value_counts().reset_index()
fig = plot_wearables_barplot(gdf=gdf_8)

# %%
## How much do you agree with the following statements?
fig = plot_likert_barplot(df=df, starting_column=9, n_columns=3, legend=False)
fig2 = plot_likert_barplot(df=df, starting_column=12, n_columns=2, legend=True)

# %%
## How useful for you were different wearable device functions?
fig = plot_likert_barplot(df=df, starting_column=14, n_columns=3, legend=False)
fig2 = plot_likert_barplot(df=df, starting_column=17, n_columns=3, legend=True)

# %%
## Have you noticed any changes in your approach to healt and well-being since joinging the euPOLIS study?
df_11 = prepare_kids_data(df.rename(columns={"2 sex": "Sex"}), 20).rename(
    columns={"female": "Female", "male": "Male"}
)
# %%
fig = plot_kids_barhplot(df_11)
# %%
