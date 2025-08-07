# %%
import pandas as pd
from eupolis import RAW
from eupolis.utils import prepare_kids_data
from eupolis.plots import plot_polish_barplot

# %%
df = pd.read_excel(RAW / "lodz" / "euPOLIS_q_form_lodz.xlsm", sheet_name="Data")
df["activities"] = df["activities"].apply(
    lambda x: [item.strip() for item in x.split(";")] if isinstance(x, str) else []
)
df["furniture"] = df["furniture"].apply(
    lambda x: [item.strip() for item in x.split(";")] if isinstance(x, str) else []
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
gdf = (
    df.groupby(["sex", "activities"])
    .agg(count=pd.NamedAgg(column="activities", aggfunc="count"))
    .reset_index()
)

fig = plot_polish_barplot(gdf=gdf, wrap_length=10, font_size=8)
# %%
df_20 = prepare_kids_data(df.rename(columns={"sex": "Sex"}), 20)  ##.rename(
##     columns={"female": "Female", "male": "Male"}
## )
## df_20.loc[:, "names"] = df_20.loc[:, "names"].apply(lambda x: "\n".join(wrap(x, 30)))
## fig = plot_kids_barhplot(df_20, labels_size=6, female_n=16, male_n=8)
## fig.legend(
##     ncol=2, loc="center", bbox_to_anchor=(0.5, -0.03), fancybox=True, shadow=True
## )
# %%
