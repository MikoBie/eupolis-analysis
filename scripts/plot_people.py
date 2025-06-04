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
lodz = prepare_data(df=df, location="Łódź", livability=PEOPLE)
pileparken = prepare_data(df=df, location="Pileparken", livability=PEOPLE)
pireus = prepare_data(df=df, location="Akti", livability=PEOPLE)
# %%
fig = plot_barplot(
    dt_ord=pireus, ticks=[-50, -25, -10, 0, 10, 25, 50], vertical_lines=[10, 25, 50]
)
fig.suptitle(
    "Cohorts of users for different times of the day Akti Dilaveri",
    fontsize=12,
    weight="bold",
)
fig.tight_layout()
fig.savefig(PNG / "akti-dilvaeri_population.png", dpi=200)
# %%
fig = plot_barplot(
    dt_ord=lodz,
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
    "Cohorts of users for different times of the day Pasaż Rynkowskiej",
    fontsize=12,
    weight="bold",
)
fig.tight_layout()
fig.savefig(PNG / "lodz_population.png", dpi=200)

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
    "Cohorts of users for different times of the day Zamunski Key",
    fontsize=12,
    weight="bold",
)
fig.tight_layout()
fig.savefig(PNG / "belgrade_population.png", dpi=200)

# %%
fig = plot_barplot(
    dt_ord=pileparken,
    ticks=[
        -5,
        0,
        5,
    ],
    vertical_lines=[
        5,
    ],
)
fig.suptitle(
    "Cohorts of users for different times of the day Pileparken 6",
    fontsize=12,
    weight="bold",
)
fig.tight_layout()
fig.savefig(PNG / "gladsaxe_population.png", dpi=200)

# %%
