"""Plot groups of people"""

# %%
import pandas as pd
from eupolis import RAW, PNG
from eupolis.config import GROUPS
from eupolis.plots import plot_groups
from eupolis.utils import get_time_label, prepare_data

# %%

# %%
df = pd.read_excel(RAW / "audits/euPOLIS_sa_form_all.xlsm", sheet_name="Data")
df["time_day"] = df["time"].map(lambda x: get_time_label(x))
# %%
belgrade = prepare_data(df=df, location="Zemunski", livability=GROUPS)
lodz = prepare_data(df=df, location="Łódź", livability=GROUPS)
pileparken = prepare_data(df=df, location="Pileparken", livability=GROUPS)
pireus = prepare_data(df=df, location="Akti", livability=GROUPS)
# %%
fig = plot_groups(dt_ord=pireus, xlimit=30)
fig.suptitle(
    "Groups of users for different times of the day Akti Dilaveri",
    fontsize=12,
    weight="bold",
)
fig.tight_layout()
fig.savefig(PNG / "akti-dilvaeri_groups.png", dpi=200)

# %%
fig = plot_groups(dt_ord=belgrade, xlimit=10)
fig.suptitle(
    "Groups of users for different times of the day Zamunski Key",
    fontsize=12,
    weight="bold",
)
fig.tight_layout()
fig.savefig(PNG / "belgrade_groups.png", dpi=200)

# %%
fig = plot_groups(dt_ord=lodz, xlimit=15)
fig.suptitle(
    "Groups of users for different times of the day Pasaż Rynkowskiej",
    fontsize=12,
    weight="bold",
)
fig.tight_layout()
fig.savefig(PNG / "lodz_groups.png", dpi=200)

# %%
fig = plot_groups(dt_ord=pileparken, xlimit=10)
fig.suptitle(
    "Groups of users for different times of the day Pileparken 6",
    fontsize=12,
    weight="bold",
)
fig.tight_layout()
fig.savefig(PNG / "gladsaxe_groups.png", dpi=200)

# %%
