"""Plot groups of people"""

# %%
import pandas as pd
from eupolis import RAW, PNG
from eupolis.config import GROUPS
from eupolis.plots import plot_groups
from eupolis.utils import get_time_label, prepare_data

# %%
df = pd.read_excel(RAW / "audits/euPOLIS_sa_form_all.xlsm", sheet_name="Data")
df["time_day"] = df["time"].map(lambda x: get_time_label(x))
# %%
belgrade = prepare_data(df=df, location="Zemunski", livability=GROUPS)
lodz_before = prepare_data(
    df=df.query("date < @pd.Timestamp(2025,5,1)"), location="Łódź", livability=GROUPS
)
lodz_after = prepare_data(
    df=df.query("date > @pd.Timestamp(2025,5,1)"), location="Łódź", livability=GROUPS
)
pileparken_before = prepare_data(
    df=df.query("date < @pd.Timestamp(2025,1,1)"),
    location="Pileparken",
    livability=GROUPS,
)
pileparken_after = prepare_data(
    df=df.query("date > @pd.Timestamp(2025,1,1)"),
    location="Pileparken",
    livability=GROUPS,
)
pireus = prepare_data(df=df, location="Akti", livability=GROUPS)
# %%
fig = plot_groups(dt_ord=pireus, xlimit=30)
fig.suptitle(
    "Groups of users for different times of the day Akti Dilaveri\n (before the intervention)",
    fontsize=12,
    weight="bold",
)
fig.tight_layout()
fig.savefig(PNG / "akti-dilvaeri_groups.png", dpi=200)

# %%
fig = plot_groups(dt_ord=belgrade, xlimit=15)
fig.suptitle(
    "Groups of users for different times of the day Zamunski Key\n(before the intervnetion)",
    fontsize=12,
    weight="bold",
)
fig.tight_layout()
fig.savefig(PNG / "belgrade_groups.png", dpi=200)

# %%
fig = plot_groups(dt_ord=lodz_before, xlimit=15)
fig.suptitle(
    "Groups of users for different times of the day Pasaż Rynkowskiej\n(before the intervention)",
    fontsize=12,
    weight="bold",
)
fig.tight_layout()
fig.savefig(PNG / "lodz__before_groups.png", dpi=200)

# %%
fig = plot_groups(dt_ord=lodz_after, xlimit=15, bar_color="green")
fig.suptitle(
    "Groups of users for different times of the day Pasaż Rynkowskiej\n (after the intervention)",
    fontsize=12,
    weight="bold",
)
fig.tight_layout()
fig.savefig(PNG / "lodz_after_groups.png", dpi=200)

# %%
fig = plot_groups(dt_ord=pileparken_before, xlimit=15)
fig.suptitle(
    "Groups of users for different times of the day Pileparken 6\n (before the intervention)",
    fontsize=12,
    weight="bold",
)
fig.tight_layout()
fig.savefig(PNG / "gladsaxe_before_groups.png", dpi=200)

# %%
fig = plot_groups(dt_ord=pileparken_after, xlimit=15, bar_color="green")
fig.suptitle(
    "Groups of users for different times of the day Pileparken 6\n (after the intervention)",
    fontsize=12,
    weight="bold",
)
fig.tight_layout()
fig.savefig(PNG / "gladsaxe_after_groups.png", dpi=200)

# %%
