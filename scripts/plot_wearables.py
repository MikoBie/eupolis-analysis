# %%
from eupolis import PROC
import pandas as pd
from eupolis.plots import plot_wearables_barplot

# %%
df = pd.read_excel(PROC / "wearables_pireus.xlsx")

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
df.iloc[:, 6].value_counts()

# %%
## How often did you use the "euPOLIS by BioAssit" app?
df.iloc[:, 7].value_counts()

# %%
## How often did you use the "Huwaii" app?
df.iloc[:, 8].value_counts()

# %%
