"""Plot the number of people in the demo site from Spatial Audit"""

# %%
import pandas as pd
from eupolis import RAW
from eupolis.config import LIVABILITY
from eupolis.plots import plot_barplot
from collections import defaultdict
from eupolis.utils import get_time_label


# %%
def prepare_data(
    df: pd.DataFrame, location: str, livability: dict = LIVABILITY
) -> dict:
    """Prepare data for plotting radar plots. It returns a dictionary where keys are time of the day and values lists of the results.

    Parameters
    ----------
    df
        data frame with Spatial Audits
    location
        the name of the city or place. It uses contains so it does not have to be the whole name
    livability, optional
        dictionary with livability dimmensions as keys. The values are the names of specific columns, by default LIVABILITY

    Returns
    -------
        A dictionary where keys are times of the day and values lists of the results.
    """
    df = df.query(f"location.str.contains('{location}')", engine="python")
    dt = defaultdict(lambda: defaultdict(float))
    for item in livability.keys():
        for _, dft in df.groupby("time_day"):
            dt[_][item] = dft[item].dropna()
    dt_ord = {}
    for key in ["Morning", "Afternoon", "Evening"]:
        if key in dt:
            dt_ord[key] = dt.pop(key)
    return dt_ord


PEOPLE = {
    "ch_m": ["ch_m"],
    "ch_f": ["ch_f"],
    "y_m": ["y_m"],
    "y_f": ["y_f"],
    "ya_m": ["ya_m"],
    "ya_f": ["ya_f"],
    "ma_m": ["ma_m"],
    "ma_f": ["ma_f"],
    "s_m": ["s_m"],
    "s_f": ["s_f"],
}
# %%
df = pd.read_excel(RAW / "audits/euPOLIS_sa_form_all.xlsm", sheet_name="Data")
df["time_day"] = df["time"].map(lambda x: get_time_label(x))
# %%
belgrade = prepare_data(df=df, location="Zemunski", livability=PEOPLE)
lodz = prepare_data(df=df, location="Łódź", livability=PEOPLE)
pileparken = prepare_data(df=df, location="Pileparken", livability=PEOPLE)
pireus = prepare_data(df=df, location="Akti", livability=PEOPLE)
# %%
plot_barplot(
    dt_ord=pireus, ticks=[-50, -25, -10, 0, 10, 25, 50], vertical_lines=[10, 25, 50]
)

# %%
