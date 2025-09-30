"""Plot the number of people in the demo site from Spatial Audit"""

# %%
import pandas as pd
from eupolis import RAW, PNG
from eupolis.config import PEOPLE
from eupolis.plots import plot_barplot
from eupolis.utils import get_time_label, prepare_data


# %%


# %%
df = pd.read_excel(RAW / "audits/euPOLIS_sa_form_all.xlsm", sheet_name="Data")
df["time_day"] = df["time"].map(lambda x: get_time_label(x))
# %%
belgrade = prepare_data(df=df, location="Zemunski", livability=PEOPLE)
lodz_before = prepare_data(
    df=df.query("date < @pd.Timestamp(2025,5,1)"), location="Łódź", livability=PEOPLE
)
lodz_after = prepare_data(
    df=df.query("date > @pd.Timestamp(2025,5,1)"), location="Łódź", livability=PEOPLE
)
pileparken_before = prepare_data(
    df=df.query("date < @pd.Timestamp(2025,5,1)"),
    location="Pileparken",
    livability=PEOPLE,
)
pileparken_after = prepare_data(
    df=df,
    location="Pileparken",
    livability=PEOPLE,
    comparison=True,
    after=pd.Timestamp(2025, 1, 1),
)
pireus = prepare_data(df=df, location="Akti", livability=PEOPLE)
# %%
fig = plot_barplot(
    dt_ord=pireus, ticks=[-50, -25, -10, 0, 10, 25, 50], vertical_lines=[10, 25, 50]
)
fig.suptitle(
    "Age cohorts of users for different times of the day Akti Dilaveri\n(before the intervention)",
    fontsize=12,
    weight="bold",
)
fig.tight_layout()
fig.savefig(PNG / "akti-dilvaeri_population.png", dpi=200)
# %%
fig = plot_barplot(
    dt_ord=lodz_before,
    ticks=[
        -5,
        -10,
        0,
        5,
        10,
    ],
    vertical_lines=[10, 5],
)
fig.suptitle(
    "Age cohorts of users for different times of the day Pasaż Rynkowskiej\n(before the intervnetion)",
    fontsize=12,
    weight="bold",
)
fig.tight_layout()
fig.savefig(PNG / "lodz_population.png", dpi=200)

# %%
fig = plot_barplot(
    dt_ord=lodz_after,
    ticks=[
        -5,
        -10,
        0,
        5,
        10,
    ],
    vertical_lines=[10, 5],
)
fig.suptitle(
    "Age cohorts of users for different times of the day Pasaż Rynkowskiej\n (after the intervention)",
    fontsize=12,
    weight="bold",
)
fig.tight_layout()
fig.savefig(PNG / "gladsaxe_after_population.png", dpi=200)
# %%
fig = plot_barplot(
    dt_ord=belgrade,
    ticks=[
        -10,
        0,
        10,
    ],
    vertical_lines=[
        10,
    ],
)
fig.suptitle(
    "Age cohorts of users for different times of the day Zamunski Key\n(before the intervention)",
    fontsize=12,
    weight="bold",
)
fig.tight_layout()
fig.savefig(PNG / "belgrade_population.png", dpi=200)

# %%
fig = plot_barplot(
    dt_ord=pileparken_before,
    ticks=[-5, 0, 5],
    vertical_lines=[5],
    comparison=False,
)
fig.suptitle(
    "Age cohorts of users for different times of the day Pileparken 6\n (before the intervention)",
    fontsize=12,
    weight="bold",
)
fig.tight_layout()
fig.savefig(PNG / "gladsaxe_before_population.png", dpi=200)

# %%
fig = plot_barplot(
    dt_ord=pileparken_after,
    ticks=[
        -200,
        0,
        200,
    ],
    vertical_lines=[100],
    comparison=True,
)
fig.suptitle(
    "Age cohorts of users for different times of the day Pileparken 6\n (comparison between before and after the intervention)",
    fontsize=12,
    weight="bold",
)
fig.tight_layout()
fig.savefig(PNG / "gladsaxe_after_population.png", dpi=200)

# %%
